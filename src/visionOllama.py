import ollama
from ollama import chat
from ollama import ChatResponse
from src.ui import AssistantUI
# https://github.com/ollama/ollama-python

ui = AssistantUI()

class GPU2Model:
    def __init__(self, ollama_model):
        # Sprawdź czy model jest pobrany (404) i pobierz go jeżeli go nie ma
        try:
          ollama.chat(ollama_model)
          ui.display_good(f"[Startup] Ollama model {ollama_model} loaded")
          self.ollama_model = ollama_model
        except ollama.ResponseError as e:
          ui.display_error('Error: ' + e.error)
          if e.status_code == 404:
            ui.display_request(f"[Startup] Ollama model {ollama_model}  not downloaded - trying download...")
            ollama.pull(ollama_model)
            ui.display_good(f"[Startup] Ollama model {ollama_model}  downloaded")
    def message(self, imagepath):
        ui.display_request(f"[OCR] {self.ollama_model} reading {imagepath}")
        response = ollama.chat(
            model=self.ollama_model,
            ## TODO: BETTER PROMPT for taking only code and logs
            messages=[
                {"role": "user", "content": "ONLY read code from IDE and logs", "images": [imagepath]},
            ],
        )
#       print(response["message"]['role'])
        return response["message"]['content']
