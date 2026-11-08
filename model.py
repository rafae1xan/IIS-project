"""One model call, with a mock by default.

Environment (never write these into a file):
    IIS_MODEL      "mock" (default) or "http"
    IIS_MODEL_URL  the chat-completions endpoint   [TBC: institutional endpoint]
    IIS_API_KEY    your key, if you have one
"""
import json, os, urllib.request

MODE = os.environ.get("IIS_MODEL", "mock")
ENDPOINT = os.environ.get("IIS_MODEL_URL", "")
KEY = os.environ.get("IIS_API_KEY", "")


def call(messages, schema=None, timeout=20):
    """Return the model's reply as text. Falls back to the mock whenever the live route is not configured."""
    if MODE != "http" or not (ENDPOINT and KEY):
        import mock_model
        return mock_model.call(messages, schema)
    body = {"messages": messages}
    if schema:
        body["response_format"] = {"type": "json_object"}
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        payload = json.loads(r.read().decode("utf-8"))
    return payload["choices"][0]["message"]["content"]


def call_json(messages, schema, timeout=20):
    """Return a dict, or None if the reply was not valid JSON. None is a caught error, not a crash."""
    text = call(messages, schema, timeout)
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None
