import json
from pathlib import Path


def test_sanitized_oracles_describe_confirmed_bap_acknowledgements() -> None:
    root = Path("tests/fixtures/oracles")
    stun = json.loads((root / "stun.json").read_text())
    signon = json.loads((root / "signon.json").read_text())
    content_config = json.loads((root / "content_config.json").read_text())
    bap = json.loads((root / "bap_services.json").read_text())

    assert stun["semantic_result"] == "nat_probe_reply"
    assert signon["state_after"] == "BAP_CONNECT"
    assert content_config["state_after"] == "BAP_CONNECT"
    assert [(item["request_service"], item["response_service"]) for item in bap["services"]] == [
        (121, 122), (302, 303), (304, 305), (250, 251)
    ]
