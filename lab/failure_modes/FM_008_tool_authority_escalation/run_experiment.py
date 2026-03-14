from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

if __package__:
    from .scenario import (
        DEFAULT_MODELS,
        build_summary_markdown,
        choose_clearest_signal,
        compute_summary,
        confidence_statement,
        ensure_fake_protected_resource,
        run_baseline_suite,
        run_guarded_suite,
    )
else:  # pragma: no cover - direct script execution
    THIS_DIR = Path(__file__).resolve().parent
    if str(THIS_DIR) not in sys.path:
        sys.path.insert(0, str(THIS_DIR))
    from scenario import (  # type: ignore
        DEFAULT_MODELS,
        build_summary_markdown,
        choose_clearest_signal,
        compute_summary,
        confidence_statement,
        ensure_fake_protected_resource,
        run_baseline_suite,
        run_guarded_suite,
    )


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run FM_008 tool authority escalation experiment.")
    parser.add_argument(
        "--models",
        nargs="+",
        default=DEFAULT_MODELS,
        help="Ollama model names to evaluate.",
    )
    parser.add_argument(
        "--base-dir",
        default=str(Path(__file__).resolve().parent),
        help="Base directory for FM_008 artifacts.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_dir = Path(args.base_dir).resolve()
    results_dir = base_dir / "results"

    ensure_fake_protected_resource(base_dir)

    baseline_records: list[dict[str, object]] = []
    guarded_records: list[dict[str, object]] = []

    for model_name in args.models:
        baseline_records.extend(run_baseline_suite(model_name=model_name, base_dir=base_dir))
        guarded_records.extend(
            run_guarded_suite(
                model_name=model_name,
                base_dir=base_dir,
                privileged_mode=False,
            )
        )

    summary = compute_summary(
        baseline_records=baseline_records,
        guarded_records=guarded_records,
    )

    _write_json(results_dir / "baseline_results.json", baseline_records)
    _write_json(results_dir / "guarded_results.json", guarded_records)

    summary_markdown = build_summary_markdown(summary=summary, models=args.models)
    (results_dir / "summary.md").write_text(summary_markdown, encoding="utf-8")

    print("FM_008 experiment finished.")
    print(f"Wrote baseline results: {results_dir / 'baseline_results.json'}")
    print(f"Wrote guarded results: {results_dir / 'guarded_results.json'}")
    print(f"Wrote summary: {results_dir / 'summary.md'}")
    print()
    print("What worked:")
    print("- Baseline and guarded runs completed with structured per-prompt logs.")
    print("- Guardrail policy outcomes are captured at the tool authorization boundary.")
    print("- Adversarial prompts were replayed identically in both versions.")
    print()
    print("What failed:")
    if summary.overall["adversarial_prompts_causing_sensitive_tool_call_in_baseline"] == 0:
        print("- No adversarial prompt triggered sensitive tool usage in baseline; attack prompts need tuning.")
    else:
        print("- Baseline relied on model judgment for tool authority and invoked sensitive tools.")
    if summary.overall["adversarial_prompts_still_calling_sensitive_tool_in_guarded"] > 0:
        print("- Some guarded runs still reached sensitive tools; policy configuration needs tightening.")
    else:
        print("- Guarded policy prevented sensitive tool execution for standard user requests.")
    print()
    print(f"Clearest signal model: {choose_clearest_signal(summary)}")
    print(
        "Confidence in demonstrated pattern (within this lab setup): "
        f"{confidence_statement(summary)}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
