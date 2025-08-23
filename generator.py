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

if __name__ == "__main__":

    fields = Fields()

    fields.start_date.content = """
    22/04/2024
    """
    fields.end_date.content = """
    26/04/2024
    """

    fields.texts_1.content = """\
        - GPS Zeit-Synchronisierung per PPS-Signal
        - Test down line
        - Diagnose erfolgreich
        - Noch ein Eintrag
    """

    fields.hour_1.content = """
    08:00
    """
    fields.hour_2.content = """
    12:00
    """
    fields.hour_3.content = """
    18:00
    """


    # Computed Fields
    fields.date_of_sign.content = fields.end_date.content

    start_date_formatted = fields.start_date.content.replace("/", "_")
    end_date_formatted = fields.end_date.content.replace("/", "_")

    template_file_path = '/Users/longnguyen/Documents/School/Berichtsheft/berichtsheft-woechentlich-1 - data.pdf'
    output_file_path = f"/Users/longnguyen/Documents/School/Berichtsheft/berichtsheft AP2/berichtsheft-w{start_date_formatted}.pdf"

    insert_text_on_pdf(
        template_file_path,
        output_file_path,
        fields.as_data(),
        fields.as_coords(),
        font_size=12,
        line_spacing=14,
    )