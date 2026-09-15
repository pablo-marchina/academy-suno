from experiments.orchestration_smoke.common import FAIL_JOB_ID, JOB_IDS
from experiments.orchestration_smoke.plain_async import run


def test_plain_async_fanout_repair_join_and_resume():
    final_state, history = run()
    assert final_state["phase"] == "complete"
    assert set(final_state["outputs"]) == set(JOB_IDS)
    assert len(history) == 2
    repaired = [job_id for job_id, item in final_state["outputs"].items() if item["repair_count"]]
    assert repaired == [FAIL_JOB_ID]
