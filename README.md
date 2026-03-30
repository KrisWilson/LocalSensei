## Local Sensei 
#### Background Daemon taking screenshots at your command, sent to local VLM (hosted at your NPU/CPU), describe then send reflection to local coding LLM (hosted at your GPU). Create successful code and automatically copy into copyboard <3

### Requirements:
* Linux with X11/Wayland
* xbindkeys or other mapping key→command software
* Ollama
* at least 15 GB of free space (depends on selected LLM model)
* Recommended usecase with Tilda or Yakuake (drop-down terminal)
* python3 with libs in requirements.txt

### Example usage for NPU (2GB RAM) and GPU (8GB VRAM):
Bind Client.py under some key with xbindkeys to trigger action

* Gemma 3 4b is unusable for recognizing code from IDE
* same as InternVL and Phi-3.5
* The best option is only to put GLM-OCR into VRAM but it won't be at CPU/NPU (its not compiled yet for OpenVINO for INTEL)

For GPU:
* Ollama with Qwen3-8b (https://ollama.com/library/qwen3) ~ 6GB VRAM 4k context

For NPU:
* OpenVINO with Gemma-3-4b (VLM) (https://huggingface.co/OpenVINO/gemma-3-4b-it-int4-cw-ov)
