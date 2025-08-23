from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import io
import textwrap
from schemas import Fields


def create_overlay(data: dict, coords: dict, font="Helvetica", font_size=12, line_spacing=14, pagesize=A4, field_max_widths=None):
    """
    data: dict with keys matching coords
    coords: dict {field_name: (x, y)}
    font_size: base font size
    line_spacing: vertical spacing between lines
    field_max_widths: dict {field_name: max_width_in_points} - fields that should wrap text
    """
    if field_max_widths is None:
        field_max_widths = {
            'texts_1': 450,  # Allow text to go up to 450 points from start position
            'texts_2': 450,
            'texts_3': 450,
        }
    
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=pagesize)
    can.setFont(font, font_size)

    for field, (x, y) in coords.items():
        if field not in data:
            continue
        value = data[field]
        if not value:
            continue

        # Handle multi-line values with optional text wrapping
        textobject = can.beginText(x, y)
        textobject.setFont(font, font_size)
        textobject.setLeading(line_spacing)

        # Check if this field needs text wrapping
        if field in field_max_widths:
            max_width = field_max_widths[field]
            # Estimate characters per line based on font size (rough approximation)
            chars_per_line = int(max_width / (font_size * 0.5))  # 0.5 is approximate char width ratio

            for line in str(value).split("\n"):
                if len(line) <= chars_per_line:
                    textobject.textLine(line)
                else:
                    # Wrap long lines
                    wrapped_lines = textwrap.fill(line, width=chars_per_line).split('\n')
                    for wrapped_line in wrapped_lines:
                        textobject.textLine(wrapped_line)
        else:
            # No wrapping for other fields
            for line in str(value).split("\n"):
                textobject.textLine(line)
        
        can.drawText(textobject)

    can.save()
    packet.seek(0)
    return packet

def insert_text_on_pdf(template_path: str, output_path: str, data: dict, coords: dict, font: str = "Helvetica", font_size: int = 12, line_spacing: int = 14, field_max_widths=None):
    reader = PdfReader(template_path)
    writer = PdfWriter()

    overlay_pdf = PdfReader(
        create_overlay(data, coords, font=font, font_size=font_size, line_spacing=line_spacing, field_max_widths=field_max_widths)
    )
    overlay_page = overlay_pdf.pages[0]

    for page in reader.pages:
        page.merge_page(overlay_page)
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

    with open(output_path, "wb") as f:
        writer.write(f)