"""Generate a one-page Europass-style CV and a cover letter for Hafiz Qasim Ali."""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepInFrame,
)
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY

EUROPASS_BLUE = colors.HexColor("#003399")
EUROPASS_LIGHT = colors.HexColor("#E6ECF5")
EUROPASS_DARK = colors.HexColor("#1A1A1A")
GREY = colors.HexColor("#555555")

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_MARGIN = 1.4 * cm
RIGHT_MARGIN = 1.2 * cm
TOP_MARGIN = 1.2 * cm
BOTTOM_MARGIN = 1.0 * cm

LABEL_W = 4.7 * cm
CONTENT_W = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN - LABEL_W - 0.3 * cm


def styles():
    base = ParagraphStyle(
        "base",
        fontName="Helvetica",
        fontSize=9,
        leading=11.5,
        textColor=EUROPASS_DARK,
    )
    return {
        "name": ParagraphStyle(
            "name", parent=base, fontName="Helvetica-Bold",
            fontSize=18, leading=21, textColor=EUROPASS_BLUE,
        ),
        "title": ParagraphStyle(
            "title", parent=base, fontSize=11, leading=13,
            textColor=GREY, spaceAfter=2,
        ),
        "contact": ParagraphStyle(
            "contact", parent=base, fontSize=9, leading=12, textColor=EUROPASS_DARK,
        ),
        "section": ParagraphStyle(
            "section", parent=base, fontName="Helvetica-Bold",
            fontSize=10.5, leading=12, textColor=colors.white,
            backColor=EUROPASS_BLUE, leftIndent=4, rightIndent=4,
            spaceBefore=0, spaceAfter=0,
            borderPadding=(3, 4, 3, 4),
        ),
        "label": ParagraphStyle(
            "label", parent=base, fontName="Helvetica-Bold",
            fontSize=9, leading=11, textColor=EUROPASS_BLUE, alignment=TA_LEFT,
        ),
        "body": ParagraphStyle(
            "body", parent=base, fontSize=9, leading=11.5, alignment=TA_JUSTIFY,
        ),
        "small": ParagraphStyle(
            "small", parent=base, fontSize=8.5, leading=10.5, textColor=GREY,
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=base, fontSize=9, leading=11.2,
            leftIndent=10, bulletIndent=0,
        ),
        "role": ParagraphStyle(
            "role", parent=base, fontName="Helvetica-Bold",
            fontSize=9.5, leading=11.5, textColor=EUROPASS_DARK,
        ),
        "dates": ParagraphStyle(
            "dates", parent=base, fontSize=9, leading=11.5,
            textColor=GREY, fontName="Helvetica-Oblique",
        ),
    }


def section_bar(title):
    t = Table(
        [[Paragraph(title.upper(), styles()["section"])]],
        colWidths=[PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), EUROPASS_BLUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def row(label, content_flowables):
    s = styles()
    label_p = Paragraph(label, s["label"])
    if not isinstance(content_flowables, list):
        content_flowables = [content_flowables]
    t = Table(
        [[label_p, content_flowables]],
        colWidths=[LABEL_W, CONTENT_W],
    )
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#CCCCCC")),
    ]))
    return t


