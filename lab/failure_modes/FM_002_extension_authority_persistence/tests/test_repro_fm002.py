from failure_modes.FM_002_extension_authority_persistence import scenario


def test_authority_persists_after_uninstall():
    result = scenario.run_baseline_with_stale_authority(host="example.com")

    assert result.authority_after_uninstall is True
    assert "example.com" in result.registry_snapshot["by_host"]
