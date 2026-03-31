import time
from contextlib import asynccontextmanager

import pyperclip
import uvicorn
from fastapi import FastAPI
from plyer import notification
from src.config import Config
from src.brain import GPUModel
from src.ui import AssistantUI
from src.vision import NPUModel
from src.visionOllama import GPU2Model
from src.capture import WindowCapturer

config = Config.load()
models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    ui = AssistantUI() # rich console instance

    ui.display_request("[Startup] Loading config...")
    config = Config.load()

    ui.display_request(f"[Startup] Loading screen-shot system")
    models["capturer"] = WindowCapturer()

    ui.display_request(f"[Startup] Checking for Ollama's {config.models.gpu_model} model...")
    models["gpumodel"] = GPUModel(config.models.gpu_model)

    if config.app.use_twice_gpu:
        ui.display_request(f"[Startup] Loading Ollama VLM model {config.models.gpu2_model}...")
        models["npumodel"] = GPU2Model(config.models.gpu2_model)
    else:
        ui.display_request(f"[Startup] Loading {"CPU" if config.app.cpu_instead_npu else "NPU"} model...")
        models["npumodel"] = NPUModel(config.models.npu_model, config.app.cpu_instead_npu)
    yield
    models.clear()
app = FastAPI(lifespan=lifespan)

@app.get("/status")
async def status():
    return {"CPU over NPU?" : config.app.cpu_instead_npu,
            "GPU twice (Ollama LLM + VLM)" : config.app.use_twice_gpu,
            "LLM Model": config.models.gpu_model,
            "VLM Model": config.models.npu_model,
            }

@app.get("/")
async def root():
    return {"about", "blank"}

@app.get("/captureAndAnalyze")
async def captureanalyze():
    pngpath = models["capturer"].capture_active_window(config.app.screenshot_dir + time.ctime())

    notification.notify(
        title='Local Sensei',
        message='Screenshot taken - identifying',
        app_name='LocalSensei',
        timeout=5
    )

    npureply = models["npumodel"].message(pngpath)
 #   ui.display_request(f"[NPU - reply] {npureply}")
    gpureply = models["gpumodel"].message(npureply)
 #   ui.display_request(f"[GPU - reply] {gpureply}")
    pyperclip.copy(gpureply[1:-1])
    notification.notify(
        title="Local Sensei",
        message="Data has been copied into your clipboard",
        app_name='LocalSensei',
        timeout=5
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
    notification.notify(
        title='Local Sensei',
        message='System is ready to action',
        app_name='LocalSensei',
        timeout=5
    )
