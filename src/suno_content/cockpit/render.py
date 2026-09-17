from __future__ import annotations

import html
import json
from typing import Any, Mapping

from .models import CockpitSnapshot, EvidenceState, JobEvidence, Provenance


def _text(value: Any, *, na: str = "N/A") -> str:
    if value is None or value == "":
        return na
    return str(value)


def _esc(value: Any, *, na: str = "N/A") -> str:
    return html.escape(_text(value, na=na))


def _json_preview(value: Mapping[str, Any] | None, limit: int = 360) -> str:
    if not value:
        return "N/A"
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _state_badge(state: EvidenceState) -> str:
    return f'<span class="state state-{state.value.lower()}">{html.escape(state.value)}</span>'


def _provenance_rows(provenance: Provenance) -> str:
    rows = (
        ("source", provenance.source_id),
        ("source ref", provenance.source_ref),
        ("source hash", provenance.source_hash),
        ("run", provenance.run_id),
        ("job", provenance.job_id),
        ("attempt", provenance.attempt),
        ("scope", provenance.evidence_scope),
        ("observed", provenance.observed_at),
        ("artifact", provenance.evidence_ref),
    )
    return "".join(
        f"<tr><th>{html.escape(label)}</th><td>{_esc(value)}</td></tr>" for label, value in rows
    )


def _job_card(job: JobEvidence) -> str:
    evaluation = job.evaluation or {}
    reasons = evaluation.get("reasons") if isinstance(evaluation, Mapping) else None
    reason_text = "N/A"
    if isinstance(reasons, (list, tuple)) and reasons:
        reason_text = ", ".join(str(item) for item in reasons)
    return f"""
    <article class="job-card" data-state="{job.state.value}">
      <header>
        <div><strong>{_esc(job.job_id)}</strong></div>
        {_state_badge(job.state)}
      </header>
      <dl>
        <div><dt>phase</dt><dd>{_esc(job.phase)}</dd></div>
        <div><dt>failure / review reasons</dt><dd>{_esc(reason_text)}</dd></div>
        <div><dt>error</dt><dd>{_esc(job.error)}</dd></div>
      </dl>
      <details>
        <summary>Output evidence</summary>
        <pre>{html.escape(_json_preview(job.output))}</pre>
      </details>
      <details>
        <summary>Evaluation evidence</summary>
        <pre>{html.escape(_json_preview(job.evaluation))}</pre>
      </details>
      <details>
        <summary>Provenance</summary>
        <table class="kv">{_provenance_rows(job.provenance)}</table>
      </details>
    </article>
    """


def _render_grid(snapshot: CockpitSnapshot) -> str:
    audiences = ("beginner", "intermediate", "advanced")
    formats = ("article", "carousel", "short_video")
    lookup = {(job.audience, job.output_format): job for job in snapshot.jobs}
    header = "".join(f"<th>{html.escape(fmt.replace('_', ' '))}</th>" for fmt in formats)
    body_rows = []
    for audience in audiences:
        cells = "".join(
            f"<td>{_job_card(lookup[(audience, fmt)])}</td>" for fmt in formats
        )
        body_rows.append(f"<tr><th class=\"rowhead\">{html.escape(audience)}</th>{cells}</tr>")
    return f"""
    <section id="comparison">
      <div class="section-heading">
        <div>
          <p class="eyebrow">REQ-014</p>
          <h2>3×3 side-by-side evidence</h2>
        </div>
        <p class="section-note">Each cell keeps its own state. Missing branches remain <strong>NOT_RUN</strong>; hard failures are never averaged away.</p>
      </div>
      <div class="table-scroll">
        <table class="matrix">
          <thead><tr><th>audience / format</th>{header}</tr></thead>
          <tbody>{''.join(body_rows)}</tbody>
        </table>
      </div>
    </section>
    """


def _render_evidence(snapshot: CockpitSnapshot) -> str:
    rows = []
    for item in snapshot.evidence_items:
        metrics = "N/A" if not item.metrics else json.dumps(item.metrics, ensure_ascii=False, sort_keys=True)
        rows.append(
            "<tr>"
            f"<td><strong>{_esc(item.label)}</strong><div class=\"muted mono\">{_esc(item.evidence_id)}</div></td>"
            f"<td>{_state_badge(item.state)}</td>"
            f"<td>{_esc(item.detail)}</td>"
            f"<td>{_esc(metrics)}</td>"
            f"<td><details><summary>trace</summary><table class=\"kv\">{_provenance_rows(item.provenance)}</table></details></td>"
            "</tr>"
        )
    if not rows:
        rows.append('<tr><td colspan="5" class="empty">N/A — no classification artifact selected.</td></tr>')
    return f"""
    <section id="evidence">
      <div class="section-heading">
        <div><p class="eyebrow">Evidence graph</p><h2>Claim-level evidence states</h2></div>
        <p class="section-note">No aggregate readiness score is computed.</p>
      </div>
      <div class="table-scroll"><table>
        <thead><tr><th>claim</th><th>state</th><th>detail</th><th>metrics</th><th>provenance</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table></div>
    </section>
    """


