from failure_modes.FM_009_extension_authority_persistence import scenario


def test_lifecycle_bound_registry_revokes_on_uninstall():
    result = scenario.run_guarded_lifecycle_bound_registry(host="example.com")

    assert result.authority_after_uninstall is False
    # No active extensions remain
    assert result.active_extensions == set()
