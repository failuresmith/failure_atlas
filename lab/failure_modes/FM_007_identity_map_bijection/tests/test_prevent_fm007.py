import pytest

from failure_modes.FM_007_identity_map_bijection import scenario


def test_bijection_validation_rejects_duplicates(experiment_log):
    participants = [
        scenario.Participant("alice", "tls_key_shared"),
        scenario.Participant("bob", "tls_key_shared"),
    ]

    with pytest.raises(ValueError):
        scenario.run_guarded_with_bijection_enforcement(participants)

    experiment_log(
        {
            "participant_ids": [p.participant_id for p in participants],
            "tls_keys": [p.tls_key for p in participants],
            "expected": "ValueError",
        }
    )
