## Local Sensei 
#### Background Daemon taking screenshots at your command, sent to local VLM (hosted at your NPU/CPU/GPU), VLM-describe then send reflection to local coding LLM (hosted at your GPU). 
#### Create successful code and automatically copy into copyboard <3


![Showcase](https://github.com/KrisWilson/LocalSensei/blob/master/showcase.gif)

### Requirements:
* Linux with X11/Wayland
* xbindkeys or other mapping key→command software
* Ollama
* at least 15 GB of free space (depends on selected LLM model)
* Recommended use case with Tilda or Yakuake (drop-down terminal)
* python3 with libs in requirements.txt


### Example usage GPU (12GB VRAM):
Bind Client.py under some key with xbindkeys to trigger action

* Tried to do NPU+GPU combo but:
* [OpenVino NPU/CPU] Gemma 3 4b is unusable for recognizing code from IDE
* [OpenVino NPU/CPU] same as InternVL and Phi-3.5
* The best option is only to put GLM-OCR into VRAM, but it won't be at CPU/NPU (it's not compiled yet for OpenVINO for INTEL)

For LLM GPU:
* Ollama with Qwen3-8b (https://ollama.com/library/qwen3) ~ 6GB VRAM

For VLM GPU:
* Ollama with GLM-OCR (VisionLM) (https://ollama.com/library/glm-ocr) ~ 4GB VRAM
