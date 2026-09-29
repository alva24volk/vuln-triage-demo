from src.triage import sort_by_severity


def test_sort_by_severity_orders_critical_first():
    findings = [
        {"id": "1", "severity": "low"},
        {"id": "2", "severity": "critical"},
        {"id": "3", "severity": "medium"},
    ]
    result = sort_by_severity(findings)
    assert [f["id"] for f in result] == ["2", "3", "1"]


def test_sort_by_severity_handles_missing_severity():
    findings = [{"id": "1"}, {"id": "2", "severity": "high"}]
    result = sort_by_severity(findings)
    assert result[0]["id"] == "2"
