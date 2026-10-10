import pytest

from src.certificate_service import Participant, certificate_markdown


def test_certificate_requires_completed_viewing_time():
    completed = Participant("Ari", "Agent tooling", 45)
    assert "Ari" in certificate_markdown(completed)
    with pytest.raises(ValueError):
        certificate_markdown(Participant("Ari", "Agent tooling", 44))
