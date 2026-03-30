import openvino_genai as ov_genai
from src.ui import AssistantUI
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import openvino as ov

gen_config = ov_genai.GenerationConfig()
gen_config.max_new_tokens = 1024
gen_config.do_sample = True
gen_config.top_p = 0.9
gen_config.temperature = 0.4
gen_config.repetition_penalty = 1.0
gen_config.top_k = 20

config = {
    "PERFORMANCE_HINT": "THROUGHPUT",
}

ui = AssistantUI()

#load_image https://huggingface.co/OpenVINO/gemma-3-4b-it-int4-cw-ov
def load_image(image_file):
    image = Image.open(image_file).convert("RGB")
    image_data = np.array(image.getdata()).reshape(1, image.size[1], image.size[0], 3).astype(np.uint8)
    return ov.Tensor(image_data)

class NPUModel:
    def __init__(self, model, cpu=False):
        self.model = "models/" + model
        self.cpu = cpu
        self.device = "CPU" if cpu else "NPU"
        ui.display_request(f"[NPU] Inicjalizacja VLMPipeline na jednostce {self.device}...")
        try:
            self.pipe = ov_genai.VLMPipeline(self.model, self.device, **config)
            ui.display_good(f"[NPU] {self.device} wystartowało.")
        except Exception as e:
            ui.display_error(f"[NPU] {self.device} nie odpowiedziało: {e}")
            exit()

    def message(self, imagepath):
        self.pipe.start_chat()
        raw_result = self.pipe.generate("", image=load_image(imagepath), generation_config=gen_config)
        self.pipe.finish_chat()
        return str(raw_result)
