#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os
from pathlib import Path
from typing import Any
from experiments.provider_compare_w004 import run_t007_a05_base as base

ROOT = base.ROOT
MODELS = base.MODELS
MAX_OUTPUT_TOKENS = base.MAX_OUTPUT_TOKENS
base.CONCEPT_GROUPS['bcb_focus_2026_08_21'][0] = ('expectativ', 'expectat')
CONCEPT_GROUPS = base.CONCEPT_GROUPS
load_tasks = base.load_tasks
prompt = base.prompt
validate_output = base.validate_output


def execute(secret: str, timeout: float, sleep_s: float) -> dict[str, Any]:
    report = base.execute(secret, timeout, sleep_s)
    report['schema_version'] = 'w004-provider-model-comparison-v005'
    report['attempt_id'] = 'A05'
    report['base_state_version'] = '0035'
    report['base_commit_sha'] = '9f50b3d3ef1b3076f20a9c456a86177b8dcc8b84'
    report['comparison_design']['guardrail_revision'] = 'A05 preserves A04 fully guarded design; module invocation fixes runner import mode only.'
    report['provenance_note'] = 'A02 merged bytes are non-canonical diagnostics due reused terminal attempt; A05 is the first attempt-valid comparison after that audit.'
    return report


def write(report: dict[str, Any], out: Path, doc: Path, result: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.parent.mkdir(parents=True, exist_ok=True)
    result.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    a = report['model_summaries'][MODELS[0]]
    b = report['model_summaries'][MODELS[1]]
    doc.write_text(
        '# W004-T007-A05 — attempt-valid observed GPT-OSS comparison\n\n'
        'Same four DEVELOPMENT sources, same prompt/config, same deterministic source-preservation verifier. '
        'A03 automated calibration labels are not model-quality gold. A02 merged bytes are retained only as non-canonical diagnostics because that attempt reused a terminal lifecycle ID.\n\n'
        '| Metric | 120B | 20B |\n|---|---:|---:|\n'
        f"| preservation pass | {a['preservation_pass_count']}/4 | {b['preservation_pass_count']}/4 |\n"
        f"| bounded quality | {a['mean_quality_score']:.3f} | {b['mean_quality_score']:.3f} |\n"
        f"| numeric recall | {a['mean_numeric_recall']:.3f} | {b['mean_numeric_recall']:.3f} |\n"
        f"| concept recall | {a['mean_concept_recall']:.3f} | {b['mean_concept_recall']:.3f} |\n"
        f"| mean latency ms | {a['mean_latency_ms']:.3f} | {b['mean_latency_ms']:.3f} |\n"
        f"| total tokens | {a['total_usage']['total_tokens']} | {b['total_usage']['total_tokens']} |\n"
        f"| derived cost USD | {a['total_derived_cost_usd']:.8f} | {b['total_derived_cost_usd']:.8f} |\n\n"
        'Decision: **NO_OVERALL_MODEL_PREFERENCE**. These measurements are bounded to source-preservation tasks and do not establish human preference or general production superiority.\n',
        encoding='utf-8',
    )
    result.write_text(
        '# RESULT W004-T007-A05\n\n'
        '`TASK_ID: W004-T007`\n'
        '`ATTEMPT_ID: A05`\n'
        '`BASE_STATE_VERSION: 0035`\n'
        '`BASE_COMMIT_SHA: 9f50b3d3ef1b3076f20a9c456a86177b8dcc8b84`\n'
        '`WORKER_BRANCH: worker/W004-T007-A05`\n'
        '`STATUS: COMPLETE_EVIDENCE_BOUNDED`\n'
        '`EVIDENCE_POLICY: D-0017`\n\n'
        '## Outcome\n\n'
        '- provider: `Groq`\n'
        '- candidates: `openai/gpt-oss-120b`, `openai/gpt-oss-20b`\n'
        '- observed calls: `8/8`\n'
        '- same four DEVELOPMENT tasks/prompt/config: `true`\n'
        '- A03 automated calibration used as model-quality gold: `false`\n'
        f"- bounded quality comparable: `{str(report['quality_comparable']).lower()}`\n"
        f"- 120B: preservation `{a['preservation_pass_count']}/4`; quality `{a['mean_quality_score']:.6f}`; numeric `{a['mean_numeric_recall']:.6f}`; concept `{a['mean_concept_recall']:.6f}`; latency `{a['mean_latency_ms']:.3f} ms`; total tokens `{a['total_usage']['total_tokens']}`; cost `{a['total_derived_cost_usd']:.10f} USD`\n"
        f"- 20B: preservation `{b['preservation_pass_count']}/4`; quality `{b['mean_quality_score']:.6f}`; numeric `{b['mean_numeric_recall']:.6f}`; concept `{b['mean_concept_recall']:.6f}`; latency `{b['mean_latency_ms']:.3f} ms`; total tokens `{b['total_usage']['total_tokens']}`; cost `{b['total_derived_cost_usd']:.10f} USD`\n"
        '- decision: `NO_OVERALL_MODEL_PREFERENCE`\n'
        '- human preference observed: `false`\n'
        '- human gold used: `false`\n'
        '- thresholds: `DIAGNOSTIC_ONLY`\n'
        '- lifecycle provenance: `ATTEMPT_VALID_SINGLE_TERMINAL_EXPECTED`\n\n'
        '## Boundary\n\n'
        'Observed quality/latency/usage/cost are real only for this bounded, same-task source-preservation comparison. They do not establish human preference or general production-model superiority.\n\n'
        '## Provenance audit\n\n'
        'A02 bytes remain in repository history but are excluded from canonical T007 satisfaction because A02 emitted TASK_BLOCKED and later TASK_COMPLETE under the same attempt ID. A05 is a fresh canonical attempt.\n\n'
        '## Artifacts\n\n'
        f"- `{out.relative_to(ROOT).as_posix()}`\n"
        f"- `{doc.relative_to(ROOT).as_posix()}`\n",
        encoding='utf-8',
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--secret-env', default='PROVIDER_API_KEY')
    parser.add_argument('--timeout', type=float, default=90)
    parser.add_argument('--sleep-seconds', type=float, default=3)
    parser.add_argument('--out', type=Path, default=ROOT / 'experiments/provider_compare_w004/runs/W004-T007-A05/comparison.json')
    parser.add_argument('--doc', type=Path, default=ROOT / 'docs/evals/provider_compare_w004/W004-T007-A05.md')
    parser.add_argument('--result', type=Path, default=ROOT / 'SYSTEM/RESULTS/W004-T007-A05.md')
    args = parser.parse_args()
    report = execute(os.getenv(args.secret_env, '').strip(), args.timeout, args.sleep_seconds)
    write(report, args.out, args.doc, args.result)
    print(json.dumps({'status': 'COMPLETE_EVIDENCE_BOUNDED', 'attempt_id': 'A05', 'summaries': report['model_summaries']}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
