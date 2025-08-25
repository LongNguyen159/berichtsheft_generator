
from dataclasses import asdict
import sys
import json
from pathlib import Path
from schemas import PersistedFields, Fields


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS', None)
        if base_path is None:
            raise AttributeError
    except AttributeError:
        # Development mode
        base_path = Path(__file__).resolve().parent
    return Path(base_path) / relative_path

def get_config_path():
    """Get path to configuration file in user's home directory"""
    config_dir = Path.home() / ".berichtsheft_generator"
    config_dir.mkdir(exist_ok=True)  # Create directory if it doesn't exist
    return config_dir / "config.json"

def save_configuration(fields: Fields) -> bool:
    """Save current field values to configuration file using typed model"""
    try:
        # Create typed model from current fields
        persisted_fields = PersistedFields.from_fields(fields)
        
        # Convert to dictionary for JSON serialization
        config_data = asdict(persisted_fields)
        
        config_path = get_config_path()
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        print(f"Configuration saved to {config_path}")
        return True
    except Exception as e:
        print(f"Error saving configuration: {e}")
        return False

def load_configuration(fields: Fields) -> bool:
    """Load configuration from file using typed model and apply to fields"""
    try:
        config_path = get_config_path()
        if not config_path.exists():
            print("No configuration file found, using defaults")
            return False
            
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        # Create typed model from loaded data
        persisted_fields = PersistedFields.from_dict(config_data)
        
        # Apply to current fields
        persisted_fields.apply_to_fields(fields)
            
        print(f"Configuration loaded from {config_path}")
        return True
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return False

