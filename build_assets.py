from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)
FONT = r"C:\Windows\Fonts\segoeui.ttf"
FONT_B = r"C:\Windows\Fonts\segoeuib.ttf"


def font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_B if bold else FONT, size)
    except OSError:
        return ImageFont.load_default()


def text(draw, xy, value, size=24, fill="#17202a", bold=False, anchor=None):
    draw.text(xy, value, font=font(size, bold), fill=fill, anchor=anchor, spacing=6)


def box(draw, xy, fill, outline="#c9d7df", radius=22, width=3):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw, start, end, fill="#0b4f71", width=5):
    draw.line([start, end], fill=fill, width=width)
    x1, y1 = start
    x2, y2 = end
    if abs(x2 - x1) >= abs(y2 - y1):
        s = -1 if x2 < x1 else 1
        draw.polygon([(x2, y2), (x2 - s * 18, y2 - 10), (x2 - s * 18, y2 + 10)], fill=fill)
    else:
        s = -1 if y2 < y1 else 1
        draw.polygon([(x2, y2), (x2 - 10, y2 - s * 18), (x2 + 10, y2 - s * 18)], fill=fill)


def path_arrow(draw, points, fill="#607b8c", width=5):
    """Draw a routed connector with an arrowhead at its final point."""
    draw.line(points, fill=fill, width=width, joint="curve")
    x1, y1 = points[-2]
    x2, y2 = points[-1]
    if abs(x2 - x1) >= abs(y2 - y1):
        s = -1 if x2 < x1 else 1
        draw.polygon([(x2, y2), (x2 - s * 18, y2 - 10), (x2 - s * 18, y2 + 10)], fill=fill)
    else:
        s = -1 if y2 < y1 else 1
        draw.polygon([(x2, y2), (x2 - 10, y2 - s * 18), (x2 + 10, y2 - s * 18)], fill=fill)


