from dataclasses import dataclass, field
from typing import Tuple, Dict
from reportlab.lib.pagesizes import A4
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
    name: Field = field(default_factory=lambda: Field((50, adjust_y(75)), "My default name"))
    week_no: Field = field(default_factory=lambda: Field((505, adjust_y(52))))
    beruf: Field = field(default_factory=lambda: Field((150, adjust_y(101))))
    ausbildung_jahr: Field = field(default_factory=lambda: Field((527, adjust_y(101))))
    start_date: Field = field(default_factory=lambda: Field((171, 712)))
    end_date: Field = field(default_factory=lambda: Field((257, 712)))
    texts_1: Field = field(default_factory=lambda: Field((50, 650)))
    texts_2: Field = field(default_factory=lambda: Field((100, 650)))
    texts_3: Field = field(default_factory=lambda: Field((100, 600)))
    hour_1: Field = field(default_factory=lambda: Field((400, 700)))
    hour_2: Field = field(default_factory=lambda: Field((400, 650)))
    hour_3: Field = field(default_factory=lambda: Field((400, 600)))
    date_of_sign: Field = field(default_factory=lambda: Field((100, 550)))

    def as_dict(self) -> Dict[str, Field]:
        """Return dict-like view, useful for iterating in PDF generator."""
        return self.__dict__

    def as_coords(self) -> Dict[str, Tuple[float, float]]:
        return {name: f.coords for name, f in self.__dict__.items()}

    def as_data(self) -> Dict[str, str]:
        return {name: f.content for name, f in self.__dict__.items()}

