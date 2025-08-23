from pathlib import Path
from schemas import Fields
from generator import insert_text_on_pdf
from nicegui import ui

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = BASE_DIR / "templates" / "berichtsheft_wochenlich_template.pdf"

# Global fields instance for the UI
fields = Fields()

def set_default_values():
    """Set default values for the fields"""
    fields.name.content = "Thanh Long Nguyen"
    fields.ausbildung_jahr.content = "2"
    fields.hour_1.content = "40"

def generate_pdf():
    """Generate the PDF with current field values"""
    try:
        # Computed Fields
        fields.date_of_sign.content = fields.end_date.content
        fields.date_of_sign_2.content = fields.end_date.content
        
        # Check if start_date is empty and provide a fallback
        if not fields.start_date.content.strip():
            ui.notify('Please enter a start date before generating PDF', type='warning')
            return
            
        start_date_formatted = fields.start_date.content.replace("/", "_")
        
        # Build filename with optional week number
        week_content = fields.week_no.content.strip()
        if week_content and week_content != "0":
            filename = f"berichtsheft_w{week_content}_{start_date_formatted}.pdf"
        else:
            filename = f"berichtsheft_w{start_date_formatted}.pdf"
        
        # Create output directory if it doesn't exist
        # TODO: Make output_dir configurable. output_file_path stays.
        output_dir = Path.home() / "Documents" / "School" / "Berichtsheft" / "berichtsheft AP2"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file_path = output_dir / filename

        insert_text_on_pdf(
            str(TEMPLATE_PATH),
            str(output_file_path),
            fields.as_data(),
            fields.as_coords(),
            font_size=12,
            line_spacing=14,
        )
        
        ui.notify(f'PDF generated successfully: {output_file_path}', type='positive')
        
    except Exception as e:
        ui.notify(f'Error generating PDF: {str(e)}', type='negative')

def create_ui():
    """Create the NiceGUI interface"""
    ui.markdown('# Berichtsheft Generator')
    
    with ui.card().style('width: 100%; max-width: 800px; margin: 0 auto;'):
        ui.markdown('## Personal Information')
        
        # Name field
        name_input = ui.input('Name', value=fields.name.content).style('width: 100%')
        name_input.bind_value(fields.name, 'content')
        
        # Week number and training year
        with ui.row().style('width: 100%; gap: 1rem'):
            week_input = ui.input('Week Number', value=fields.week_no.content).style('flex: 1')
            week_input.bind_value(fields.week_no, 'content')
            
            year_input = ui.input('Training Year', value=fields.ausbildung_jahr.content).style('flex: 1')
            year_input.bind_value(fields.ausbildung_jahr, 'content')
        
        # Profession and department
        with ui.row().style('width: 100%; gap: 1rem'):
            beruf_input = ui.input('Profession', value=fields.beruf.content).style('flex: 1')
            beruf_input.bind_value(fields.beruf, 'content')
            
            abteilung_input = ui.input('Department', value=fields.abteilung.content).style('flex: 1')
            abteilung_input.bind_value(fields.abteilung, 'content')
        
        # Date range
        with ui.row().style('width: 100%; gap: 1rem'):
            start_date_input = ui.input('Start Date', value=fields.start_date.content).style('flex: 1')
            start_date_input.bind_value(fields.start_date, 'content')
            
            end_date_input = ui.input('End Date', value=fields.end_date.content).style('flex: 1')
            end_date_input.bind_value(fields.end_date, 'content')
    
    with ui.card().style('width: 100%; max-width: 800px; margin: 1rem auto;'):
        ui.markdown('### Activities')
        
        # Text fields for activities
        texts_1_input = ui.textarea(label='Work', value=fields.texts_1.content, placeholder='Enter work activities for this period...').props('autogrow').style('width: 100%; min-height: 100px')
        texts_1_input.bind_value_to(fields.texts_1, 'content')
        
        hour_1_input = ui.input('Hours 1', value=fields.hour_1.content).style('width: 100px')
        hour_1_input.bind_value(fields.hour_1, 'content')
        
        ui.separator()
        
        texts_2_input = ui.textarea(label='Unterweisungen', value=fields.texts_2.content, placeholder='Enter work activities for this period...').props('autogrow').style('width: 100%; min-height: 100px')
        texts_2_input.bind_value_to(fields.texts_2, 'content')
        
        hour_2_input = ui.input('Hours 2', value=fields.hour_2.content).style('width: 100px')
        hour_2_input.bind_value(fields.hour_2, 'content')
        
        ui.separator()
        
        texts_3_input = ui.textarea(label='School activities', value=fields.texts_3.content, placeholder='Enter work activities for this period...').props('autogrow').style('width: 100%; min-height: 100px')
        texts_3_input.bind_value_to(fields.texts_3, 'content')
        
        hour_3_input = ui.input('Hours 3', value=fields.hour_3.content).style('width: 100px')
        hour_3_input.bind_value(fields.hour_3, 'content')
    
    # with ui.card().style('width: 100%; max-width: 800px; margin: 1rem auto;'):
    #     ui.markdown('## Signature Dates')
        
    #     with ui.row().style('width: 100%; gap: 1rem'):
    #         date_sign_1_input = ui.input('Signature Date 1', value=fields.date_of_sign.content).style('flex: 1')
    #         date_sign_1_input.bind_value(fields.date_of_sign, 'content')
            
    #         date_sign_2_input = ui.input('Signature Date 2', value=fields.date_of_sign_2.content).style('flex: 1')
    #         date_sign_2_input.bind_value_to(fields.date_of_sign_2, 'content')
    
    # Generate PDF button
    with ui.card().style('width: 100%; max-width: 800px; margin: 1rem auto; text-align: center;'):
        ui.button('Generate PDF', on_click=generate_pdf).props('color=primary size=lg')

def main():
    """Main function to set up and run the application"""
    # Set default values
    set_default_values()
    
    # Create the UI
    create_ui()
    
    # Run the application
    ui.run(title='Berichtsheft Generator', port=8080, show=True)

if __name__ in {"__main__", "__mp_main__"}:
    main()
