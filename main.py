from pathlib import Path
from schemas import Fields
from generator import insert_text_on_pdf

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = BASE_DIR / "templates" / "berichtsheft_wochenlich_template.pdf"

def main():
    fields = Fields()

    fields.name.content = "Thanh Long Nguyen"

    fields.week_no.content = "59"
    fields.start_date.content = "22/04/2024"
    fields.end_date.content = "27/04/2024"
    fields.ausbildung_jahr.content = "2"

    fields.texts_3.content = """\
        - GPS Zeit-Synchronisierung per PPS-Signal
        - Test down line
        - Diagnose erfolgreich
        - Noch ein Eintrag
        - Test if this new code works
    """

    fields.hour_1.content = "40"


    fields.hour_2.content = "12"
    fields.hour_3.content = "18"


    # Computed Fields
    fields.date_of_sign.content = fields.end_date.content
    fields.date_of_sign_2.content = fields.end_date.content
    start_date_formatted = fields.start_date.content.replace("/", "_")
    output_file_path = f"/Users/longnguyen/Documents/School/Berichtsheft/berichtsheft AP2/berichtsheft-w{start_date_formatted}.pdf"

    insert_text_on_pdf(
        str(TEMPLATE_PATH),
        str(output_file_path),
        fields.as_data(),
        fields.as_coords(),
        font_size=12,
        line_spacing=14,
    )

if __name__ == "__main__":
    main()
