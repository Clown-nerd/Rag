from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def make_pdf(path="backend/data/knowledge.pdf"):
    c = canvas.Canvas(path, pagesize=letter)
    text = c.beginText(40, 750)

    lines = [
        "Kenyan Law Firm – Legal Knowledge Base",
        "",
        "=== Filing a Civil Suit ===",
        "To file a civil suit in Kenya, prepare a plaint as per Order 2 of the",
        "Civil Procedure Rules, 2010. File the plaint in the appropriate court",
        "(Magistrate's Court for claims up to KES 20 million; High Court above",
        "that threshold). Pay the requisite filing fees at the court registry.",
        "",
        "=== Limitation Periods ===",
        "The Limitation of Actions Act (Cap 22) sets key periods:",
        "- Contract claims: 6 years from the date of breach.",
        "- Tort (personal injury): 3 years from the date of injury.",
        "- Land matters: 12 years.",
        "- Government claims: 12 months statutory notice required under the",
        "  Government Proceedings Act (Cap 40).",
        "",
        "=== Employment Disputes ===",
        "Employment disputes are governed by the Employment Act, 2007 and heard",
        "by the Employment and Labour Relations Court. An employee claiming",
        "unfair termination must file within 3 years of the termination date.",
        "",
        "=== Drafting Written Submissions ===",
        "Written submissions should include:",
        "1. A brief introduction of the parties and the case.",
        "2. A summary of the issues for determination.",
        "3. Legal arguments supported by statute and case law.",
        "4. A conclusion with the relief sought.",
        "Cite Kenyan case law (e.g. 'Giella v Cassman Brown [1973] EA 358')",
        "and relevant statutes.",
        "",
        "=== Constitutional Rights ===",
        "The Constitution of Kenya, 2010, Chapter 4 (Bill of Rights) guarantees",
        "fundamental rights including the right to fair hearing (Article 50),",
        "the right to property (Article 40), and freedom of expression",
        "(Article 33). Any person whose rights are violated may petition the",
        "High Court under Article 22.",
    ]

    for line in lines:
        text.textLine(line)

    c.drawText(text)
    c.save()

if __name__ == "__main__":
    make_pdf()