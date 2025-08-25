from pathlib import Path
from schemas import Fields
from generator import insert_text_on_pdf
from nicegui import ui, native
from datetime import datetime, timedelta
from multiprocessing import freeze_support  # noqa
freeze_support()  # noqa
from file_manager import save_configuration, load_configuration, get_resource_path
from sys import exit

# Global fields instance for the UI
fields = Fields()

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = get_resource_path("assets/templates/berichtsheft_wochenlich_template.pdf")

# Verify template exists
if not TEMPLATE_PATH.exists():
    print(f"Error: Template file not found at {TEMPLATE_PATH}")
    exit(1)



def compute_end_date_from_start(start_date_str: str) -> str:
    """
    Compute end date (Friday) from start date (Monday).
    Supports formats: DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY
    """
    if not start_date_str.strip():
        return ""
    
    try:
        # Try different date formats
        formats = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y"]
        start_date = None
        
        for fmt in formats:
            try:
                start_date = datetime.strptime(start_date_str.strip(), fmt)
                break
            except ValueError:
                continue
        
        if start_date is None:
            return ""  # Could not parse date
        
        # Add 4 days to get from Monday to Friday (Monday + 4 days = Friday)
        end_date = start_date + timedelta(days=4)
        
        # Return in the same format as input (detect by separator)
        if "/" in start_date_str:
            return end_date.strftime("%d/%m/%Y")
        elif "-" in start_date_str:
            return end_date.strftime("%d-%m-%Y")
        else:
            return end_date.strftime("%d.%m.%Y")
            
    except Exception:
        return ""  # Return empty string if any error occurs

def get_week_dates(base_date_str: str, weeks_offset: int) -> tuple[str, str]:
    """
    Get Monday and Friday dates for a week relative to base_date.
    
    Args:
        base_date_str: Current date string in any supported format
        weeks_offset: Number of weeks to add/subtract (negative for previous weeks)
    
    Returns:
        Tuple of (monday_str, friday_str) in the same format as input
    """
    try:
        if not base_date_str.strip():
            # If no base date, use current date
            base_date = datetime.now()
            format_str = "%d/%m/%Y"
        else:
            # Parse the base date
            formats = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y"]
            base_date = None
            format_str = "%d/%m/%Y"  # Default format
            
            for fmt in formats:
                try:
                    base_date = datetime.strptime(base_date_str.strip(), fmt)
                    format_str = fmt
                    break
                except ValueError:
                    continue
            
            if base_date is None:
                return "", ""
        
        # Find the Monday of the base week
        days_since_monday = base_date.weekday()  # Monday is 0, Sunday is 6
        current_monday = base_date - timedelta(days=days_since_monday)
        
        # Calculate the target week's Monday
        target_monday = current_monday + timedelta(weeks=weeks_offset)
        target_friday = target_monday + timedelta(days=4)
        
        # Format dates
        monday_str = target_monday.strftime(format_str)
        friday_str = target_friday.strftime(format_str)
        
        return monday_str, friday_str
        
    except Exception:
        return "", ""

def set_default_values():
    """Set default values for the fields"""
    # Try to load saved configuration first
    config_loaded = load_configuration(fields)
    
    # Only set defaults if no configuration was loaded
    if not config_loaded:
        fields.ausbildung_jahr.content = "2"
        fields.hour_1.content = "40"

def generate_pdf():
    """Generate the PDF with current field values"""
    try:
        # Auto-compute end date from start date if end date is empty
        if fields.start_date.content.strip() and not fields.end_date.content.strip():
            fields.end_date.content = compute_end_date_from_start(fields.start_date.content)
        
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
        
        # Create output directory if it doesn't exist (now configurable)
        output_dir = Path(fields.output_directory.content)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file_path = output_dir / filename

        insert_text_on_pdf(
            str(TEMPLATE_PATH),
            str(output_file_path),
            fields.as_data(),
            fields.as_coords(),
            font_size=12,
            line_spacing=14,
            field_max_widths=fields.get_text_wrapping_fields()
        )
        
        ui.notify(f'PDF generated successfully: {output_file_path}', type='positive')
        
        # Auto-save configuration after successful PDF generation
        save_configuration(fields)
        
    except Exception as e:
        ui.notify(f'Error generating PDF: {str(e)}', type='negative')

