from fastapi import FastAPI, Request, Form
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from webcam import generate_frames
import serial

app = FastAPI()

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates")

# 비디오 스트리밍 경로
@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

# 기본 페이지 (웹브라우저에서 카메라 영상 확인)
@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 사용자 입력을 받는 페이지
@app.get("/input")
async def input_page(request: Request):
    return templates.TemplateResponse("input.html", {"request": request})

# 사용자 입력을 처리하는 엔드포인트
@app.post("/send_signal")
async def send_signal(action: str = Form(...)):
    arduino = serial.Serial('/dev/ttyUSB0', 9600)
    
    if action == '졸음운전':
        arduino.write(b'1')
        signal = "Drowsy driving detected"
    elif action == '음주운전':
        arduino.write(b'2')
        signal = "Drunk driving detected"
    elif action == '물건찾는다':
        arduino.write(b'3')
        signal = "Searching for an item"
    elif action == '통화':
        arduino.write(b'4')
        signal = "Talking on the phone"
    elif action == '휴대폰 조작':
        arduino.write(b'5')
        signal = "Using the phone"
    elif action == '운전자 폭행':
        arduino.write(b'6')
        signal = "Driver assault detected"
    else:
        arduino.write(b'0')
        signal = "Unknown action"

    # 프론트엔드로 신호 전달
    return JSONResponse(content={"status": "signal sent", "signal": signal})

# 필요한 라이브러리 설치
# pip install fastapi uvicorn serial