def _render_repairs(snapshot: CockpitSnapshot) -> str:
    if not snapshot.repairs:
        content = '<div class="empty-panel">N/A — no versioned repair lineage selected.</div>'
    else:
        blocks = []
        for repair in snapshot.repairs:
            before_status = None if repair.before_evaluation is None else repair.before_evaluation.get("status")
            after_status = None if repair.after_evaluation is None else repair.after_evaluation.get("status")
            resolved = ", ".join(repair.resolved_failure_codes) or "N/A"
            introduced = ", ".join(repair.introduced_failure_codes) or "N/A"
            blocks.append(
                f"""
                <article class="repair-card">
                  <header><div><strong>{_esc(repair.job_id)}</strong><span class="muted"> attempt {_esc(repair.attempt_number)}</span></div></header>
                  <div class="before-after">
                    <div><p class="eyebrow">Before</p><p><strong>Status:</strong> {_esc(before_status)}</p><p class="mono wrap"><strong>hash:</strong> {_esc(repair.before_output_hash)}</p><pre>{html.escape(_json_preview(repair.before_evaluation))}</pre></div>
                    <div><p class="eyebrow">After</p><p><strong>Status:</strong> {_esc(after_status)}</p><p class="mono wrap"><strong>hash:</strong> {_esc(repair.after_output_hash)}</p><pre>{html.escape(_json_preview(repair.after_evaluation))}</pre></div>
                  </div>
                  <div class="repair-meta">
                    <span><strong>resolved:</strong> {_esc(resolved)}</span>
                    <span><strong>introduced:</strong> {_esc(introduced)}</span>
                    <span><strong>fresh hard-gate runs:</strong> {_esc(repair.fresh_hard_gate_runs)}</span>
                    <span><strong>siblings immutable:</strong> {_esc(repair.siblings_immutable)}</span>
                  </div>
                  <details><summary>Repair provenance</summary><table class="kv">{_provenance_rows(repair.provenance)}</table></details>
                </article>
                """
            )
        content = "".join(blocks)
    return f"""
    <section id="repair">
      <div class="section-heading"><div><p class="eyebrow">Control loop</p><h2>Repair before / after</h2></div></div>
      {content}
    </section>
    """


def _render_telemetry(snapshot: CockpitSnapshot) -> str:
    telemetry = snapshot.telemetry
    if telemetry is None:
        return """
        <section id="telemetry"><div class="section-heading"><div><p class="eyebrow">Observability</p><h2>Telemetry</h2></div></div>
        <div class="empty-panel">N/A — no telemetry summary selected.</div></section>
        """
    stage_rows = []
    for stage, values in sorted(telemetry.stage_latency.items()):
        if isinstance(values, Mapping):
            stage_rows.append(
                "<tr>"
                f"<td>{_esc(stage)}</td><td>{_esc(values.get('count'))}</td>"
                f"<td>{_esc(values.get('mean_ns'))}</td><td>{_esc(values.get('p50_ns'))}</td><td>{_esc(values.get('p95_ns'))}</td>"
                "</tr>"
            )
    if not stage_rows:
        stage_rows.append('<tr><td colspan="5">N/A</td></tr>')

    usage = "N/A" if telemetry.usage is None else json.dumps(telemetry.usage, ensure_ascii=False, sort_keys=True)
    production_cost = "N/A" if telemetry.observed_cost is None else json.dumps(telemetry.observed_cost, ensure_ascii=False, sort_keys=True)
    raw_cost = "N/A" if telemetry.raw_observed_cost is None else json.dumps(telemetry.raw_observed_cost, ensure_ascii=False, sort_keys=True)
    retries = json.dumps(telemetry.transport_retries, ensure_ascii=False, sort_keys=True) if telemetry.transport_retries else "N/A"
    repairs = json.dumps(telemetry.quality_repairs, ensure_ascii=False, sort_keys=True) if telemetry.quality_repairs else "N/A"
    terminal = json.dumps(telemetry.terminal, ensure_ascii=False, sort_keys=True) if telemetry.terminal else "N/A"
    cost_note = (
        "Selected raw cost is synthetic/diagnostic and is intentionally excluded from provider-cost evidence."
        if telemetry.cost_evidence_state is EvidenceState.DIAGNOSTIC_ONLY and telemetry.raw_observed_cost is not None
        else "Production-grade cost is shown only when the selected artifact has non-synthetic pricing provenance."
    )
    return f"""
    <section id="telemetry">
      <div class="section-heading"><div><p class="eyebrow">Observability</p><h2>Telemetry</h2></div><p class="section-note">run {_esc(telemetry.run_id)} · events {_esc(telemetry.event_count)}</p></div>
      <div class="telemetry-grid">
        <article class="metric-panel"><h3>Retries</h3><pre>{html.escape(retries)}</pre></article>
        <article class="metric-panel"><h3>Quality repairs</h3><pre>{html.escape(repairs)}</pre></article>
        <article class="metric-panel"><h3>Usage</h3><pre>{html.escape(usage)}</pre></article>
        <article class="metric-panel"><h3>Provider cost evidence {_state_badge(telemetry.cost_evidence_state)}</h3><p>{html.escape(cost_note)}</p><p><strong>eligible observed cost:</strong></p><pre>{html.escape(production_cost)}</pre><p><strong>raw diagnostic artifact:</strong></p><pre>{html.escape(raw_cost)}</pre></article>
      </div>
      <h3>Stage latency (ns)</h3>
      <div class="table-scroll"><table><thead><tr><th>stage</th><th>count</th><th>mean</th><th>p50</th><th>p95</th></tr></thead><tbody>{''.join(stage_rows)}</tbody></table></div>
      <details><summary>Terminal telemetry</summary><pre>{html.escape(terminal)}</pre></details>
      <details><summary>Telemetry provenance</summary><table class="kv">{_provenance_rows(telemetry.provenance)}</table></details>
    </section>
    """


