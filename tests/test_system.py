from src.chismes_system import (
    CaseStatus,
    ChismeIntelligenceEngine,
    ChismeOpsOrchestrator,
    FeedbackRecord,
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


def test_orchestrator_intake_prioritizes_and_escalates_high_risk_case():
    sources = {
        "s1": SourceProfile("s1", reliability=0.4, bias_index=0.2, domain_expertise=["rrhh"]),
        "s2": SourceProfile("s2", reliability=0.45, bias_index=0.3, domain_expertise=["legal"]),
    }
    engine = ChismeIntelligenceEngine(sources=sources)
    orchestrator = ChismeOpsOrchestrator(engine)

    report = GossipReport(
        report_id="E",
        text="Rumor de alto impacto reputacional.",
        topic="rrhh",
        source_ids=["s1", "s2"],
        evidence_count=0,
        contradiction_count=2,
        emotional_intensity=0.95,
    )

    case = orchestrator.intake(report)

    assert case.case_id == "CASE-E"
    assert case.priority > 0.6
    assert case.status in {CaseStatus.TRIAGE, CaseStatus.ESCALATED}
    assert case.timeline


def test_orchestrator_feedback_updates_source_reliability():
    sources = {
        "s1": SourceProfile("s1", reliability=0.5, bias_index=0.1, domain_expertise=["rrhh"]),
    }
    engine = ChismeIntelligenceEngine(sources=sources)
    orchestrator = ChismeOpsOrchestrator(engine)

    report = GossipReport(
        report_id="F",
        text="Rumor validado.",
        topic="rrhh",
        source_ids=["s1"],
        evidence_count=2,
        contradiction_count=0,
        emotional_intensity=0.5,
    )
    case = orchestrator.intake(report)

    before = engine.sources["s1"].reliability
    orchestrator.apply_feedback(
        FeedbackRecord(case_id=case.case_id, confirmed_true=True, confidence=0.75, notes="Confirmado por comité")
    )
    after = engine.sources["s1"].reliability

    assert after > before
    assert "Feedback" in case.timeline[-1]
