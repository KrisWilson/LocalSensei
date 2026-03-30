import openvino_genai as ov_genai
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import openvino as ov

device = "NPU"
pipe = ov_genai.VLMPipeline("../models/gemma-3-4b-it-int4-cw-ov", device)

def load_image(image_file):
    if isinstance(image_file, str) and (image_file.startswith("http") or image_file.startswith("https")):
        response = requests.get(image_file)
        image = Image.open(BytesIO(response.content)).convert("RGB")
    else:
        image = Image.open(image_file).convert("RGB")
    image_data = np.array(image.getdata()).reshape(1, image.size[1], image.size[0], 3).astype(np.uint8)
    return ov.Tensor(image_data)

prompt = "Write down code from image. Do not comment anything, just code."

#url = "https://github.com/openvinotoolkit/openvino_notebooks/assets/29454499/d5fbbd1a-d484-415c-88cb-9986625b7b11"
image_tensor = load_image("../screenshot/1.png")

def streamer(subword: str) -> bool:
    print(subword, end="", flush=True)
    return False

pipe.start_chat()
output = pipe.generate(prompt, image=image_tensor, max_new_tokens=100, streamer=streamer)
pipe.finish_chat()
