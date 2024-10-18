from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from webcam import generate_frames


app = FastAPI()

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates")

# 비디오 스트리밍 경로
@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

# 기본 페이지 (웹브라우저에서 카메라 영상 확인)
@app.get("/")
async def main(request : Request):
    return templates.TemplateResponse("index.html", {"request": request})