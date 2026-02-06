"""
Generate a sample PDF using ReportLab for correctness.

This replaces the previous hand-rolled PDF writer which produced
files that some PDF parsers (like pypdf) could not read.

Requires `reportlab` (already listed in `requirements.txt`).
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


def create_pdf(path, text):
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter
    textobject = c.beginText(72, height - 72)
    textobject.setFont("Helvetica", 12)
    for line in text.splitlines():
        textobject.textLine(line)
    c.drawText(textobject)
    c.showPage()
    c.save()


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "knowledge.pdf")
    text = (
        "Sample knowledge base PDF for the demo.\n\n"
        "This PDF provides a few sentences about the product, policies, and support contact.\n"
        "Use /ingest endpoint to index this content and then /chat to query."
    )
    create_pdf(out, text)
    print(f"Wrote sample PDF to: {out}")
