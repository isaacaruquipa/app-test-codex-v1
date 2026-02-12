from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SourceProfile:
    source_id: str
    reliability: float = 0.5
    bias_index: float = 0.0
    domain_expertise: List[str] = field(default_factory=list)

    def adjusted_quality(self, topic: str) -> float:
        expertise_bonus = 0.15 if topic in self.domain_expertise else 0.0
        quality = self.reliability + expertise_bonus - (self.bias_index * 0.2)
        return _clamp(quality, 0.0, 1.0)


@dataclass
class GossipReport:
    report_id: str
    text: str
    topic: str
    source_ids: List[str]
    evidence_count: int = 0
    contradiction_count: int = 0
    emotional_intensity: float = 0.5


@dataclass
class PolicyConfig:
    credibility_thresholds: Dict[str, float]
    risk_thresholds: Dict[str, float]

    @classmethod
    def default(cls) -> "PolicyConfig":
        return cls(
            credibility_thresholds={
                "low": 0.35,
                "medium": 0.55,
                "high": 0.75,
            },
            risk_thresholds={
                "medium": 0.45,
                "high": 0.70,
                "critical": 0.85,
            },
        )


@dataclass
class EvaluationResult:
    report_id: str
    credibility_score: float
    risk_score: float
    severity: Severity
    recommendation: str
    rationale: str


class ChismeIntelligenceEngine:
    def __init__(self, sources: Dict[str, SourceProfile], policy: PolicyConfig | None = None):
        self.sources = sources
        self.policy = policy or PolicyConfig.default()

    def evaluate(self, report: GossipReport) -> EvaluationResult:
        credibility = self._credibility_score(report)
        risk = self._risk_score(report, credibility)
        severity = self._severity(risk)
        recommendation = self._recommendation(severity, credibility)
        rationale = self._build_rationale(report, credibility, risk, severity)
        return EvaluationResult(
            report_id=report.report_id,
            credibility_score=credibility,
            risk_score=risk,
            severity=severity,
            recommendation=recommendation,
            rationale=rationale,
        )

    def _credibility_score(self, report: GossipReport) -> float:
        source_quality = self._source_quality(report.source_ids, report.topic)
        evidence_bonus = min(report.evidence_count * 0.08, 0.30)
        contradiction_penalty = min(report.contradiction_count * 0.12, 0.36)
        emotional_penalty = max(0.0, (report.emotional_intensity - 0.7) * 0.25)

        score = source_quality + evidence_bonus - contradiction_penalty - emotional_penalty
        return _clamp(score, 0.0, 1.0)

    def _risk_score(self, report: GossipReport, credibility: float) -> float:
        propagation_potential = min(len(report.source_ids) * 0.12, 0.36)
        harm_potential = 0.25 + (report.emotional_intensity * 0.35)
        uncertainty_pressure = 0.35 * (1.0 - credibility)

        risk = propagation_potential + harm_potential + uncertainty_pressure
        return _clamp(risk, 0.0, 1.0)

    def _severity(self, risk_score: float) -> Severity:
        critical = self.policy.risk_thresholds["critical"]
        high = self.policy.risk_thresholds["high"]
        medium = self.policy.risk_thresholds["medium"]

        if risk_score >= critical:
            return Severity.CRITICAL
        if risk_score >= high:
            return Severity.HIGH
        if risk_score >= medium:
            return Severity.MEDIUM
        return Severity.LOW

    def _recommendation(self, severity: Severity, credibility: float) -> str:
        if severity == Severity.CRITICAL:
            return "Escalar a comité interdisciplinar + activar protocolo legal y reputacional."
        if severity == Severity.HIGH:
            return "Abrir investigación rápida, congelar difusión y exigir verificación cruzada."
        if severity == Severity.MEDIUM and credibility < self.policy.credibility_thresholds["medium"]:
            return "Mantener en observación; recolectar evidencia adicional antes de actuar."
        if severity == Severity.MEDIUM:
            return "Verificación humana focalizada con ventana de seguimiento de 24h."
        return "Monitoreo pasivo y registro para aprendizaje del sistema."

    def _source_quality(self, source_ids: List[str], topic: str) -> float:
        qualities = [
            self.sources[source_id].adjusted_quality(topic)
            for source_id in source_ids
            if source_id in self.sources
        ]
        if not qualities:
            return 0.30
        return sum(qualities) / len(qualities)

    def _build_rationale(
        self,
        report: GossipReport,
        credibility: float,
        risk: float,
        severity: Severity,
    ) -> str:
        return (
            f"Reporte {report.report_id}: credibilidad={credibility:.2f}, "
            f"riesgo={risk:.2f}, severidad={severity.value}. "
            f"Evidencias={report.evidence_count}, contradicciones={report.contradiction_count}, "
            f"intensidad emocional={report.emotional_intensity:.2f}."
        )


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def load_policy_from_yaml(path: str) -> PolicyConfig:
    import yaml

    with open(path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return PolicyConfig(
        credibility_thresholds=data["credibility_thresholds"],
        risk_thresholds=data["risk_thresholds"],
    )


def build_demo_engine() -> Tuple[ChismeIntelligenceEngine, GossipReport]:
    sources = {
        "ana": SourceProfile("ana", reliability=0.78, bias_index=0.10, domain_expertise=["equipo", "rrhh"]),
        "leo": SourceProfile("leo", reliability=0.62, bias_index=0.25, domain_expertise=["producto"]),
        "mia": SourceProfile("mia", reliability=0.70, bias_index=0.05, domain_expertise=["rrhh", "legal"]),
    }
    engine = ChismeIntelligenceEngine(sources=sources)
    report = GossipReport(
        report_id="CH-001",
        text="Se comenta una salida masiva por conflicto de liderazgo.",
        topic="rrhh",
        source_ids=["ana", "mia", "leo"],
        evidence_count=2,
        contradiction_count=1,
        emotional_intensity=0.76,
    )
    return engine, report
