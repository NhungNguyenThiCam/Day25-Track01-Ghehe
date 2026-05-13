from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml
from dotenv import load_dotenv
from langsmith import Client

from vna_chatbot import answer_question, load_config, load_pages, retrieve_pages


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def sync_dataset(dataset_name: str, input_path: Path, config_path: Path) -> None:
    """Sync examples to LangSmith dataset.

    If example records include extra fields (tokens, cost, latency, tags,
    metadata, metrics, etc.), this function will attempt to push them as
    example metadata and create best-effort runs containing metrics.
    """
    load_dotenv()
    config = load_config(config_path)
    client = Client()
    # Read existing dataset if present, otherwise create it. Some Client
    # implementations expose different helpers, so use a try/except fallback
    try:
        dataset = client.read_dataset(dataset_name=dataset_name)
    except Exception:
        dataset = client.create_dataset(dataset_name=dataset_name, description="Vietnam Airlines chatbot testset")

    examples = read_jsonl(input_path)
    existing_questions = {
        example.inputs.get(config.langsmith.get("input_key", "question"), "")
        for example in client.list_examples(dataset_id=dataset.id)
    }

    created = 0
    for example in examples:
        question_key = config.langsmith.get("input_key", "question")
        question = example[question_key]
        if question in existing_questions:
            continue

        inputs = {question_key: question}
        outputs = {}
        if config.langsmith.get("reference_key") in example:
            outputs[config.langsmith.get("reference_key")] = example[config.langsmith.get("reference_key")]

        # Collect common metadata fields if present in the input example
        metadata = example.get("metadata", {}) or {}
        # Copy well-known telemetry/fields into metadata when provided
        for k in (
            "tokens",
            "cost",
            "latency",
            "dataset",
            "annotation_queue",
            "feedback",
            "reference_example",
            "error",
            "start_time",
            "first_token",
        ):
            if k in example:
                metadata.setdefault(k, example.get(k))

        tags = example.get("tags", []) or []

        # Try to create an example with full fields; fall back to minimal if API doesn't accept extras
        created_example = None
        try:
            created_example = client.create_example(
                dataset_id=dataset.id,
                inputs=inputs,
                outputs=outputs,
                metadata=metadata,
                # tags=tags,
            )
        except TypeError:
            # Older client signatures may not accept metadata/tags kwargs
            created_example = client.create_example(dataset_id=dataset.id, inputs=inputs, outputs=outputs)
        except Exception as exc:
            print(f"Warning: failed to create example with full fields: {exc}")
            created_example = client.create_example(dataset_id=dataset.id, inputs=inputs, outputs=outputs)

        created += 1

        # If the example contains precomputed metrics, try to create a run capturing them
        if isinstance(example.get("metrics"), dict):
            metrics = example.get("metrics")
            try:
                # Best-effort: some clients support create_run or create_run_for_example
                if hasattr(client, "create_run"):
                    client.create_run(
                        name="sync_metrics_run",
                        run_type="chain",
                        dataset_id=dataset.id,
                        reference_example_id=getattr(created_example, "id", None),
                        inputs=inputs,
                        outputs=outputs,
                        extra={"metrics": metrics}, # Đưa metrics vào extra an toàn hơn với API LangSmith
                        metadata=metadata,
                        tags=tags,
                    )  # type: ignore
                elif hasattr(client, "create_run_for_example"):
                    client.create_run_for_example(example_id=getattr(created_example, "id", None), metrics=metrics)  # type: ignore
                else:
                    # last resort: attach metrics into example metadata via an update call
                    if hasattr(client, "update_example") and getattr(created_example, "id", None):
                        client.update_example(example_id=created_example.id, metadata={**metadata, "metrics": metrics})
            except Exception as exc:
                print(f"Warning: failed to push metrics/run to LangSmith for question '{question}': {exc}")

    print(f"Synced {created} new examples to LangSmith dataset: {dataset_name}")


def run_local_benchmark(dataset_path: Path, config_path: Path) -> None:
    load_dotenv()
    config = load_config(config_path)
    pages = load_pages(config.data_path)
    examples = read_jsonl(dataset_path)

    for example in examples:
        question = example.get(config.langsmith.get("input_key", "question"), "")
        result = answer_question(question, config, pages)
        print(json.dumps({"question": question, "answer": result["answer"], "sources": result["sources"]}, ensure_ascii=False, indent=2))


