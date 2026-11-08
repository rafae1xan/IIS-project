"""The finished wiring (staff reference): the three additions this lab makes to the Lab 3 prototype.

Copy the marked blocks into your own app.py. Run this file to see the whole path once, offline:

    python wiring.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import retrieve, tools, vlm  # noqa: E402

THRESHOLD = 0.25   # chosen by hand for this corpus; justify yours in the test record


# ---- addition 1: print what you actually send -------------------------------------------------
def log_context(parts):
    total = sum(len(p["text"].split()) for p in parts)
    print("%d parts, ~%d words" % (len(parts), total))
    for p in parts:
        print("  %-22s %5d  (%2d%%)" % (p["name"], len(p["text"].split()),
                                        100 * len(p["text"].split()) // max(total, 1)))


# ---- addition 2: retrieval with provenance ----------------------------------------------------
def answer(question):
    hits = retrieve.retrieve(question, k=3)
    relevant = [h for h in hits if h["score"] > 0]
    parts = [{"name": "instructions", "text": "You are a module assistant. Answer only from the passages."},
             {"name": "retrieved passages", "text": retrieve.format_passages(relevant)},
             {"name": "the question", "text": question}]
    log_context(parts)
    if not relevant or relevant[0]["score"] < THRESHOLD:
        return {"reply": "The corpus does not give a reliable answer. Ask the module lead for anything it does not cover.",
                "hits": relevant, "grounded": False, "stale_warning": None}
    top = relevant[0]
    current = next((h for h in relevant
                    if h["section"] == top["section"] and not h["superseded"]), None)
    warning = None
    if top["superseded"]:
        if current:
            warning = "The top retrieval result is superseded. This answer uses the newer passage shown below."
        else:
            return {"reply": "The top result is marked superseded, and no current passage was found. Check a current source before using it.",
                    "hits": relevant, "grounded": False,
                    "stale_warning": "No current passage was found; do not rely on the old result."}
    return {"reply": (current or top)["text"], "hits": relevant,
            "grounded": True, "stale_warning": warning}


def show(result):
    """The provenance display: the quoted sentence, its source, its date and its score."""
    print("\n" + result["reply"])
    if result["stale_warning"]:
        print("  WARNING: " + result["stale_warning"])
    count = 3 if result["stale_warning"] else (1 if result["grounded"] else 2)
    for h in result["hits"][:count]:
        status = "SUPERSEDED | " if h["superseded"] else ""
        print('  [%s%s | %s | updated %s | score %.2f]' % (status, h["source"], h["section"], h["date"], h["score"]))
        print('  "%s"' % h["text"])


# ---- addition 3: the tool, gated -------------------------------------------------------------
def propose_and_run(call, confirmed):
    ok, reason = tools.valid(call)
    if not ok:
        return {"status": "refused", "reason": reason}          # check 1: nothing ran
    if tools.NEEDS_CONFIRMATION and not confirmed:
        return {"status": "awaiting_confirmation", "ask": tools.describe(call)}   # check 4
    return tools.run(call, confirmed_by="user")


if __name__ == "__main__":
    for q in ["When is coursework 1 due?", "What is the late-submission penalty?",
              "Can I use an AI assistant for the project?"]:
        print("\n=== " + q)
        show(answer(q))
    print("\n=== an invalid tool call")
    print(propose_and_run({"name": "book_slot", "arguments": {"date": "2026-11-14", "minutes": 900}}, False))
    print("=== a valid one, before confirmation")
    print(propose_and_run({"name": "book_slot", "arguments": {"date": "2026-11-14", "minutes": 90}}, False))
    print("=== the image path")
    print(vlm.render(vlm.ask("sample_images/sample_poster.png", "what deadline is shown?")))
    print(vlm.render(vlm.ask("sample_images/sample_noticeboard.png", "what deadline is shown?")))
