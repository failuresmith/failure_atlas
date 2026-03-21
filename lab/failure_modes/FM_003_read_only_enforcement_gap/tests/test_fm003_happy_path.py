from failure_modes.FM_003_read_only_enforcement_gap import scenario


def test_write_tools_available_in_full_mode():
    result = scenario.run_happy_path_full_tools()

    for tool in scenario.WRITE_TOOLS:
        assert tool in result.exposed_tools
    assert result.read_only is False
