"""One-Glance Control: a local prototype for action-oriented LLM interaction.

    python app.py            serve on 8000
    python app.py --port 8001

The prototype is deliberately offline. Retrieval, validation and the model response are all local
or mocked, so the interaction can be inspected without an API key. A tool call is never executed
until the user confirms a human-readable proposal.
"""
import json, os, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import model  # noqa: E402
import retrieve  # noqa: E402
import tools  # noqa: E402
import vlm  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = {"reply": str, "options": list, "action": (dict, type(None)), "unsupported_claims": list}
THRESHOLD = 0.25
PENDING_CALL = None


def valid(data):
    return isinstance(data, dict) and all(k in data and isinstance(data[k], t) for k, t in SCHEMA.items())


def base_result(reply, **extra):
    result = {"reply": reply, "options": [], "action": None, "unsupported_claims": [],
              "evidence": [], "stale_warning": None, "control": None}
    result.update(extra)
    return result


def fallback_turn():
    """A malformed reply is a caught error, never a blank page."""
    return base_result("I could not read the reply, so I have not changed anything. Try again or ask the module lead.",
                       recovery_notice="No action was taken because the structured response was invalid.")


def clarification_turn(candidates):
    names = " or ".join("%s on %s" % (a["clinic"], a["date"]) for a in candidates)
    return base_result("Which appointment: %s?" % names,
                       options=[a["id"] for a in candidates],
                       control={"mode": "clarification", "reason": "The request maps to more than one object."})


def decline_turn():
    return base_result("I cannot verify that clinic or your unavailable days, so I will not guess. Here are the open slots; you choose.",
                       options=["Thu 09:40", "Fri 14:10"],
                       unsupported_claims=["clinic availability beyond next week"],
                       control={"mode": "refusal", "reason": "The available context does not support the requested claim."})


def grounded_answer(question):
    """Retrieve evidence, retain provenance, and handle stale sources explicitly."""
    hits = retrieve.retrieve(question, k=3)
    relevant = [h for h in hits if h["score"] > 0]
    if not relevant or relevant[0]["score"] < THRESHOLD:
        return base_result("The supplied corpus does not give a reliable answer. Ask the module lead for anything it does not cover.",
                           control={"mode": "refusal", "reason": "No sufficiently relevant source was found."})
    top = relevant[0]
    current = next((h for h in relevant if h["section"] == top["section"] and not h["superseded"]), None)
    warning = None
    if top["superseded"]:
        if current:
            warning = "The top retrieval result is superseded. This answer uses the newer passage shown below."
        else:
            return base_result("The top result is marked superseded, and no current passage was found. Check a current source before using it.",
                               evidence=relevant, stale_warning="No current passage was found; do not rely on the old result.",
                               control={"mode": "refusal", "reason": "The only strong source is stale."})
    answer = current or top
    return base_result(answer["text"], evidence=relevant, stale_warning=warning,
                       control={"mode": "grounded", "reason": "Answer is linked to quoted passages and provenance."})


def propose_revision_slot():
    """Build a compact, inspectable action proposal without executing it."""
    global PENDING_CALL
    call = {"name": "book_slot", "arguments": {"date": "2026-11-14", "minutes": 90}}
    ok, reason = tools.valid(call)
    if not ok:
        return base_result("I rejected the proposed action before execution: %s." % reason,
                           control={"mode": "refusal", "reason": reason})
    PENDING_CALL = call
    action = {"type": "local schedule update", "object": "your local revision schedule",
              "date": call["arguments"]["date"], "minutes": call["arguments"]["minutes"],
              "reversible": "Yes - remove the local slot later", "impact": "Writes one entry to schedule.json"}
    return base_result("I prepared an action proposal. Nothing has been changed yet.",
                       action=action, tool_confirmation=tools.describe(call),
                       control={"mode": "awaiting_confirmation", "selected_object": action["object"],
                                "parameters": "14 Nov 2026; 90 minutes", "uncertainty": "Low for the local file; no external calendar is contacted.",
                                "reversible": action["reversible"]})


def confirm_tool():
    global PENDING_CALL
    if PENDING_CALL is None:
        return base_result("There is no pending action to confirm.",
                           control={"mode": "no_pending_action"})
    result = tools.run(PENDING_CALL, confirmed_by="user")
    call = PENDING_CALL
    PENDING_CALL = None
    action = {"type": "local schedule update", "object": "your local revision schedule",
              "date": call["arguments"]["date"], "minutes": call["arguments"]["minutes"],
              "reversible": "Yes - remove the local slot later", "impact": "Local file updated"}
    return base_result("The confirmed action returned this result.", action=action, tool_result=result,
                       control={"mode": "executed", "confirmed": "user", "reversible": action["reversible"]})


def cancel_tool():
    global PENDING_CALL
    PENDING_CALL = None
    return base_result("Cancelled. No action was taken.",
                       control={"mode": "cancelled", "reason": "The person kept control before execution."})


def turn(message):
    m = (message or "").lower()
    if message == "__confirm_tool__":
        return confirm_tool()
    if message == "__cancel_tool__":
        return cancel_tool()
    if message == "__propose_revision__" or "revision slot" in m or "book a revision" in m:
        return propose_revision_slot()
    if message == "__poster__":
        return base_result("The image supports this claim.", image_result=vlm.ask(os.path.join(HERE, "sample_images", "sample_poster.png"), "what deadline is shown?"),
                           control={"mode": "multimodal", "reason": "Confidence is displayed with the image claim."})
    if message == "__noticeboard__":
        return base_result("The system refused the image question.", image_result=vlm.ask(os.path.join(HERE, "sample_images", "sample_noticeboard.png"), "what deadline is shown?"),
                           control={"mode": "refusal", "reason": "The image cannot support the question and contains personal data."})
    if "achebe" in m or "next week" in m:
        return decline_turn()
    if "appointment" in m:
        return clarification_turn([{"id": "derm-14nov", "clinic": "Dermatology", "date": "14 Nov", "time": "10:20"},
                                   {"id": "physio-20nov", "clinic": "Physiotherapy", "date": "20 Nov", "time": "09:00"}])
    return grounded_answer(message)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def do_GET(self):
        with open(os.path.join(HERE, "index.html"), "rb") as f:
            self._send(200, f.read(), "text/html; charset=utf-8")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        msg = json.loads(self.rfile.read(n).decode("utf-8")).get("message", "")
        self._send(200, json.dumps(turn(msg)).encode("utf-8"))

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = 8000
    if "--port" in sys.argv:
        port = int(sys.argv[sys.argv.index("--port") + 1])
    print("serving on http://localhost:%d" % port)
    HTTPServer(("localhost", port), Handler).serve_forever()
