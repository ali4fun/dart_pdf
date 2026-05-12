"""
Generate Europass-style CV and Cover Letter for Hafiz Qasim Ali
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ── Europass colour palette ──────────────────────────────────────────────────
EURO_BLUE      = colors.HexColor("#003399")   # header / headings
EURO_LIGHT     = colors.HexColor("#E8EEF7")   # left-column background
EURO_LINE      = colors.HexColor("#003399")   # dividers
EURO_DARK      = colors.HexColor("#1A1A1A")   # body text
EURO_GREY      = colors.HexColor("#555555")   # secondary text
WHITE          = colors.white

PAGE_W, PAGE_H = A4
MARGIN_L = 18 * mm
MARGIN_R = 14 * mm
MARGIN_T = 14 * mm
MARGIN_B = 12 * mm

LEFT_COL  = 55 * mm
GUTTER    = 4  * mm
RIGHT_COL = PAGE_W - MARGIN_L - MARGIN_R - LEFT_COL - GUTTER


# ── Styles ───────────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()

    def ps(name, **kw):
        return ParagraphStyle(name, **kw)

    name_style = ps(
        "Name",
        fontName="Helvetica-Bold", fontSize=17, textColor=WHITE,
        leading=20, spaceAfter=0, spaceBefore=0,
    )
    title_style = ps(
        "Title",
        fontName="Helvetica", fontSize=10, textColor=colors.HexColor("#CCE0FF"),
        leading=13, spaceAfter=0,
    )
    section_heading = ps(
        "SectionHeading",
        fontName="Helvetica-Bold", fontSize=8.5, textColor=EURO_BLUE,
        leading=11, spaceBefore=5, spaceAfter=1, textTransform="uppercase",
    )
    left_label = ps(
        "LeftLabel",
        fontName="Helvetica-Bold", fontSize=7.5, textColor=WHITE,
        leading=10, spaceAfter=1,
    )
    left_value = ps(
        "LeftValue",
        fontName="Helvetica", fontSize=7.5, textColor=colors.HexColor("#DCE8FF"),
        leading=10, spaceAfter=3,
    )
    body = ps(
        "Body",
        fontName="Helvetica", fontSize=7.8, textColor=EURO_DARK,
        leading=11, spaceAfter=2,
    )
    bullet_item = ps(
        "BulletItem",
        fontName="Helvetica", fontSize=7.5, textColor=EURO_DARK,
        leading=10.5, leftIndent=8, firstLineIndent=-6, spaceAfter=1,
    )
    job_title = ps(
        "JobTitle",
        fontName="Helvetica-Bold", fontSize=8, textColor=EURO_DARK,
        leading=11, spaceAfter=0,
    )
    job_org = ps(
        "JobOrg",
        fontName="Helvetica-Oblique", fontSize=7.5, textColor=EURO_GREY,
        leading=10, spaceAfter=1,
    )
    summary = ps(
        "Summary",
        fontName="Helvetica", fontSize=7.8, textColor=EURO_DARK,
        leading=11.5, spaceAfter=2, alignment=TA_JUSTIFY,
    )
    skill_tag = ps(
        "SkillTag",
        fontName="Helvetica", fontSize=7.3, textColor=EURO_DARK,
        leading=10, spaceAfter=1,
    )
    edu_title = ps(
        "EduTitle",
        fontName="Helvetica-Bold", fontSize=8, textColor=EURO_DARK,
        leading=11, spaceAfter=0,
    )
    edu_sub = ps(
        "EduSub",
        fontName="Helvetica-Oblique", fontSize=7.5, textColor=EURO_GREY,
        leading=10, spaceAfter=1,
    )
    lang_item = ps(
        "LangItem",
        fontName="Helvetica", fontSize=7.5, textColor=EURO_DARK,
        leading=10, spaceAfter=1,
    )
    return dict(
        name=name_style, title=title_style, section=section_heading,
        left_label=left_label, left_value=left_value,
        body=body, bullet=bullet_item, job_title=job_title, job_org=job_org,
        summary=summary, skill_tag=skill_tag, edu_title=edu_title,
        edu_sub=edu_sub, lang=lang_item,
    )


# ── Helpers ──────────────────────────────────────────────────────────────────
def hr(color=EURO_LINE, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceAfter=2, spaceBefore=2)


def section_title(text, styles):
    return [Paragraph(text.upper(), styles["section"]), hr()]


def bullet(text, styles):
    return Paragraph(f"• &nbsp;{text}", styles["bullet"])


# ── Left column ──────────────────────────────────────────────────────────────
def build_left_col(styles):
    items = []

    def label(t):
        items.append(Paragraph(t, styles["left_label"]))

    def value(t):
        items.append(Paragraph(t, styles["left_value"]))

    def gap(h=3):
        items.append(Spacer(1, h))

    # Contact
    label("LOCATION")
    value("Ajman, UAE")
    gap()
    label("EMAIL")
    value("h.qasimali007@gmail.com")
    gap()
    label("PHONE")
    value("+971 50 289 6128")
    gap(5)

    # Divider
    items.append(HRFlowable(width="100%", thickness=0.4,
                             color=colors.HexColor("#5577BB"),
                             spaceAfter=4, spaceBefore=2))

    # Technical Skills
    label("MOBILE & FRONTEND")
    for s in ["Flutter (Android, iOS, Web, Desktop)",
              "Android SDK (Java, XML)",
              "React Native",
              "NativeScript (Angular/TS)",
              "HTML · CSS · TypeScript"]:
        value(s)
    gap(4)

    label("BACKEND")
    for s in ["Python (APIs, integrations)", "RESTful APIs", "Firebase"]:
        value(s)
    gap(4)

    label("DATABASES")
    for s in ["SQLite", "MongoDB"]:
        value(s)
    gap(4)

    label("TOOLS & PLATFORMS")
    for s in ["Android Studio", "Git & Version Control",
              "Apple Pay · Stripe SDKs",
              "Push Notifications",
              "Maps & Geolocation",
              "Odoo Integration"]:
        value(s)
    gap(5)

    items.append(HRFlowable(width="100%", thickness=0.4,
                             color=colors.HexColor("#5577BB"),
                             spaceAfter=4, spaceBefore=2))

    # Languages
    label("LANGUAGES")
    for lang, lvl in [("English", "Professional"),
                      ("Urdu",    "Native"),
                      ("Punjabi", "Native")]:
        value(f"{lang}  –  {lvl}")

    return items


# ── Right column ─────────────────────────────────────────────────────────────
def build_right_col(styles):
    items = []

    def gap(h=3):
        items.append(Spacer(1, h))

    # ── Professional Summary ──
    items += section_title("Professional Summary", styles)
    items.append(Paragraph(
        "Lead Flutter Developer with <b>8+ years</b> of software development experience "
        "and a strong background in cross-platform mobile architecture, system design, and "
        "team leadership. Expert in building scalable Flutter applications for <b>Android, "
        "iOS, Web, and Desktop</b>, with hands-on experience designing Python-based backend "
        "services and RESTful APIs. Proven ability to own end-to-end products, mentor "
        "developers, and deliver high-performance systems for e-commerce, POS, logistics, "
        "and enterprise applications.",
        styles["summary"]
    ))
    gap(4)

    # ── Core Competencies ──
    items += section_title("Core Competencies", styles)
    competencies = [
        "Flutter Architecture & State Management",
        "Cross-Platform Development (Mobile · Web · Desktop)",
        "Technical Leadership & Code Reviews",
        "Python Backend Development",
        "RESTful API Design & Integration",
        "Payment Gateways (Apple Pay, Stripe)",
        "Database Design & Optimisation",
        "Performance Optimisation & Scalability",
        "Mentoring & Team Collaboration",
    ]
    # Two-column grid for competencies
    rows = []
    for i in range(0, len(competencies), 2):
        left  = Paragraph(f"✔  {competencies[i]}",   styles["skill_tag"])
        right = Paragraph(f"✔  {competencies[i+1]}", styles["skill_tag"]) \
                if i + 1 < len(competencies) else Paragraph("", styles["skill_tag"])
        rows.append([left, right])

    comp_table = Table(rows, colWidths=[RIGHT_COL * 0.5, RIGHT_COL * 0.5])
    comp_table.setStyle(TableStyle([
        ("VALIGN",  (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 1),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
    ]))
    items.append(comp_table)
    gap(4)

    # ── Professional Experience ──
    items += section_title("Professional Experience", styles)

    # Job 1
    job1 = Table(
        [[Paragraph("Lead / Senior Flutter Developer &amp; Tech Lead",  styles["job_title"]),
          Paragraph("Oct 2021 – Present", styles["job_org"])]],
        colWidths=[RIGHT_COL * 0.65, RIGHT_COL * 0.35]
    )
    job1.setStyle(TableStyle([
        ("VALIGN",  (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ]))
    items.append(job1)
    items.append(Paragraph("IKLIX &nbsp;·&nbsp; Dubai, UAE", styles["job_org"]))
    for b in [
        "Led architecture &amp; development of Flutter apps across mobile, web and desktop",
        "Owned full e-commerce ecosystem: POS, delivery, dashboards, inventory",
        "Built and maintained Python backend services and RESTful APIs",
        "Integrated Apple Pay, Stripe and third-party SDKs",
        "Conducted code reviews, mentoring and enforced best practices",
        "Odoo integration with Klix App for sales management",
        "Improved performance, scalability and release stability",
    ]:
        items.append(bullet(b, styles))
    gap(3)

    # Job 2
    job2 = Table(
        [[Paragraph("Technical Developer",  styles["job_title"]),
          Paragraph("Sep 2018 – Aug 2021", styles["job_org"])]],
        colWidths=[RIGHT_COL * 0.65, RIGHT_COL * 0.35]
    )
    job2.setStyle(TableStyle([
        ("VALIGN",  (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ]))
    items.append(job2)
    items.append(Paragraph("Massar &nbsp;·&nbsp; Dubai, UAE", styles["job_org"]))
    for b in [
        "Developed iOS and Android apps using NativeScript (Angular / TypeScript)",
        "Published apps to Google Play Store and Apple App Store",
        "Integrated native plugins and third-party APIs",
    ]:
        items.append(bullet(b, styles))
    gap(3)

    # Job 3
    job3 = Table(
        [[Paragraph("Android Developer",  styles["job_title"]),
          Paragraph("Dec 2015 – Mar 2017", styles["job_org"])]],
        colWidths=[RIGHT_COL * 0.65, RIGHT_COL * 0.35]
    )
    job3.setStyle(TableStyle([
        ("VALIGN",  (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ]))
    items.append(job3)
    items.append(Paragraph(
        "Al-Hafiz Design Center &amp; Jolta Technology &nbsp;·&nbsp; Pakistan",
        styles["job_org"]
    ))
    for b in [
        "Developed native and hybrid Android applications",
        "Integrated REST APIs and worked on Arduino-based home automation",
        "Enhanced multiple production apps",
    ]:
        items.append(bullet(b, styles))
    gap(4)

    # ── Education ──
    items += section_title("Education", styles)
    items.append(Paragraph("Bachelor of Software Engineering", styles["edu_title"]))
    items.append(Paragraph(
        "GC University Faisalabad, Pakistan &nbsp;·&nbsp; 2011 – 2015",
        styles["edu_sub"]
    ))

    return items


# ── Build the CV ─────────────────────────────────────────────────────────────
def generate_cv(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=0, rightMargin=0,
        topMargin=0,  bottomMargin=0,
    )

    styles = make_styles()
    left_items  = build_left_col(styles)
    right_items = build_right_col(styles)

    # ── Header banner ──────────────────────────────────────────────────────
    header_data = [[
        Paragraph("Hafiz Qasim Ali", styles["name"]),
        Paragraph("Lead Flutter Developer", styles["title"]),
    ]]
    header_table = Table(
        header_data,
        colWidths=[PAGE_W * 0.55, PAGE_W * 0.45],
        rowHeights=[22 * mm],
    )
    header_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), EURO_BLUE),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",  (0, 0), (0,  0),  MARGIN_L),
        ("LEFTPADDING",  (1, 0), (1,  0),  4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]))

    # ── Blue accent bar below header ───────────────────────────────────────
    accent_table = Table(
        [[""]],
        colWidths=[PAGE_W],
        rowHeights=[3],
    )
    accent_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFD700")),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
    ]))

    # ── Two-column body ────────────────────────────────────────────────────
    left_cell  = left_items
    right_cell = right_items

    body_table = Table(
        [[left_cell, "", right_cell]],
        colWidths=[LEFT_COL, GUTTER, RIGHT_COL],
        rowHeights=[None],
    )
    body_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (0, 0), EURO_BLUE),
        ("BACKGROUND",   (2, 0), (2, 0), WHITE),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (0,  0),  MARGIN_L),
        ("RIGHTPADDING", (0, 0), (0,  0),  5),
        ("TOPPADDING",   (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING",(0, 0), (-1, -1), MARGIN_B),
        ("LEFTPADDING",  (2, 0), (2,  0),  6),
        ("RIGHTPADDING", (2, 0), (2,  0),  MARGIN_R),
    ]))

    story = [header_table, accent_table, body_table]

    doc.build(story)
    print(f"CV saved → {output_path}")


# ── Cover Letter ─────────────────────────────────────────────────────────────
def generate_cover_letter(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=0,
        bottomMargin=MARGIN_B,
    )

    styles = make_styles()

    def ps(name, **kw):
        return ParagraphStyle(name, **kw)

    h_name = ps("CLName", fontName="Helvetica-Bold", fontSize=16,
                 textColor=WHITE, leading=20, spaceAfter=1)
    h_title = ps("CLTitle", fontName="Helvetica", fontSize=9.5,
                  textColor=colors.HexColor("#CCE0FF"), leading=13)
    cl_body = ps("CLBody", fontName="Helvetica", fontSize=9.5,
                  textColor=EURO_DARK, leading=14, spaceAfter=8,
                  alignment=TA_JUSTIFY)
    cl_label = ps("CLLabel", fontName="Helvetica-Bold", fontSize=8.5,
                   textColor=EURO_GREY, leading=12)
    cl_value = ps("CLValue", fontName="Helvetica", fontSize=9,
                   textColor=EURO_DARK, leading=13)
    cl_sig   = ps("CLSig", fontName="Helvetica-Bold", fontSize=10,
                   textColor=EURO_BLUE, leading=14)
    date_style = ps("CLDate", fontName="Helvetica-Oblique", fontSize=8.5,
                     textColor=EURO_GREY, leading=12, spaceAfter=8)

    # Header banner
    header_data = [[
        Paragraph("Hafiz Qasim Ali", h_name),
        Paragraph("Lead Flutter Developer", h_title),
    ]]
    header_table = Table(
        header_data,
        colWidths=[PAGE_W * 0.55, PAGE_W * 0.45],
        rowHeights=[20 * mm],
    )
    header_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), EURO_BLUE),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",  (0, 0), (0,  0),  MARGIN_L),
        ("LEFTPADDING",  (1, 0), (1,  0),  4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]))

    accent = Table([[""]],colWidths=[PAGE_W], rowHeights=[3])
    accent.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFD700")),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
    ]))

    story = [header_table, accent, Spacer(1, 10 * mm)]

    # Date & contact block
    contact_rows = [
        ["Date:",     "12 May 2026"],
        ["Email:",    "h.qasimali007@gmail.com"],
        ["Phone:",    "+971 50 289 6128"],
        ["Location:", "Ajman, UAE"],
    ]
    contact_table = Table(
        [[Paragraph(r[0], cl_label), Paragraph(r[1], cl_value)]
         for r in contact_rows],
        colWidths=[28 * mm, 100 * mm],
    )
    contact_table.setStyle(TableStyle([
        ("VALIGN",  (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING",   (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 1),
    ]))
    story.append(contact_table)
    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="100%", thickness=0.7, color=EURO_BLUE,
                             spaceAfter=6, spaceBefore=2))

    # Salutation
    story.append(Paragraph("Dear Hiring Manager,", cl_body))

    # Body paragraphs
    para1 = (
        "I am writing to express my strong interest in a <b>Lead Flutter Developer</b> "
        "or <b>Senior Mobile Engineer</b> position within your organisation. With over "
        "<b>eight years of hands-on software development experience</b> — including four "
        "years leading cross-platform Flutter projects at IKLIX Dubai — I am confident "
        "that my technical depth and leadership background align closely with the demands "
        "of a senior engineering role."
    )
    para2 = (
        "At IKLIX, I architected and delivered an end-to-end Flutter ecosystem spanning "
        "mobile, web, and desktop platforms. My responsibilities extended well beyond "
        "writing code: I designed the overall system architecture, owned the full "
        "e-commerce stack (POS, delivery, inventory, and merchant dashboards), integrated "
        "payment gateways (Apple Pay and Stripe), and connected the platform with Odoo "
        "ERP. I also built and maintained the Python-based backend services and RESTful "
        "APIs that power these products, demonstrating my ability to contribute across the "
        "full stack."
    )
    para3 = (
        "Prior to IKLIX, I worked as a Technical Developer at Massar Dubai, where I "
        "developed and published iOS and Android applications using NativeScript, and "
        "earlier as an Android Developer in Pakistan, delivering native and hybrid apps "
        "with REST API integrations. This breadth of experience gives me a strong "
        "contextual understanding of how mobile products evolve across the full lifecycle."
    )
    para4 = (
        "I take particular pride in my approach to <b>team leadership and knowledge "
        "sharing</b>: conducting structured code reviews, mentoring junior developers, "
        "and establishing best practices that reduce technical debt and accelerate "
        "delivery. I believe great mobile products are built by empowered, well-guided "
        "teams, and I am eager to bring that mindset to your engineering culture."
    )
    para5 = (
        "I hold a <b>Bachelor of Software Engineering</b> from GC University Faisalabad "
        "and communicate fluently in English, Urdu, and Punjabi. I am available for "
        "immediate interview and can accommodate relocation or remote arrangements as "
        "required."
    )
    para6 = (
        "Thank you for considering my application. I look forward to the opportunity to "
        "discuss how my skills and experience can contribute to your team's success. "
        "Please find my CV attached for your reference."
    )

    for para in [para1, para2, para3, para4, para5, para6]:
        story.append(Paragraph(para, cl_body))

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("Yours sincerely,", cl_body))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("Hafiz Qasim Ali", cl_sig))
    story.append(Paragraph("Lead Flutter Developer", ps(
        "CLSubSig", fontName="Helvetica", fontSize=9, textColor=EURO_GREY, leading=12
    )))

    doc.build(story)
    print(f"Cover letter saved → {output_path}")


if __name__ == "__main__":
    os.makedirs("/workspace/cv/output", exist_ok=True)
    generate_cv("/workspace/cv/output/Hafiz_Qasim_Ali_Europass_CV.pdf")
    generate_cover_letter("/workspace/cv/output/Hafiz_Qasim_Ali_Cover_Letter.pdf")
