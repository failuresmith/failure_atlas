from failure_modes.FM_007_identity_map_bijection import scenario


def test_duplicate_tls_key_overwrites_prior_mapping(experiment_log):
    participants = [
        scenario.Participant("alice", "tls_key_shared"),
        scenario.Participant("bob", "tls_key_shared"),
    ]

    result = scenario.run_known_broken_baseline(participants)

    experiment_log(
        {
            "participant_count": result.participant_count,
            "unique_participant_ids": result.unique_participant_ids,
            "unique_tls_keys": result.unique_tls_keys,
            "has_bijection": result.has_bijection,
            "duplicate_tls_keys": result.duplicate_tls_keys,
        }
    )

    assert len(result.registry) == 1
    assert result.registry["tls_key_shared"] == "bob"
    assert not result.has_bijection
