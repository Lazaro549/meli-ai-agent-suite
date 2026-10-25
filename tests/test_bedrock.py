import json

import pytest

from src.tools.bedrock_tools import BedrockClient, BedrockGenerationError


class FakeRuntime:
    def __init__(self, text):
        self.text = text
        self.kwargs = None

    def converse(self, **kwargs):
        self.kwargs = kwargs
        return {"output": {"message": {"content": [{"text": self.text}]}}}


def test_bedrock_json_is_parsed_and_schema_is_not_assumed():
    runtime = FakeRuntime('{"title":"Cable USB-C","seo_score":0.8}')
    client = BedrockClient(model_id="fake", client=runtime)
    assert client.generate_json("write")["seo_score"] == 0.8
    assert runtime.kwargs["modelId"] == "fake"


def test_invalid_json_fails_closed():
    client = BedrockClient(client=FakeRuntime("not json"))
    with pytest.raises(BedrockGenerationError):
        client.generate_json("write")
