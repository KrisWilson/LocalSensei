import time

from fastapi import FastAPI
from plyer import notification

from src.config import Config
from src.brain import GPUModel
from src.ui import AssistantUI
from src.vision import NPUModel
from src.capture import WindowCapturer

app = FastAPI()
#if __name__ == "__main__":

ui = AssistantUI() # rich console instance

ui.display_request("[Startup] Loading config...")
config = Config.load()

ui.display_request("[Startup] Checking for Ollama's model...")
gpumodel = GPUModel(config.models.gpu_model)

ui.display_request(f"[Startup] Loading {"CPU" if config.app.cpu_instead_npu else "NPU"} model...")
npumodel = NPUModel(config.models.npu_model, config.app.cpu_instead_npu)

ui.display_request(f"[Startup] Loading screen-shot system")
capturer = WindowCapturer()


notification.notify(
    title='Local Sensei',
    message='System is ready to action',
    app_name='LocalSensei',
    timeout=5
)

@app.get("/status")
async def status():
    return {"GPU status": "GPU " + config.models.gpu_model + " is online",
            "NPU status": "NPU " + config.models.npu_model + " is online",
            "CPU use": config.app.cpu_instead_npu
            }

@app.get("/")
async def root():
    return {"about", "blank"}

@app.get("/captureAndAnalyze")
async def captureanalyze():
    pngpath = capturer.capture_active_window(config.app.screenshot_dir + time.ctime())
    npureply = npumodel.message(pngpath)
    ui.display_request(f"[Capture - NPU] {npureply}")
    #uvicorn.run("src.main:app", host="127.0.0.1", port=8005, reload=True)