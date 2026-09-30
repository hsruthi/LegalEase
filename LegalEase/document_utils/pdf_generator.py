from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from .common import ensure_output_directory, create_filename, clean_text


def generate_pdf(title, content, output_directory="generated_documents"):
    """Generate a PDF document from the supplied title and content."""

    output_dir = ensure_output_directory(output_directory)
    filename = create_filename("LegalEase_Document", "pdf")
    file_path = Path(output_dir) / filename

    document = SimpleDocTemplate(
        str(file_path),
        pagesize=A4,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "LegalEaseTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        leading=22,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "LegalEaseHeading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=16,
        spaceBefore=10,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "LegalEaseBody",
        parent=styles["BodyText"],
        fontSize=10.5,
        leading=15,
        spaceAfter=8,
    )

    story = []

    # Title
    story.append(Paragraph(clean_text(title), title_style))
    story.append(Spacer(1, 10))

    # Content
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict):
                heading = clean_text(item.get("heading", ""))
                text = clean_text(item.get("text", ""))

                if heading:
                    story.append(Paragraph(heading, heading_style))

                if text:
                    story.append(Paragraph(text, body_style))

            else:
                text = clean_text(item)

                if text:
                    story.append(Paragraph(text, body_style))

    else:
        paragraphs = str(content).split("\n")

        for paragraph in paragraphs:
            paragraph = clean_text(paragraph)

            if paragraph:
                story.append(Paragraph(paragraph, body_style))

    document.build(story)

    return file_path