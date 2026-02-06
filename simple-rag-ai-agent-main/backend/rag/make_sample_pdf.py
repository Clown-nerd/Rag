from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def make_pdf(path="backend/data/knowledge.pdf"):
    c = canvas.Canvas(path, pagesize=letter)
    text = c.beginText(40, 750)

    lines = [
        "Insurance Agency Customer Care Knowledge Base",
        "",
        "Q: How do I file a claim?",
        "A: Call our claims line or submit through the portal.",
        "",
        "Q: What is a deductible?",
        "A: The amount you pay before insurance starts paying."
    ]

    for line in lines:
        text.textLine(line)

    c.drawText(text)
    c.save()

if __name__ == "__main__":
    make_pdf()