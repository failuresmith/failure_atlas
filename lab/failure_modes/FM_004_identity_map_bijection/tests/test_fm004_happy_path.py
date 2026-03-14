from failure_modes.FM_004_identity_map_bijection import scenario


def test_happy_path_fm004_unique_participants_preserve_bijection(experiment_log):
    participants = [
        scenario.Participant("alice", "tls_key_alice"),
        scenario.Participant("bob", "tls_key_bob"),
    ]

    result = scenario.run_happy_path_unique_participants(participants)

    experiment_log(
        {
            "participant_count": result.participant_count,
            "unique_participant_ids": result.unique_participant_ids,
            "unique_tls_keys": result.unique_tls_keys,
            "has_bijection": result.has_bijection,
        }
    )

    assert result.has_bijection
    assert result.registry["tls_key_alice"] == "alice"
    assert result.registry["tls_key_bob"] == "bob"
