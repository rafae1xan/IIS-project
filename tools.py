"""One tool, with the five checks from Lecture 12 and a log.

    python tools.py --selftest

book_slot is deliberately narrow: it adds one revision slot to a local schedule file. It is enough to
practise the boundary on, and it cannot touch anything outside this folder.
"""
import json, os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "tool_log.jsonl")
SCHEDULE = os.path.join(HERE, "schedule.json")

TOOL = {"name": "book_slot",
        "description": "Add one revision slot to the local schedule. Does not contact anyone.",
        "args": {"date": "YYYY-MM-DD", "minutes": "integer 15..180"}}

NEEDS_CONFIRMATION = True   # it writes a file the user can see: not reversible without an undo


def valid(call):
    """Check 1, shape. Returns (ok, reason) so the reason can be shown to a person."""
    if not isinstance(call, dict) or call.get("name") != TOOL["name"]:
        return False, "not a book_slot call"
    a = call.get("arguments") or {}
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(a.get("date", ""))):
        return False, "date must be YYYY-MM-DD"
    try:
        m = int(a["minutes"])
    except (KeyError, TypeError, ValueError):
        return False, "minutes must be an integer"
    if not 15 <= m <= 180:
        return False, "minutes must be between 15 and 180"
    return True, ""


def describe(call):
    """What the confirmation shows: the arguments, in words, not the identifier."""
    a = call["arguments"]
    d = datetime.date.fromisoformat(a["date"])
    return "Add a %d-minute revision slot on %s?" % (int(a["minutes"]), d.strftime("%a %d %b %Y"))


def run(call, confirmed_by="user"):
    """Execute, append to the log, and return what actually happened."""
    ok, reason = valid(call)
    if not ok:
        return {"status": "refused", "reason": reason}
    slots = []
    if os.path.exists(SCHEDULE):
        with open(SCHEDULE, encoding="utf-8") as f:
            slots = json.load(f)
    a = call["arguments"]
    if any(s["date"] == a["date"] and s["minutes"] == int(a["minutes"]) for s in slots):
        result = {"status": "ok", "id": None, "note": "identical slot already present; nothing added"}
    else:
        slot = {"id": "slot_%d" % (len(slots) + 1), "date": a["date"], "minutes": int(a["minutes"])}
        slots.append(slot)
        with open(SCHEDULE, "w", encoding="utf-8") as f:
            json.dump(slots, f, indent=1)
        result = {"status": "ok", "id": slot["id"], "total_slots": len(slots)}
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": datetime.datetime.now().isoformat(timespec="minutes"),
                            "tool": call["name"], "args": a,
                            "confirmed_by": confirmed_by, "result": result}) + "\n")
    return result


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        good = {"name": "book_slot", "arguments": {"date": "2026-11-14", "minutes": 90}}
        bad = {"name": "book_slot", "arguments": {"date": "2026-11-14", "minutes": 900}}
        assert valid(good)[0] and not valid(bad)[0]
        print("ok: valid call accepted, 900-minute call refused (%s)" % valid(bad)[1])