def create_ui():
    """Create the NiceGUI interface"""
    ui.markdown('## Berichtsheft Generator').style('display: flex; width: 100%; justify-content: center;')

    with ui.column().style('width: 100%; max-width: 800px; margin: 0 auto; border-radius: 22px;'):
        ui.markdown('### Basic Information')
        # Output directory field with browse button
        with ui.row().style('width: 100%; gap: 0.5rem'):
            output_dir_input = ui.input('Output Directory', value=fields.output_directory.content, placeholder='Where to save generated PDFs').style('flex: 1')
            output_dir_input.bind_value(fields.output_directory, 'content')
            
            def browse_folder():
                # For now, show a notification with instructions since file dialogs are complex in web UI
                ui.notify('Copy and paste the folder path where you want to save PDFs', type='info')
            
            ui.button('📁', on_click=browse_folder).props('size=sm').style('align-self: end; margin-bottom: 6px')
        
        # Name field
        name_input = ui.input('Name', value=fields.name.content).style('width: 100%')
        name_input.bind_value(fields.name, 'content')
        
        
        # Profession and department
        with ui.row().style('width: 100%; gap: 1rem'):
            beruf_input = ui.input('Profession', value=fields.beruf.content).style('flex: 1')
            beruf_input.bind_value(fields.beruf, 'content')
            
            abteilung_input = ui.input('Department', value=fields.abteilung.content).style('flex: 1')
            abteilung_input.bind_value(fields.abteilung, 'content')
        
    with ui.column().style('width: 100%; max-width: 800px; margin: 1rem auto;'):
        ui.markdown('### Activities')
        with ui.card().style('width: 100%; gap: 1rem; padding: 22px; border-radius: 22px;'):
            # Week number and training year
            with ui.row().style('width: 100%; gap: 1rem'):
                week_input = ui.input('Week Number', value=fields.week_no.content).style('flex: 1')
                week_input.bind_value(fields.week_no, 'content')
                
                year_input = ui.input('Training Year', value=fields.ausbildung_jahr.content).style('flex: 1')
                year_input.bind_value(fields.ausbildung_jahr, 'content')
            
            # Date range
            with ui.row().style('width: 100%; gap: 1rem'):
                start_date_input = ui.input('Start Date', value=fields.start_date.content).style('flex: 1')
                start_date_input.bind_value(fields.start_date, 'content')
                
                end_date_input = ui.input('End Date', value=fields.end_date.content).style('flex: 1')
                end_date_input.bind_value(fields.end_date, 'content')
                
                # Auto-compute end date when start date changes
                def on_start_date_change():
                    if fields.start_date.content.strip():
                        computed_end = compute_end_date_from_start(fields.start_date.content)
                        if computed_end:
                            fields.end_date.content = computed_end
                            end_date_input.value = computed_end
                
                start_date_input.on('blur', on_start_date_change)
            
            # Week navigation buttons
            with ui.row().style('width: 100%; gap: 0.5rem; justify-content: center; margin-top: 0.5rem'):
                def go_to_previous_week():
                    base_date = fields.start_date.content or fields.end_date.content
                    monday, friday = get_week_dates(base_date, -1)
                    if monday and friday:
                        fields.start_date.content = monday
                        fields.end_date.content = friday
                        start_date_input.value = monday
                        end_date_input.value = friday
                        
                        # Decrement week number
                        current_week = fields.week_no.content.strip()
                        if current_week.isdigit():
                            new_week = max(1, int(current_week) - 1)  # Don't go below 1
                            fields.week_no.content = str(new_week)
                            week_input.value = str(new_week)
                        
                        # Auto-save after week change
                        save_configuration(fields)
                
                def go_to_next_week():
                    base_date = fields.start_date.content or fields.end_date.content
                    monday, friday = get_week_dates(base_date, 1)
                    if monday and friday:
                        fields.start_date.content = monday
                        fields.end_date.content = friday
                        start_date_input.value = monday
                        end_date_input.value = friday
                        
                        # Increment week number
                        current_week = fields.week_no.content.strip()
                        if current_week.isdigit():
                            new_week = int(current_week) + 1
                            fields.week_no.content = str(new_week)
                            week_input.value = str(new_week)
                        elif not current_week:  # If empty, start at 1
                            fields.week_no.content = "1"
                            week_input.value = "1"
                        
                        # Auto-save after week change
                        save_configuration(fields)
                
                def go_to_current_week():
                    monday, friday = get_week_dates("", 0)  # Current week
                    if monday and friday:
                        fields.start_date.content = monday
                        fields.end_date.content = friday
                        start_date_input.value = monday
                        end_date_input.value = friday
                        # Note: Current week button doesn't change week number

                ui.button('← Previous Week', on_click=go_to_previous_week).props('size=sm color=secondary').style('border-radius: 100px;')
                ui.button('This Week', on_click=go_to_current_week).props('size=sm color=primary').style('border-radius: 100px;')
                ui.button('Next Week →', on_click=go_to_next_week).props('size=sm color=secondary').style('border-radius: 100px;')

        # Work textarea
        with ui.column().style("gap: 0; width: 100%;"):
            ui.markdown('#### Work').style('margin-left: 16px;')
            with ui.card().style('width: 100%; gap: 1rem; padding: 22px; border-radius: 22px;'):
                with ui.row().style('width: 100%; gap: 2rem; margin-bottom: 8px;'):
                    texts_1_input = ui.textarea(label='Work', value=fields.texts_1.content, placeholder='e.g. Work on Angular Services, etc.').props('autogrow').style('flex: 1;')
                    texts_1_input.bind_value_to(fields.texts_1, 'content')
                    
                    hour_1_input = ui.input('Hours 1', value=fields.hour_1.content).style('width: 100px')
                    hour_1_input.bind_value(fields.hour_1, 'content')
        

        # Learning textarea
        with ui.column().style("gap: 0; width: 100%;"):
            ui.markdown('#### Learning').style('margin-left: 16px;')
            with ui.card().style('width: 100%; gap: 1rem; padding: 22px; border-radius: 22px;'):
                with ui.row().style('width: 100%; gap: 2rem; margin-bottom: 8px;'):
                    texts_2_input = ui.textarea(label='Unterweisungen', value=fields.texts_2.content, placeholder='e.g. Supply chain, how to write a document, etc.').props('autogrow').style('flex: 1;')
                    texts_2_input.bind_value_to(fields.texts_2, 'content')
                    
                    hour_2_input = ui.input('Hours 2', value=fields.hour_2.content).style('width: 100px')
                    hour_2_input.bind_value(fields.hour_2, 'content')

        # School textarea
        with ui.column().style("gap: 0; width: 100%;"):
            ui.markdown('#### School').style('margin-left: 16px;')
            with ui.card().style('width: 100%; gap: 1rem; padding: 22px; border-radius: 22px;'):
                with ui.row().style('width: 100%; gap: 2rem; margin-bottom: 8px;'):
                    texts_3_input = ui.textarea(label='School activities', value=fields.texts_3.content, placeholder='e.g. LF5: Datenbank Technologien, etc.').props('autogrow').style('flex: 1;')
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
    
    # Generate PDF button and Save Configuration
    with ui.row().style('width: 100%; max-width: 800px; margin: 1rem auto; text-align: center; border-radius: 22px; justify-content: center; gap: 1rem;'):
        def save_config():
            success = save_configuration(fields)
            if success:
                ui.notify('Configuration saved successfully! ✅', type='positive')
            else:
                ui.notify('Failed to save configuration ❌', type='negative')
        
        # ui.button('💾 Save Settings', on_click=save_config).props('color=secondary size=md').style('border-radius: 100px;')
        ui.button('Generate PDF', on_click=generate_pdf).props('color=primary size=lg').style('border-radius: 100px;')

def main():
    """Main function to set up and run the application"""
    # Set default values
    set_default_values()
    
    # Create the UI
    create_ui()
    
    # Run the application
    ui.run(title='Berichtsheft Generator', port=native.find_open_port(), show=False, native=True, reload=False)

if __name__ in {"__main__", "__mp_main__"}:
    main()
