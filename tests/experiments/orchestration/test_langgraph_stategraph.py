import pytest

pytest.importorskip("langgraph")

from experiments.orchestration_smoke.common import FAIL_JOB_ID, JOB_IDS
from experiments.orchestration_smoke.langgraph_hazards import run_hazard_probe
from experiments.orchestration_smoke.langgraph_stategraph import run


def test_langgraph_fanout_repair_join_checkpoint_resume_history_and_reducer_hazard():
    final_state, history = run()
    assert final_state["phase"] == "complete"
    assert set(final_state["outputs"]) == set(JOB_IDS)
    assert len(history) >= 3
    repaired = [job_id for job_id, item in final_state["outputs"].items() if item["repair_count"]]
    assert repaired == [FAIL_JOB_ID]
    assert "Error" in run_hazard_probe()