def build_cv(path):
    s = styles()
    doc = BaseDocTemplate(
        path,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title="Hafiz Qasim Ali - Europass CV",
        author="Hafiz Qasim Ali",
    )
    frame = Frame(
        LEFT_MARGIN, BOTTOM_MARGIN,
        PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN,
        PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
        showBoundary=0,
    )
    doc.addPageTemplates([PageTemplate(id="cv", frames=[frame])])

    story = []

    header_left = [
        Paragraph("Hafiz Qasim Ali", s["name"]),
        Paragraph("Lead Flutter Developer | Mobile, Web &amp; Desktop", s["title"]),
    ]
    header_right = [
        Paragraph(
            "<b>Email:</b> h.qasimali007@gmail.com<br/>"
            "<b>Phone:</b> +971 50 289 6128<br/>"
            "<b>Address:</b> Ajman, United Arab Emirates<br/>"
            "<b>Nationality:</b> Pakistani",
            s["contact"],
        ),
    ]
    header = Table(
        [[header_left, header_right]],
        colWidths=[(PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN) * 0.55,
                   (PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN) * 0.45],
    )
    header.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(header)
    story.append(Spacer(1, 2))

    story.append(section_bar("Personal Information"))
    story.append(row("Position applied for", Paragraph(
        "Lead / Senior Flutter Developer", s["body"])))
    story.append(row("Languages", Paragraph(
        "English (Professional) &nbsp;|&nbsp; Urdu (Native) &nbsp;|&nbsp; Punjabi (Native)",
        s["body"])))

    story.append(Spacer(1, 4))
    story.append(section_bar("Professional Profile"))
    story.append(row("About me", Paragraph(
        "Lead Flutter Developer with <b>8+ years</b> of software development experience "
        "and a strong background in cross-platform mobile architecture, system design "
        "and team leadership. Expert in building scalable Flutter applications for "
        "Android, iOS, Web and Desktop, with hands-on experience designing "
        "Python-based backend services and RESTful APIs. Proven ability to own "
        "end-to-end products, mentor developers and deliver reliable, "
        "high-performance systems for e-commerce, POS, logistics and enterprise apps.",
        s["body"])))

    story.append(Spacer(1, 4))
    story.append(section_bar("Work Experience"))

    story.append(row("Oct 2021 – Present", [
        Paragraph("Lead / Senior Flutter Developer &amp; Tech Lead", s["role"]),
        Paragraph("IKLIX — Dubai, UAE", s["dates"]),
        Paragraph(
            "• Led architecture and development of Flutter apps across mobile, web and desktop.<br/>"
            "• Owned full e-commerce ecosystem: POS, delivery, dashboards and inventory.<br/>"
            "• Built and maintained Python backend services and RESTful APIs.<br/>"
            "• Integrated Apple Pay, Stripe and third-party SDKs; Odoo integration with Klix App for sales.<br/>"
            "• Conducted code reviews, mentored the team and improved release stability and performance.",
            s["bullet"]),
    ]))

    story.append(row("Sep 2018 – Aug 2021", [
        Paragraph("Technical Developer", s["role"]),
        Paragraph("Massar — Dubai, UAE", s["dates"]),
        Paragraph(
            "• Built iOS and Android apps using NativeScript (Angular / TypeScript).<br/>"
            "• Published apps to Google Play and the App Store; integrated native plugins and REST APIs.",
            s["bullet"]),
    ]))

    story.append(row("Dec 2015 – Mar 2017", [
        Paragraph("Android Developer", s["role"]),
        Paragraph("Al-Hafiz Design Center &amp; Jolta Technology — Pakistan", s["dates"]),
        Paragraph(
            "• Developed native and hybrid Android applications and integrated REST APIs.<br/>"
            "• Worked on Arduino-based home automation; enhanced several production apps.",
            s["bullet"]),
    ]))

    story.append(Spacer(1, 4))
    story.append(section_bar("Education & Training"))
    story.append(row("2011 – 2015", [
        Paragraph("Bachelor of Software Engineering", s["role"]),
        Paragraph("GC University Faisalabad — Pakistan", s["dates"]),
    ]))

    story.append(Spacer(1, 4))
    story.append(section_bar("Skills"))
    story.append(row("Core skills", Paragraph(
        "Flutter Architecture &amp; State Management • Cross-Platform Development "
        "(Mobile, Web, Desktop) • Technical Leadership &amp; Code Reviews • "
        "RESTful API Design &amp; Integration • Payment Gateway Integration "
        "(Apple Pay, Stripe) • Database Design &amp; Optimization • Performance "
        "Optimization &amp; Scalability • Mentoring &amp; Team Collaboration",
        s["body"])))
    story.append(row("Mobile &amp; Frontend", Paragraph(
        "Flutter (Android, iOS, Web, Desktop) • Android SDK (Java, XML) • "
        "React Native • NativeScript (Angular, TypeScript) • HTML, CSS, TypeScript",
        s["body"])))
    story.append(row("Backend &amp; Data", Paragraph(
        "Python (API development, business logic, integrations) • RESTful APIs • "
        "Firebase • Third-party API &amp; plugin integration • SQLite • MongoDB",
        s["body"])))
    story.append(row("Tools &amp; Platforms", Paragraph(
        "Android Studio • Git &amp; Version Control • Payment SDKs (Apple Pay, Stripe) • "
        "Push Notifications • Maps &amp; Geolocation",
        s["body"])))

    fitted = KeepInFrame(
        PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN,
        PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN,
        story,
        mode="shrink",
    )
    doc.build([fitted])


