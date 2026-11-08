from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).parent
OUT = Path(r"C:\Users\徐健\Documents\Codex\2026-11-06\cha\outputs")
OUT.mkdir(parents=True, exist_ok=True)
OUTPUT = OUT / "A2_One_Glance_Control_Project_Report_Final4.docx"


def set_font(run, name="Aptos", size=10.5, bold=None, italic=None, color="000000"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:ascii"), name)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), name)
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor.from_string(color)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def add_body(doc, text, indent=True):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.06
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.18)
    r = p.add_run(text)
    set_font(r)
    return p


def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(text)
    set_font(r, size=8.5, italic=True, color="536775")
    return p


def clear_template_formatting(paragraph):
    ppr = paragraph._p.get_or_add_pPr()
    for tag in ("w:numPr", "w:pBdr"):
        node = ppr.find(qn(tag))
        if node is not None:
            ppr.remove(node)


def clear_style_formatting(style):
    ppr = style._element.find(qn("w:pPr"))
    if ppr is None:
        return
    for tag in ("w:numPr", "w:pBdr"):
        node = ppr.find(qn(tag))
        if node is not None:
            ppr.remove(node)


def add_figure(doc, path, width=6.55):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(1)
    p.add_run().add_picture(str(path), width=Inches(width))


def main():
    source = (ROOT / "A2_report_content.md").read_text(encoding="utf-8")
    lines = source.splitlines()
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Inches(0.65)
    sec.bottom_margin = Inches(0.65)
    sec.left_margin = Inches(0.78)
    sec.right_margin = Inches(0.78)

    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
    normal.font.size = Pt(10.5)
    for style_name, size in (("Title", 21), ("Heading 1", 13.5), ("Heading 2", 11.5)):
        st = doc.styles[style_name]
        clear_style_formatting(st)
        st.font.name = "Aptos Display"
        st._element.rPr.rFonts.set(qn("w:ascii"), "Aptos Display")
        st._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos Display")
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = RGBColor(0, 0, 0)
        st.paragraph_format.space_before = Pt(10 if style_name != "Title" else 0)
        st.paragraph_format.space_after = Pt(4)

    in_figure_section = False
    figure_added = False
    for line in lines:
        if line.startswith("# "):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(line[2:].strip())
            set_font(r, name="Aptos Display", size=21, bold=True)
            continue
        if line.startswith("**A2 Project Report"):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(line.replace("**", ""))
            set_font(r, size=9.5, italic=True, color="536775")
            continue
        if line.startswith("## "):
            heading = line[3:].strip()
            hp = doc.add_paragraph()
            hp.paragraph_format.space_before = Pt(10)
            hp.paragraph_format.space_after = Pt(4)
            r = hp.add_run(heading)
            set_font(r, name="Aptos Display", size=13.5, bold=True)
            in_figure_section = heading == "Figures"
            continue
        if not line.strip():
            continue
        if line.startswith("**Figure"):
            continue
        if line.startswith("**") and line.endswith("**"):
            p = doc.add_paragraph()
            r = p.add_run(line.strip("*"))
            set_font(r, size=9, italic=True, color="536775")
            continue
        if line.startswith("##"):
            continue
        # Keep references compact and readable; headings/captions do not count as body prose.
        p = add_body(doc, line, indent=not line.startswith(("Clark,", "Horvitz,", "Ji,", "Kulesza,", "Lewis,", "Luger,", "Shi,", "Shneiderman,", "University of Birmingham.")))
        if line.startswith(("Clark,", "Horvitz,", "Ji,", "Kulesza,", "Lewis,", "Luger,", "Shi,", "Shneiderman,", "University of Birmingham.")):
            p.paragraph_format.left_indent = Inches(0.18)
            p.paragraph_format.first_line_indent = Inches(-0.18)

    if in_figure_section and not figure_added:
        add_figure(doc, ROOT / "assets" / "system_diagram.png")
        add_caption(doc, "Figure 1. System boundary, components and control flow.")
        add_figure(doc, ROOT / "assets" / "storyboard_normal.png")
        add_caption(doc, "Figure 2. Normal interaction: inspect, decide and receive the tool result.")
        add_figure(doc, ROOT / "assets" / "storyboard_failure.png")
        add_caption(doc, "Figure 3. Failure and recovery: stale evidence is exposed and the decision returns to the person.")

    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = footer.add_run("A2 Project Report | One-Glance Control")
    set_font(r, size=8, color="6b7b86")
    doc.core_properties.title = "One Glance Control for Action Oriented LLM Systems"
    doc.core_properties.subject = "Assignment 2 Project Report"
    doc.core_properties.author = "University of Birmingham student"
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
