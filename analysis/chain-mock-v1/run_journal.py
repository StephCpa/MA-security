"""Single-writer durable invocation journal. No network or credentials here."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


class Journal:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.events = []
        self.states = {}
        if self.path.exists():
            with self.path.open(encoding="utf-8") as stream:
                for line in stream:
                    event = json.loads(line)  # a partial tail stops recovery
                    if event["seq"] != len(self.events):
                        raise ValueError("non-contiguous journal")
                    self._transition(event)
                    self.events.append(event)

    def _transition(self, event):
        key, kind = event["call_id"], event["kind"]
        if kind == "request":
            if key in self.states:
                raise ValueError("duplicate call id")
            retry = event["data"].get("retry_of")
            if retry is not None and self.states.get(retry) != "error":
                raise ValueError("only a recorded transport error permits explicit retry")
            self.states[key] = "pending"
        elif kind in ("response", "error"):
            if self.states.get(key) != "pending":
                raise ValueError("completion without one pending request")
            self.states[key] = kind
        else:
            raise ValueError("unknown journal event")

    def append(self, kind, call_id, data):
        event = {"seq": len(self.events), "utc": datetime.now(timezone.utc).isoformat(),
                 "kind": kind, "call_id": call_id, "data": data}
        wire = json.dumps(event, ensure_ascii=False, allow_nan=False) + "\n"
        previous = self.states.copy()
        self._transition(event)
        try:
            with self.path.open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(wire)
                stream.flush()
                os.fsync(stream.fileno())
        except Exception:
            self.states = previous
            raise
        self.events.append(event)

    def invoke(self, call_id, stage, request, transport, *, identity, retry_of=None):
        """Persist before invoking injected transport; never retry automatically.

        Transport returns (HTTP status, response body string). Transport exception
        messages are not archived because they may embed credentials. A new
        process must not assume a pending call was never sent.
        """
        allowed = {"model", "messages", "temperature", "enable_thinking",
                   "max_tokens", "stream", "tools", "tool_choice", "thinking"}
        if not isinstance(request, dict) or set(request) - allowed:
            raise ValueError("request contains unsupported fields, possibly headers")
        id_keys = {"directive_id", "arm", "attack_variant", "repeat_id", "branch_id"}
        if not isinstance(identity, dict) or set(identity) != id_keys:
            raise ValueError("complete experimental identity required")
        self.append("request", call_id, {"stage": stage, "identity": identity,
                                         "request": request, "retry_of": retry_of})
        try:
            status, body = transport(request)
            if not isinstance(status, int) or not isinstance(body, str):
                raise TypeError("transport must return status and body text")
        except Exception as exc:
            self.append("error", call_id, {"error_type": type(exc).__name__})
            return {"HttpStatus": None, "Response": None, "ErrorType": type(exc).__name__}
        # Body is archived before JSON decoding, preserving malformed responses.
        self.append("response", call_id, {"http_status": status, "body_text": body})
        try:
            response = json.loads(body)
        except (ValueError, TypeError):
            response = None
        return {"HttpStatus": status, "Response": response, "Request": request}
