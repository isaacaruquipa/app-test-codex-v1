from src.chismes_system import (
    ChismeIntelligenceEngine,
    GossipReport,
    Severity,
    SourceProfile,
    build_demo_engine,
)


def test_demo_engine_evaluates_report():
    engine, report = build_demo_engine()
    result = engine.evaluate(report)

    assert 0.0 <= result.credibility_score <= 1.0
    assert 0.0 <= result.risk_score <= 1.0
    assert result.severity in {Severity.LOW, Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL}
    assert "Reporte CH-001" in result.rationale


def test_higher_evidence_improves_credibility():
    sources = {
        "s1": SourceProfile("s1", reliability=0.7, bias_index=0.1, domain_expertise=["rrhh"]),
    }
    engine = ChismeIntelligenceEngine(sources=sources)

    low_evidence = GossipReport(
        report_id="A",
        text="Rumor A",
        topic="rrhh",
        source_ids=["s1"],
        evidence_count=0,
        contradiction_count=0,
        emotional_intensity=0.4,
    )
    high_evidence = GossipReport(
        report_id="B",
        text="Rumor B",
        topic="rrhh",
        source_ids=["s1"],
        evidence_count=3,
        contradiction_count=0,
        emotional_intensity=0.4,
    )

    assert engine.evaluate(high_evidence).credibility_score > engine.evaluate(low_evidence).credibility_score


def test_contradictions_increase_risk_via_uncertainty():
    sources = {
        "s1": SourceProfile("s1", reliability=0.8, bias_index=0.0, domain_expertise=["legal"]),
    }
    engine = ChismeIntelligenceEngine(sources=sources)

    base = GossipReport(
        report_id="C",
        text="Rumor C",
        topic="legal",
        source_ids=["s1"],
        evidence_count=1,
        contradiction_count=0,
        emotional_intensity=0.6,
    )
    conflicted = GossipReport(
        report_id="D",
        text="Rumor D",
        topic="legal",
        source_ids=["s1"],
        evidence_count=1,
        contradiction_count=3,
        emotional_intensity=0.6,
    )

    assert engine.evaluate(conflicted).risk_score > engine.evaluate(base).risk_score
