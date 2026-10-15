"""Financial source-anchored cross-output consistency diagnostics."""
from .engine import ConsistencyBundle, FinancialAssertion, FinancialFact, VariantAssertions, evaluate_consistency

__all__ = ["ConsistencyBundle", "FinancialAssertion", "FinancialFact", "VariantAssertions", "evaluate_consistency"]