def _render_source(snapshot: CockpitSnapshot) -> str:
    source_json = _json_preview(snapshot.source, limit=1000)
    source_provenance = snapshot.jobs[0].provenance if snapshot.jobs else Provenance(run_id=snapshot.run_id)
    return f"""
    <section id="source">
      <div class="section-heading"><div><p class="eyebrow">REQ-018</p><h2>Source traceability</h2></div></div>
      <div class="source-grid">
        <article class="metric-panel"><h3>Source artifact</h3><pre>{html.escape(source_json)}</pre></article>
        <article class="metric-panel"><h3>Lineage</h3><table class="kv">{_provenance_rows(source_provenance)}</table></article>
      </div>
    </section>
    """


def render_html(snapshot: CockpitSnapshot, *, title: str = "Suno Evidence Cockpit") -> str:
    """Render a dependency-free, self-contained evidence cockpit HTML document."""

    legend = "".join(_state_badge(state) for state in EvidenceState)
    blocking = ""
    if snapshot.has_failures:
        blocking += '<div class="alert alert-fail"><strong>FAIL present.</strong> Hard failure remains visible and is not compensated by any other metric.</div>'
    if snapshot.needs_review:
        blocking += '<div class="alert alert-review"><strong>REVIEW_REQUIRED present.</strong> Human/explicit review remains open.</div>'
    if not blocking:
        blocking = '<div class="alert alert-neutral">No FAIL/REVIEW_REQUIRED is present in the selected artifacts. This is not a production-readiness claim.</div>'

    artifact_rows = "".join(
        f"<tr><th>{_esc(key)}</th><td class=\"mono wrap\">{_esc(value)}</td></tr>"
        for key, value in sorted(snapshot.artifact_refs.items())
    ) or '<tr><th>artifacts</th><td>N/A</td></tr>'

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
:root {{ color-scheme: light dark; --bg:#f4f5f7; --panel:#fff; --text:#17191c; --muted:#60656d; --line:#d7dbe0; --soft:#eef1f4; --fail:#a92323; --review:#986b00; --unknown:#5d4b8a; --proven:#176b4d; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#111315; --panel:#191c20; --text:#f2f3f4; --muted:#a9afb7; --line:#343941; --soft:#22262b; --fail:#ff8585; --review:#e9bd5a; --unknown:#b9a1ef; --proven:#71d3ac; }} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text); font:14px/1.5 ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
main {{ max-width:1500px; margin:0 auto; padding:28px; }}
h1,h2,h3,p {{ margin-top:0; }} h1 {{ font-size:32px; margin-bottom:8px; }} h2 {{ font-size:22px; }} h3 {{ font-size:15px; }}
.hero {{ display:grid; grid-template-columns:minmax(0,2fr) minmax(300px,1fr); gap:18px; align-items:start; margin-bottom:20px; }}
.panel, section, .job-card, .repair-card, .metric-panel {{ background:var(--panel); border:1px solid var(--line); border-radius:12px; }}
.hero .panel {{ padding:20px; }} section {{ padding:20px; margin:18px 0; }}
.eyebrow {{ text-transform:uppercase; letter-spacing:.1em; font-size:11px; font-weight:700; color:var(--muted); margin-bottom:5px; }}
.muted,.section-note {{ color:var(--muted); }} .mono {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }} .wrap {{ overflow-wrap:anywhere; }}
.legend {{ display:flex; flex-wrap:wrap; gap:8px; margin:12px 0 0; }}
.state {{ display:inline-block; border:1px solid currentColor; border-radius:999px; padding:2px 8px; font-size:10px; font-weight:800; letter-spacing:.04em; white-space:nowrap; }}
.state-proven {{ color:var(--proven); }} .state-fail {{ color:var(--fail); }} .state-review_required {{ color:var(--review); }}
.state-diagnostic_only,.state-not_computable,.state-not_run,.state-not_comparable,.state-production_unknown {{ color:var(--unknown); }}
.alert {{ border-left:5px solid var(--line); padding:12px 14px; background:var(--panel); margin:8px 0; border-radius:8px; }}
.alert-fail {{ border-left-color:var(--fail); }} .alert-review {{ border-left-color:var(--review); }}
.section-heading {{ display:flex; justify-content:space-between; gap:16px; align-items:start; margin-bottom:14px; }} .section-heading h2 {{ margin-bottom:0; }} .section-note {{ max-width:680px; }}
table {{ border-collapse:collapse; width:100%; }} th,td {{ border-bottom:1px solid var(--line); padding:10px; text-align:left; vertical-align:top; }} thead th {{ background:var(--soft); }}
.table-scroll {{ overflow:auto; }} .matrix {{ min-width:1200px; }} .matrix > tbody > tr > td {{ width:30%; }} .rowhead {{ min-width:120px; text-transform:capitalize; background:var(--soft); }}
.job-card {{ padding:12px; min-height:290px; }} .job-card header,.repair-card header {{ display:flex; justify-content:space-between; gap:8px; align-items:start; margin-bottom:10px; }}
dl {{ margin:0 0 10px; }} dl div {{ display:grid; grid-template-columns:110px 1fr; gap:8px; }} dt {{ color:var(--muted); }} dd {{ margin:0; overflow-wrap:anywhere; }}
details {{ margin-top:10px; }} summary {{ cursor:pointer; font-weight:650; }} pre {{ white-space:pre-wrap; overflow-wrap:anywhere; background:var(--soft); border-radius:8px; padding:10px; font-size:11px; max-height:300px; overflow:auto; }}
.kv th,.kv td {{ padding:5px 7px; font-size:12px; }} .kv th {{ width:120px; color:var(--muted); font-weight:600; }}
.empty,.empty-panel {{ color:var(--muted); }} .empty-panel {{ padding:18px; background:var(--soft); border-radius:8px; }}
.before-after,.telemetry-grid,.source-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; }} .repair-card {{ padding:16px; margin:12px 0; }} .repair-meta {{ display:flex; flex-wrap:wrap; gap:12px; padding-top:10px; }}
.telemetry-grid {{ grid-template-columns:repeat(4,minmax(0,1fr)); }} .metric-panel {{ padding:14px; min-width:0; }}
@media (max-width:900px) {{ main {{ padding:16px; }} .hero,.before-after,.telemetry-grid,.source-grid {{ grid-template-columns:1fr; }} .section-heading {{ display:block; }} }}
</style>
</head>
<body>
<main>
  <div class="hero">
    <div class="panel">
      <p class="eyebrow">B13 · evidence cockpit</p>
      <h1>{html.escape(title)}</h1>
      <p>Read-only projection over versioned RESULT / RunStore / telemetry / calibration artifacts. Unknowns remain unknown; there is no aggregate green score.</p>
      <div class="legend">{legend}</div>
    </div>
    <div class="panel">
      <table class="kv">
        <tr><th>run</th><td>{_esc(snapshot.run_id)}</td></tr>
        <tr><th>task attempt</th><td>{_esc(snapshot.task_attempt_id)}</td></tr>
        <tr><th>evidence scope</th><td>{_esc(snapshot.evidence_scope)}</td></tr>
        {artifact_rows}
      </table>
    </div>
  </div>
  {blocking}
  {_render_evidence(snapshot)}
  {_render_grid(snapshot)}
  {_render_source(snapshot)}
  {_render_repairs(snapshot)}
  {_render_telemetry(snapshot)}
</main>
</body>
</html>
"""
