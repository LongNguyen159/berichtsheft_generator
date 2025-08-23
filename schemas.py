from dataclasses import dataclass, field
from typing import Tuple, Dict
from reportlab.lib.pagesizes import A4
from pathlib import Path
import textwrap


# PDF dimensions
PDF_WIDTH, PDF_HEIGHT = A4  # A4 is (595.27, 841.89)

def adjust_y(y: float) -> float:
    """Flip coordinate system to PDF coordinates."""
    return PDF_HEIGHT - y

@dataclass
class Field:
    coords: Tuple[float, float]
    _content: str = ""
    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        # Automatically dedent triple-quoted or indented text
        self._content = textwrap.dedent(value).strip("\n")

# Define schema of all fields
@dataclass
class Fields:
    week_no: Field = field(default_factory=lambda: Field((505, adjust_y(44))))
    name: Field = field(default_factory=lambda: Field((211, adjust_y(70))))

    beruf: Field = field(default_factory=lambda: Field((170, adjust_y(96)), "Fachinformatiker - Anwendungsentwicklung"))
    ausbildung_jahr: Field = field(default_factory=lambda: Field((528, adjust_y(96))))
    abteilung: Field = field(default_factory=lambda: Field((470, adjust_y(121)), "IT-Abteilung"))

    start_date: Field = field(default_factory=lambda: Field((171, adjust_y(121))))
    end_date: Field = field(default_factory=lambda: Field((257, adjust_y(121))))

    texts_1: Field = field(default_factory=lambda: Field((50, adjust_y(176))))
    hour_1: Field = field(default_factory=lambda: Field((502, adjust_y(176))))

    texts_2: Field = field(default_factory=lambda: Field((50, adjust_y(352))))
    hour_2: Field = field(default_factory=lambda: Field((502, adjust_y(352))))

    texts_3: Field = field(default_factory=lambda: Field((50, adjust_y(525))))
    hour_3: Field = field(default_factory=lambda: Field((502, adjust_y(525))))

    date_of_sign: Field = field(default_factory=lambda: Field((50, adjust_y(716))))
    date_of_sign_2: Field = field(default_factory=lambda: Field((305, adjust_y(716))))
    
    # UI configuration fields (not rendered to PDF)
    output_directory: Field = field(default_factory=lambda: Field((0, 0), str(Path.home() / "Documents" / "School" / "Berichtsheft" / "berichtsheft AP2")))

    def as_dict(self) -> Dict[str, Field]:
        """Return dict-like view, useful for iterating in PDF generator."""
        return self.__dict__

    def as_coords(self) -> Dict[str, Tuple[float, float]]:
        """Return coordinates for PDF fields only (excludes UI configuration fields)"""
        ui_fields = {'output_directory'}  # Fields that are UI-only
        return {name: f.coords for name, f in self.__dict__.items() if name not in ui_fields}

    def as_data(self) -> Dict[str, str]:
        """Return data for PDF fields only (excludes UI configuration fields)"""
        ui_fields = {'output_directory'}  # Fields that are UI-only
        return {name: f.content for name, f in self.__dict__.items() if name not in ui_fields}

    def get_text_wrapping_fields(self) -> Dict[str, int]:
        """Return fields that need text wrapping with their maximum widths in points"""
        # Type-safe approach: reference the actual field attributes and get their names
        wrapping_config = [
            (self.texts_1, 475),
            (self.texts_2, 475), 
            (self.texts_3, 475),
        ]
        
        # Get the field names by finding which attribute matches each Field object
        result = {}
        field_dict = self.as_dict()
        
        for field_obj, width in wrapping_config:
            # Find the attribute name that corresponds to this Field object
            for attr_name, attr_field in field_dict.items():
                if attr_field is field_obj:
                    result[attr_name] = width
                    break
        
        return result

