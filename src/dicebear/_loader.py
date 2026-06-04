from importlib.resources import files
import json


def load_style(name: str) -> dict:
    try:
        return json.loads(
            files('dicebear_styles').joinpath(f'{name}.json').read_text('utf-8')
        )
    except FileNotFoundError:
        raise ValueError(
            f"Unknown style '{name}'. "
            f"Try upgrading: pip install -U dicebear-styles"
        )
