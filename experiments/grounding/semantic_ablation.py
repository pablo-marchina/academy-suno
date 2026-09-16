"""Adapter-neutral semantic ablation entry helper.

No provider/model is selected here. Experiments construct a candidate SemanticAdapter,
pass frozen claims/evidence to run_semantic_ablation(), and persist the returned
versioned result for evidence-based comparison.
"""

from suno_content.grounding import run_semantic_ablation

__all__ = ["run_semantic_ablation"]
