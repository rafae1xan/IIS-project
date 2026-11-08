"""The vision path used in Lab 4.

    python vlm.py --selftest
    python vlm.py sample_images/sample_poster.png "what deadline is shown?"

Returns a structured claim with a confidence, or a refusal with a reason. The refusal is the taught
case: an image that does not answer the question, and which also contains someone else's personal data.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(HERE, "sample_images")
MODE = os.environ.get("IIS_MODEL", "mock")


def ask(image_path, question, timeout=20):
    """Return the structured teaching result for one supplied sample image."""
    name = os.path.basename(image_path)
    if MODE != "http":
        if "noticeboard" in name:
            return {"refused": True, "reason": "no deadline is visible in this image, and it shows a named person's mark, which I will not read out"}
        return {"claim": "14 November, 12:00", "confidence": 0.86, "evidence": "the sheet reads 'Due: 14 November, 12:00'"}
    raise RuntimeError("live vision route not configured: set IIS_MODEL_URL and IIS_API_KEY  [TBC]")


def render(result):
    """What the page shows. A refusal is rendered, not swallowed."""
    if result.get("refused"):
        return "I cannot answer that from this image: %s" % result.get("reason", "no reason given")
    return "%s  (confidence %.2f — %s)" % (result["claim"], result["confidence"], result["evidence"])


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        n = len([f for f in os.listdir(IMAGES) if f.endswith(".png")])
        assert ask(os.path.join(IMAGES, "sample_poster.png"), "what deadline is shown?")["claim"]
        assert ask(os.path.join(IMAGES, "sample_noticeboard.png"), "what deadline is shown?")["refused"]
        print("ok: %d sample images" % n)
        sys.exit(0)
    img = sys.argv[1] if len(sys.argv) > 1 else os.path.join(IMAGES, "sample_poster.png")
    q = sys.argv[2] if len(sys.argv) > 2 else "what deadline is shown?"
    print(render(ask(img, q)))
