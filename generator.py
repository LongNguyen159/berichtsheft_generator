from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
from schemas import Fields


def create_overlay(data: dict, coords: dict, font="Helvetica", font_size=12, line_spacing=14, pagesize=A4):
    """
    data: dict with keys matching coords
    coords: dict {field_name: (x, y)}
    font_size: base font size
    line_spacing: vertical spacing between lines
    """
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=pagesize)
    can.setFont(font, font_size)

    for field, (x, y) in coords.items():
        if field not in data:
            continue
        value = data[field]
        if not value:
            continue

        # Handle multi-line values
        textobject = can.beginText(x, y)
        textobject.setFont(font, font_size)
        textobject.setLeading(line_spacing)  # ← use your line spacing here

        for line in str(value).split("\n"):
            textobject.textLine(line)
        can.drawText(textobject)

    can.save()
    packet.seek(0)
    return packet

def insert_text_on_pdf(template_path: str, output_path: str, data: dict, coords: dict, font: str = "Helvetica", font_size: int = 12, line_spacing: int = 14):
    reader = PdfReader(template_path)
    writer = PdfWriter()

    overlay_pdf = PdfReader(
        create_overlay(data, coords, font=font, font_size=font_size, line_spacing=line_spacing)
    )
    overlay_page = overlay_pdf.pages[0]

    for page in reader.pages:
        page.merge_page(overlay_page)
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)