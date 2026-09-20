"""Links prompt/agent configuration versions to evaluation outcomes."""

from __future__ import annotations

from dataclasses import dataclass

from .regression import RegressionReport


@dataclass
class EvalResult:
    """The outcome of running one evaluation set against one configuration version."""

    version_id: str
    accuracy: float | None = None
    latency_ms: float | None = None
    cost_usd: float | None = None
    success_rate: float | None = None
    hallucination_rate: float | None = None
    user_rating: float | None = None


class Evaluator:
    """Runs an evaluation set against a version and records the outcome linkage."""

    def __init__(self, eval_set, storage=None):
        pass

    def evaluate(self, version_id: str, configuration) -> EvalResult:
        """Run the eval set against a configuration and store the result."""
        pass

    def evaluate_shadow(
        self, candidate_version_id: str, baseline_version_id: str
    ) -> RegressionReport:
        """Run a candidate version in shadow mode against the current baseline."""
        pass
