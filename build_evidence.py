from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

ROOT = Path(__file__).parent
OUT = ROOT / "assets"
FONT = r"C:\Windows\Fonts\segoeui.ttf"
MONO = r"C:\Windows\Fonts\consola.ttf"


def f(path, size, bold=False):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def make_text_image(text, filename, title, subtitle, width=1800, line_height=34, mono=False):
    lines = text.splitlines()
    height = 170 + max(1, len(lines)) * line_height + 45
    im = Image.new("RGB", (width, height), "#f7f9fa")
    d = ImageDraw.Draw(im)
    d.text((70, 38), title, font=f(FONT, 36, True), fill="#17202a")
    d.text((70, 94), subtitle, font=f(FONT, 21), fill="#61707d")
    y = 155
    face = f(MONO if mono else FONT, 23)
    for line in lines:
        d.text((82, y), line, font=face, fill="#17202a")
        y += line_height
    im.save(OUT / filename)


def main():
    run_log = (ROOT / "recorded_runs" / "a2_run_log.txt").read_text(encoding="utf-8")
    make_text_image(
        run_log,
        "run_log.png",
        "Recorded A2 run evidence",
        "Self-tests and interaction checks executed against the local prototype",
        line_height=31,
        mono=True,
    )

    lines = (ROOT / "app.py").read_text(encoding="utf-8").splitlines()
    wrapped = []
    for i in range(77, 106):
        prefix = f"{i + 1:>3}  "
        chunks = textwrap.wrap(lines[i], width=106, subsequent_indent="      ") or [""]
        wrapped.append(prefix + chunks[0])
        wrapped.extend("      " + chunk for chunk in chunks[1:])
    snippet = "\n".join(wrapped)
    make_text_image(
        snippet,
        "code_snippet.png",
        "Implementation evidence from app.py",
        "Proposal is stored as pending; only the confirmed path calls tools.run",
        line_height=30,
        mono=True,
    )


if __name__ == "__main__":
    main()
