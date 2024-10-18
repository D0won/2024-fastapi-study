import cv2
import os
import time
from datetime import datetime

camera = cv2.VideoCapture(0)

# 프레임을 저장할 디렉토리
output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)

def generate_frames():
    while True:
        # 카메라에서 프레임 읽기
        success, frame = camera.read()
        if not success:
            break
        else:
            # 프레임을 JPEG 형식으로 변환
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = os.path.join(output_dir, f"frame_{timestamp}.jpg")
            with open(filename, "wb") as f:
                f.write(frame)

            # 프레임을 클라이언트에게 전송 (multipart/form-data 형식)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
            # 파일 삭제
            os.remove(filename)
            # 프레임 삭제
            del frame
            del buffer
            time.sleep(1/60)