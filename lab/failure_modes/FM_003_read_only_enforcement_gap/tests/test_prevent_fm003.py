from failure_modes.FM_003_read_only_enforcement_gap import scenario


def test_write_tools_absent_in_guarded_read_only_mode():
    result = scenario.run_guarded_read_only_registry(read_only=True)

    for tool in scenario.WRITE_TOOLS:
        assert tool not in result.exposed_tools
    assert result.read_only is True
