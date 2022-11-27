from pathlib import Path

from pydantic import BaseModel


class ClassifierModelFiles(BaseModel):
    root_dir_path: Path
    model_file_name: str
    class_names_file_name: str

    @property
    def model_file_path(self) -> Path:
        return self.root_dir_path / self.model_file_name

    @property
    def class_names_file_path(self) -> Path:
        return self.root_dir_path / self.class_names_file_name