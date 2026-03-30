from PIL import Image
import requests
from optimum.intel.openvino import OVModelForVisualCausalLM
from transformers import AutoTokenizer, TextStreamer

model_id = "../models/InternVL2-2B-int4-ov"

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)

ov_model = OVModelForVisualCausalLM.from_pretrained(model_id, trust_remote_code=True)
prompt = "Rewrite all CODE from IDE. Do not comment or add anything."

#url = "https://github.com/openvinotoolkit/openvino_notebooks/assets/29454499/d5fbbd1a-d484-415c-88cb-9986625b7b11"
#image = Image.open(requests.get(url, stream=True).raw)
image = Image.open("../screenshot/1.png")

inputs = ov_model.preprocess_inputs(text=prompt, image=image, tokenizer=tokenizer, config=ov_model.config)

generation_args = {
    "max_new_tokens": 100,
    "streamer": TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
}

generate_ids = ov_model.generate(**inputs, **generation_args)

generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
response = tokenizer.batch_decode(generate_ids, skip_special_tokens=True)[0]