def run_ragas_eval(dataset_path: Path, config_path: Path) -> None:
    load_dotenv()
    config = load_config(config_path)
    pages = load_pages(config.data_path)
    examples = read_jsonl(dataset_path)

    prepared_rows: list[dict] = []
    for example in examples:
        question = example.get(config.langsmith.get("input_key", "question"), "")
        reference = example.get(config.langsmith.get("reference_key", "reference"), "")
        result = answer_question(question, config, pages)
        retrieved_pages = retrieve_pages(question, pages, top_k=config.top_k)
        contexts = [page.get("body_text") or page.get("body_markdown") or "" for page in retrieved_pages]
        prepared_rows.append(
            {
                "question": question,
                "answer": result["answer"],
                "contexts": contexts,
                "ground_truth": reference,
            }
        )

    try:
        from datasets import Dataset
        from ragas import evaluate
        from ragas.metrics import answer_relevancy, context_precision, faithfulness
    except ImportError as exc:
        raise SystemExit(
            "ragas/datasets chưa được cài. Hãy chạy pip install -r requirements.txt rồi thử lại."
        ) from exc

    try:
        dataset = Dataset.from_list(prepared_rows)
        result = evaluate(
            dataset,
            metrics=[faithfulness, answer_relevancy, context_precision],
        )
        print(result)
    except Exception as exc:  # fallback simple scoring if ragas raises runtime errors
        print(f"RAGAS evaluation failed: {exc}\nFalling back to lightweight local scoring...")

        # Lightweight fallback metrics per-example
        scores = []
        for row in prepared_rows:
            answer = row.get("answer", "") or ""
            gt = (row.get("ground_truth") or "").lower()
            contexts = " ".join(row.get("contexts") or [])

            gt_tokens = set(gt.split())
            ans_tokens = set(answer.lower().split())
            ctx_tokens = set(contexts.lower().split())

            faithfulness = (len(gt_tokens & ans_tokens) / max(1, len(gt_tokens))) if gt_tokens else 0.0
            answer_relevancy_score = (len(ans_tokens & gt_tokens) / max(1, len(ans_tokens))) if ans_tokens else 0.0
            context_precision_score = (len(ans_tokens & ctx_tokens) / max(1, len(ans_tokens))) if ans_tokens else 0.0

            scores.append(
                {
                    "question": row.get("question"),
                    "faithfulness": round(faithfulness, 3),
                    "answer_relevancy": round(answer_relevancy_score, 3),
                    "context_precision": round(context_precision_score, 3),
                }
            )

        # Aggregate
        avg = {"faithfulness": 0.0, "answer_relevancy": 0.0, "context_precision": 0.0}
        for s in scores:
            avg["faithfulness"] += s["faithfulness"]
            avg["answer_relevancy"] += s["answer_relevancy"]
            avg["context_precision"] += s["context_precision"]
        n = len(scores) or 1
        avg = {k: round(v / n, 3) for k, v in avg.items()}

        print("Fallback per-example scores:")
        for s in scores:
            print(s)
        print("Fallback aggregated scores:", avg)


def main() -> None:
    parser = argparse.ArgumentParser(description="LangSmith dataset utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync-dataset", help="Create a LangSmith dataset from JSONL")
    sync_parser.add_argument("--dataset-name", required=True)
    sync_parser.add_argument("--input-file", required=True)
    sync_parser.add_argument("--config", default="config/chatbot.yaml")

    run_parser = subparsers.add_parser("run-local", help="Run the chatbot locally on a JSONL testset")
    run_parser.add_argument("--input-file", required=True)
    run_parser.add_argument("--config", default="config/chatbot.yaml")

    ragas_parser = subparsers.add_parser("run-ragas", help="Run RAGAS eval on a JSONL testset")
    ragas_parser.add_argument("--input-file", required=True)
    ragas_parser.add_argument("--config", default="config/chatbot.yaml")

    args = parser.parse_args()

    if args.command == "sync-dataset":
        sync_dataset(args.dataset_name, Path(args.input_file), Path(args.config))
    elif args.command == "run-local":
        run_local_benchmark(Path(args.input_file), Path(args.config))
    elif args.command == "run-ragas":
        run_ragas_eval(Path(args.input_file), Path(args.config))


if __name__ == "__main__":
    main()