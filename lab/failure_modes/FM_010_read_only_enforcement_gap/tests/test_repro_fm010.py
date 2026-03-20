from failure_modes.FM_010_read_only_enforcement_gap import scenario


def test_write_tools_exposed_in_read_only_baseline():
    result = scenario.run_baseline_with_read_only_flag(read_only=True)

    for tool in scenario.WRITE_TOOLS:
        assert tool in result.exposed_tools
    assert result.read_only is True
