import yaml
from pydantic import BaseModel

class ModelSettings(BaseModel):
    gpu_model: str
    gpu2_model: str
    npu_model: str

class AppSettings(BaseModel):
    debug: bool
    use_twice_gpu: bool
    cpu_instead_npu: bool
    screenshot_dir: str

class Config(BaseModel):
    models: ModelSettings
    app: AppSettings

    @classmethod
    def load(cls, path="config/settings.yaml"):
        with open(path, "r") as f:
            data = yaml.safe_load(f)
            return cls(**data)
