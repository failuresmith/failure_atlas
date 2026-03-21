from failure_modes.FM_002_extension_authority_persistence import scenario


def test_active_extension_retains_authority():
    result = scenario.run_happy_path_active_extension(host="example.com")

    assert result.authority_after_uninstall is True
    assert result.active_extensions == {"ext-1"}
