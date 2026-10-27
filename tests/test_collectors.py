from infrapilot.collectors import collect_disks, collect_report, collect_system


def test_system_has_identity_fields():
    system = collect_system()
    assert system["hostname"]
    assert system["operating_system"]
    assert system["logical_cpu_count"] is None or system["logical_cpu_count"] > 0


def test_disks_have_safe_percentages():
    for disk in collect_disks():
        assert 0 <= disk["free_percent"] <= 100
        assert disk["total_bytes"] >= disk["free_bytes"]


def test_report_is_json_ready():
    report = collect_report(services=())
    assert report["collection_mode"] == "local_read_only"
    assert report["disks"]
    assert report["services"] == []