def build_cover_letter(path):
    s = styles()
    doc = BaseDocTemplate(
        path,
        pagesize=A4,
        leftMargin=2.0 * cm,
        rightMargin=2.0 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="Hafiz Qasim Ali - Cover Letter",
        author="Hafiz Qasim Ali",
    )
    frame = Frame(
        2.0 * cm, 1.8 * cm,
        PAGE_WIDTH - 4.0 * cm,
        PAGE_HEIGHT - 3.6 * cm,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    doc.addPageTemplates([PageTemplate(id="cover", frames=[frame])])

    body = ParagraphStyle(
        "cb", fontName="Helvetica", fontSize=11,
        leading=15, alignment=TA_JUSTIFY, textColor=EUROPASS_DARK,
    )
    name = ParagraphStyle(
        "cn", fontName="Helvetica-Bold", fontSize=16,
        leading=19, textColor=EUROPASS_BLUE,
    )
    sub = ParagraphStyle(
        "cs", fontName="Helvetica", fontSize=10.5,
        leading=13, textColor=GREY,
    )
    contact = ParagraphStyle(
        "cc", fontName="Helvetica", fontSize=9.5,
        leading=12, textColor=EUROPASS_DARK,
    )

    story = []
    story.append(Paragraph("Hafiz Qasim Ali", name))
    story.append(Paragraph("Lead Flutter Developer", sub))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Ajman, United Arab Emirates &nbsp;•&nbsp; "
        "h.qasimali007@gmail.com &nbsp;•&nbsp; +971 50 289 6128",
        contact))
    story.append(Spacer(1, 14))

    story.append(Paragraph("12 May 2026", body))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Dear Hiring Manager,", body))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "I am writing to express my interest in the <b>Lead / Senior Flutter "
        "Developer</b> position within your organisation. With over <b>eight years "
        "of software development experience</b> and a track record of leading "
        "cross-platform projects from architecture to release, I am confident "
        "I can deliver immediate value to your team.",
        body))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "As Lead Flutter Developer &amp; Tech Lead at <b>IKLIX (Dubai)</b>, "
        "I have owned the architecture and delivery of a complete e-commerce "
        "ecosystem — POS, delivery, dashboards and inventory — across mobile, "
        "web and desktop. I designed and maintained Python-based backend services "
        "and RESTful APIs, integrated payment gateways such as <b>Apple Pay</b> "
        "and <b>Stripe</b>, connected Odoo with the Klix application for sales "
        "operations, and continuously improved release stability, scalability "
        "and performance. Alongside hands-on engineering, I run code reviews, "
        "mentor developers and enforce engineering best practices.",
        body))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Earlier roles at <b>Massar (Dubai)</b> and in Pakistan strengthened my "
        "foundations in native Android, NativeScript and hybrid development, "
        "including publishing apps to the App Store and Google Play and "
        "integrating native plugins, REST APIs and IoT components. I hold a "
        "<b>Bachelor of Software Engineering</b> from GC University Faisalabad.",
        body))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "What I bring to your team is a rare combination of <b>deep Flutter "
        "expertise</b>, <b>backend pragmatism in Python</b> and <b>technical "
        "leadership</b> — the ability to take a product from idea, to "
        "architecture, to a reliable production release while growing the "
        "engineers around me. I would welcome the opportunity to discuss how "
        "my experience can support your roadmap.",
        body))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Thank you for considering my application. I look forward to hearing "
        "from you.",
        body))
    story.append(Spacer(1, 16))

    story.append(Paragraph("Sincerely,", body))
    story.append(Spacer(1, 18))
    story.append(Paragraph("<b>Hafiz Qasim Ali</b>", body))

    doc.build(story)


if __name__ == "__main__":
    import os
    out_dir = os.path.dirname(os.path.abspath(__file__))
    build_cv(os.path.join(out_dir, "Hafiz_Qasim_Ali_Europass_CV.pdf"))
    build_cover_letter(os.path.join(out_dir, "Hafiz_Qasim_Ali_Cover_Letter.pdf"))
    print("Generated CV and cover letter in", out_dir)