def system_diagram():
    im = Image.new("RGB", (1800, 1050), "#f7f9fa")
    d = ImageDraw.Draw(im)
    text(d, (90, 60), "One-Glance Control system boundary", 42, bold=True)
    text(d, (90, 122), "Implemented local prototype; model and external services are simulated or deliberately out of scope", 22, fill="#61707d")
    # left to right path
    nodes = [
        ((90, 300, 370, 480), "Person", "asks a question\nor requests an action", "#e8f0f7"),
        ((500, 300, 790, 480), "Context and retrieval", "local corpus\nquoted evidence + provenance", "#e3f2ec"),
        ((920, 300, 1210, 480), "Model proposal", "mock structured reply\nclaim, parameters, uncertainty", "#f7eedb"),
        ((1340, 215, 1690, 385), "Control panel", "object + parameters\nimpact + reversibility", "#dff1ea"),
        ((1340, 425, 1690, 595), "Validation gate", "shape + range + scope\ninvalid calls refused", "#fff0ee"),
        ((1340, 635, 1690, 805), "User decision", "Confirm / Cancel\nclarify / correct", "#e8f0f7"),
        ((920, 680, 1210, 850), "Local tool", "writes schedule.json\nlogs result", "#e3f2ec"),
    ]
    for xy, title, body, fill in nodes:
        box(d, xy, fill)
        x1, y1, x2, y2 = xy
        text(d, ((x1 + x2) // 2, y1 + 42), title, 25, bold=True, anchor="mm")
        text(d, ((x1 + x2) // 2, y1 + 102), body, 20, fill="#40515c", anchor="mm")
    arrow(d, (370, 390), (500, 390))
    arrow(d, (790, 390), (920, 390))
    arrow(d, (1210, 350), (1340, 300))
    arrow(d, (1515, 385), (1515, 425))
    arrow(d, (1515, 595), (1515, 635))
    arrow(d, (1340, 720), (1210, 765))
    # Route feedback around the legend and back into the Person node. The
    # previous diagonal ended in empty space, so it did not show a real loop.
    path_arrow(d, [(920, 765), (850, 765), (850, 965), (55, 965), (55, 390), (90, 390)])
    text(d, (920, 925), "feedback, refusal or result returns to the person", 22, fill="#61707d")
    # legend
    box(d, (90, 680, 790, 900), "#ffffff", outline="#d8e0e6", radius=18, width=2)
    text(d, (120, 715), "Scope labels", 23, bold=True)
    text(d, (120, 765), "Implemented", 20, fill="#176b4d", bold=True)
    text(d, (320, 765), "retrieval, provenance, validation, confirmation, logging", 19)
    text(d, (120, 810), "Simulated", 20, fill="#9b6700", bold=True)
    text(d, (320, 810), "mock model, local corpus, local schedule tool", 19)
    text(d, (120, 855), "Planned", 20, fill="#7a4f8b", bold=True)
    text(d, (320, 855), "live calendar connector and user study", 19)
    im.save(OUT / "system_diagram.png")


def storyboard(title, subtitle, frames, filename):
    im = Image.new("RGB", (1800, 850), "#f7f9fa")
    d = ImageDraw.Draw(im)
    text(d, (80, 45), title, 38, bold=True)
    text(d, (80, 100), subtitle, 21, fill="#61707d")
    left = 80
    top = 200
    w = 370
    gap = 28
    for i, (head, person, system, accent) in enumerate(frames):
        x = left + i * (w + gap)
        box(d, (x, top, x + w, top + 510), "#ffffff", outline="#cfdbe2", radius=18, width=3)
        text(d, (x + 22, top + 24), f"Frame {i+1}", 20, fill="#61707d", bold=True)
        text(d, (x + 22, top + 70), head, 26, bold=True)
        box(d, (x + 22, top + 145, x + w - 22, top + 270), "#e8f0f7", outline="#bed1df", radius=14, width=2)
        text(d, (x + 40, top + 165), "Person", 17, fill="#0b4f71", bold=True)
        text(d, (x + 40, top + 205), person, 19, fill="#33434d")
        box(d, (x + 22, top + 300, x + w - 22, top + 425), accent, outline="#c8ddd5", radius=14, width=2)
        text(d, (x + 40, top + 320), "System", 17, fill="#176b4d", bold=True)
        text(d, (x + 40, top + 360), system, 19, fill="#33434d")
        if i < len(frames) - 1:
            arrow(d, (x + w + 5, top + 255), (x + w + gap - 5, top + 255), fill="#607b8c", width=4)
    im.save(OUT / filename)


system_diagram()
storyboard(
    "Normal interaction storyboard",
    "The user can inspect the evidence-to-action chain before confirming a local schedule change.",
    [
        ("1. Request", "Type: book a revision slot", "Recognises the request;\nno file change yet.", "#e3f2ec"),
        ("2. Inspect", "Read the selected object\nand 90-minute parameter", "Shows evidence, impact\nand reversibility in one glance.", "#dff1ea"),
        ("3. Decide", "Select Confirm", "Validation passes;\nthe decision is explicit.", "#f7eedb"),
        ("4. Result", "Continue with the\nrevised plan", "Tool writes one local slot\nand reports the result.", "#e3f2ec"),
    ],
    "storyboard_normal.png",
)
storyboard(
    "Failure and recovery storyboard",
    "A stale source or ambiguous request becomes visible and repairable instead of silently producing an action.",
    [
        ("1. Risk", "Ask: what is the\nlate-submission penalty?", "Retriever ranks an older\nhandbook first.", "#fff3d6"),
        ("2. Notice", "See SUPERSEDED warning\nand both dates", "Uses the newer passage\nand labels the old one.", "#fff3d6"),
        ("3. Repair", "Ask the module lead\nif still unsure", "Refuses unsupported claims;\ndoes not guess or execute.", "#fff0ee"),
        ("4. Control", "Keep, correct or\ncancel the next action", "Returns the decision to the\nperson with a clear reason.", "#e8f0f7"),
    ],
    "storyboard_failure.png",
)
