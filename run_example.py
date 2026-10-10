import json

from src.certificate_service import InfraiClient, Participant


if __name__ == "__main__":
    participant = Participant("Mina Chen", "RAG for Streamers", 62)
    result = InfraiClient().generate_certificate(participant)
    print(json.dumps(result, indent=2))
