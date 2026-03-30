import ollama
from ollama import chat
from ollama import ChatResponse
from src.ui import AssistantUI
# https://github.com/ollama/ollama-python

ui = AssistantUI()

class GPUModel:
    def __init__(self, ollama_model):
        # Sprawdź czy model jest pobrany (404) i pobierz go jeżeli go nie ma
        try:
          ollama.chat(ollama_model)
          ui.display_good("[Startup] Ollama model loaded")
          self.ollama_model = ollama_model
        except ollama.ResponseError as e:
          ui.display_error('Error: ' + e.error)
          if e.status_code == 404:
            ui.display_request("[Startup] Ollama model not downloaded - trying download...")
            ollama.pull(ollama_model)
            ui.display_good("[Startup] Ollama model downloaded")
    def message(self, message):
        ui.display_request(f"[LLM] {self.ollama_model} doing job...")
        response: ChatResponse = chat(model=self.ollama_model, messages=[
        {
            'role': 'user',
            'content': "Please write ONLY CODE, there is a not working code: \n\n" + message,
        },
        ])
        return response.message.content
