from fpdf import FPDF
import os
import platform

def create_resume(data: dict) -> str:
    """
    Rezyume yaratadi PDF formatida.
    Emoji yo'q, O‘zbek va Ingliz harflari ishlaydi.
    """

    lang = data.get("language", "uz")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(True, 15)

    # ================= FONT =================
    base_dir = os.path.dirname(__file__)
    font_path = os.path.join(base_dir, "DejaVuSans.ttf")

    # Agar DejaVuSans.ttf topilmasa Windows fontidan foydalan
    if not os.path.exists(font_path):
        if platform.system() == "Windows":
            font_path = "C:/Windows/Fonts/arial.ttf"
        else:
            raise FileNotFoundError(f"Font topilmadi: {font_path}")

    pdf.add_font("CustomFont", "", font_path, uni=True)
    pdf.add_font("CustomFont", "B", font_path, uni=True)
    pdf.set_font("CustomFont", "", 12)

    # ================= LABELS =================
    if lang == "en":
        title = "YOUR RESUME"
        labels = {
            "name": "Name:",
            "surname": "Surname:",
            "birth": "Date of birth:",
            "address": "Address:",
            "phone": "Phone:",
            "email": "Email:",
            "exp": "Work Experience",
            "company": "Company:",
            "direction": "Direction:",
            "period": "Period:",
            "skills_title": "Skills & Certificates",
            "skills": "Skills:",
            "certificate": "Certificates:"
        }
    else:
        title = "SIZNING REZYUMENGIZ"
        labels = {
            "name": "Ism:",
            "surname": "Familiya:",
            "birth": "Tug‘ilgan sana:",
            "address": "Manzil:",
            "phone": "Telefon:",
            "email": "Email:",
            "exp": "Ish tajribasi",
            "company": "Kompaniya nomi:",
            "direction": "Kompaniya yo'nalishi:",
            "period": "Ish boshlanish va tugash davri:",
            "skills_title": "Ko‘nikmalar va Sertifikatlar",
            "skills": "Ko‘nikmalar:",
            "certificate": "Sertifikat:"
        }

    # ================= TITLE =================
    pdf.set_font("CustomFont", "B", 16)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("CustomFont", "", 12)

    # ================= HELPER FUNC =================
    def line(label, key):
        value = data.get(key, "")
        if value:
            pdf.multi_cell(0, 8, f"{label} {value}")

    # ================= BASIC INFO =================
    line(labels["name"], "name")
    line(labels["surname"], "surname")
    line(labels["birth"], "birth")
    line(labels["address"], "address")
    line(labels["phone"], "phone")
    line(labels["email"], "email")

    # ================= EXPERIENCE =================
    pdf.ln(3)
    pdf.set_font("CustomFont", "B", 12)
    pdf.cell(0, 8, labels["exp"], ln=True)
    pdf.set_font("CustomFont", "", 12)
    line(labels["company"], "company")
    line(labels["direction"], "direction")
    line(labels["period"], "period")

    # ================= SKILLS =================
    pdf.ln(3)
    pdf.set_font("CustomFont", "B", 12)
    pdf.cell(0, 8, labels["skills_title"], ln=True)
    pdf.set_font("CustomFont", "", 12)
    line(labels["skills"], "skills")
    line(labels["certificate"], "certificate")

    # ================= SAVE FILE =================
    filename = os.path.join(base_dir, "resume.pdf")
    pdf.output(filename)
    return filename