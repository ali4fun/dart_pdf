#!/usr/bin/env python3
"""Generate Europass-inspired one-page CV and a cover letter PDF (fpdf2)."""

from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

EUROPASS_BLUE = (0, 51, 153)
LIGHT_GRAY = (245, 245, 245)


class Doc(FPDF):
    def __init__(self) -> None:
        super().__init__(format="A4", unit="mm")
        self.set_auto_page_break(auto=False)
        self.set_margins(12, 12, 12)

    def header_bar(self, title: str) -> None:
        self.set_fill_color(*EUROPASS_BLUE)
        self.rect(0, 0, 210, 11, "F")
        self.set_xy(12, 3)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(255, 255, 255)
        self.cell(0, 6, title)
        self.set_text_color(0, 0, 0)
        self.set_y(14)

    def section(self, label: str) -> None:
        self.ln(2)
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*LIGHT_GRAY)
        self.cell(0, 5, f"  {label}", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.set_font("Helvetica", "", 8.5)
        self.ln(1)

    def kv_row(self, k: str, v: str) -> None:
        self.set_font("Helvetica", "B", 8)
        wk = 38
        self.cell(wk, 4, k)
        self.set_font("Helvetica", "", 8)
        self.multi_cell(0, 4, v, new_x="LMARGIN", new_y="NEXT")

    def bullets(self, items: list[str]) -> None:
        for t in items:
            self.set_x(14)
            self.multi_cell(0, 3.6, f"- {t}", new_x="LMARGIN", new_y="NEXT")


def build_cv(path: Path) -> None:
    pdf = Doc()
    pdf.add_page()
    pdf.header_bar("Curriculum Vitae")

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 6, "Hafiz Qasim Ali", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 4, "Lead Flutter Developer", new_x="LMARGIN", new_y="NEXT")

    pdf.section("Personal information")
    pdf.kv_row("Address:", "Ajman, United Arab Emirates")
    pdf.kv_row("Telephone:", "+971 50 289 6128")
    pdf.kv_row("Email:", "h.qasimali007@gmail.com")

    pdf.section("Profile")
    pdf.set_font("Helvetica", "", 8.5)
    pdf.multi_cell(
        0,
        3.6,
        "Lead Flutter Developer with 8+ years in software development: cross-platform "
        "architecture (Flutter on mobile, web, desktop), system design, and technical "
        "leadership. Strong delivery across e-commerce, POS, logistics, and enterprise "
        "products; Python backends and REST APIs; mentoring, code quality, and stable releases.",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.section("Work experience")
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.cell(0, 4, "Lead / Senior Flutter Developer & Tech Lead", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 8)
    pdf.cell(0, 3.5, "IKLIX, Dubai  |  October 2021 - Present", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.bullets(
        [
            "Architecture and delivery of Flutter apps (Android, iOS, web, desktop).",
            "End-to-end e-commerce: POS, delivery, dashboards, inventory; Odoo integration.",
            "Python services and REST APIs; Apple Pay, Stripe, maps, push, third-party SDKs.",
            "Code reviews, mentoring, performance and scalability improvements.",
        ]
    )
    pdf.ln(0.5)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.cell(0, 4, "Technical Developer", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 8)
    pdf.cell(0, 3.5, "Massar, Dubai  |  September 2018 - August 2021", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.bullets(
        [
            "iOS/Android apps with NativeScript; store releases and native plugin integration.",
        ]
    )
    pdf.ln(0.5)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.cell(0, 4, "Android Developer", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 8)
    pdf.cell(
        0,
        3.5,
        "Al-Hafiz Design Center & Jolta Technology, Pakistan  |  December 2015 - March 2017",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.set_font("Helvetica", "", 8)
    pdf.bullets(
        [
            "Native/hybrid Android, REST integrations, Arduino home automation, production app maintenance.",
        ]
    )

    pdf.section("Education and training")
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.cell(0, 4, "Bachelor of Software Engineering", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 3.5, "GC University Faisalabad, Pakistan  |  2011 - 2015", new_x="LMARGIN", new_y="NEXT")

    pdf.section("Language skills")
    pdf.set_font("Helvetica", "", 8.5)
    pdf.multi_cell(
        0,
        3.6,
        "Mother tongue(s): Urdu, Punjabi  |  Other language(s): English (professional).",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.section("Digital competence")
    pdf.set_font("Helvetica", "", 8)
    pdf.multi_cell(
        0,
        3.5,
        "Flutter (mobile/web/desktop), state management & architecture; Android (Java/XML); "
        "React Native; NativeScript (Angular, TypeScript); HTML, CSS, TypeScript; Python (APIs, "
        "integrations); REST; Firebase; SQLite, MongoDB; Git; Android Studio; payment SDKs "
        "(Apple Pay, Stripe); maps and geolocation; push notifications.",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.output(path)


def build_cover_letter(path: Path) -> None:
    pdf = Doc()
    pdf.add_page()
    pdf.header_bar("Cover letter")

    pdf.set_font("Helvetica", "", 10)
    y = pdf.get_y() + 2
    pdf.set_xy(12, y)
    pdf.multi_cell(
        0,
        5,
        "Hafiz Qasim Ali\nAjman, United Arab Emirates\nh.qasimali007@gmail.com\n+971 50 289 6128",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, "Dear Hiring Manager,", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    body = (
        "I am writing to express my interest in a Lead or Senior Flutter Developer role where I can "
        "combine hands-on engineering with clear technical direction. Over eight years in software "
        "development, I have focused on cross-platform delivery with Flutter across Android, iOS, web, "
        "and desktop, alongside Python-based backends and REST APIs when products require a full-stack "
        "owner.\n\n"
        "In my current position at IKLIX in Dubai, I lead architecture and implementation for "
        "large-scale customer-facing systems, including e-commerce, POS, delivery, dashboards, and "
        "inventory. I integrate payment providers (Apple Pay, Stripe), third-party services, and Odoo "
        "for sales workflows, and I invest in performance, scalability, and release discipline. I "
        "regularly mentor engineers, run code reviews, and keep quality bar high without slowing "
        "delivery.\n\n"
        "Earlier at Massar, I shipped production mobile applications with NativeScript for both major "
        "app stores, which strengthened my eye for native constraints, plugins, and store compliance. "
        "My earlier Android work grounded me in native SDK patterns and API-driven features.\n\n"
        "I would welcome the opportunity to discuss how my experience in Flutter leadership, product "
        "ownership, and pragmatic backend work can support your team and roadmap. Thank you for "
        "considering my application.\n\n"
        "Yours sincerely,\n\n"
        "Hafiz Qasim Ali"
    )
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, body, new_x="LMARGIN", new_y="NEXT")

    pdf.output(path)


def main() -> None:
    out = Path(__file__).resolve().parent / "output"
    out.mkdir(parents=True, exist_ok=True)
    build_cv(out / "Hafiz_Qasim_Ali_CV_Europass_one_page.pdf")
    build_cover_letter(out / "Hafiz_Qasim_Ali_Cover_Letter.pdf")
    print(f"Wrote:\n  {(out / 'Hafiz_Qasim_Ali_CV_Europass_one_page.pdf')}\n  {(out / 'Hafiz_Qasim_Ali_Cover_Letter.pdf')}")


if __name__ == "__main__":
    main()
