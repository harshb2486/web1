import os
from pathlib import Path
from typing import Dict


TEMPLATES_DIR = Path(__file__).parent / "templates"


class PromptLoader:
    def load(self, template_name: str) -> str:
        path = TEMPLATES_DIR / template_name
        if not path.exists():
            raise FileNotFoundError(f"Prompt template not found: {template_name}")
        return path.read_text(encoding="utf-8")

    def render(self, template_name: str, **kwargs: Dict[str, str]) -> str:
        template = self.load(template_name)
        for key, value in kwargs.items():
            template = template.replace(f"{{{key}}}", str(value))
        return template

    def list_templates(self) -> list:
        return [f.name for f in TEMPLATES_DIR.iterdir() if f.suffix == ".txt"]
