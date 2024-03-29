from fastapi import FastAPI, WebSocket
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
import PoseModule as pm
import asyncio

app = FastAPI()


detector = pm.poseDetector()

count = 0
direction = 0
form = 0
feedback = "Fix Form"

async def generate_frames():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break

        # 이미지 생성
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        if len(lmList) != 0:
            arm = detector.findAngle(img, 11, 13, 15)
            per = np.interp(arm, (60, 160), (100, 0))
            bar = np.interp(arm, (60, 160), (50, 380))
            global count, direction, form, feedback
            if arm > 170:
                form = 1
            if form == 1:
                if per == 0:
                    if arm < 60:
                        feedback = "Unfold"
                        if direction == 0:
                            count += 0.5
                            direction = 1
                    else:
                        feedback = "Fix Form"
                if per >= 98.5:
                    if arm <= 161:
                        feedback = "Fold"
                        if direction == 1:
                            count += 0.5
                            direction = 0
                    else:
                        feedback = "Fix Form"

        if form == 1:
            cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 0, 0), 2)
        
        cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2)

    
        _, buffer = cv2.imencode('.jpg', img)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
# FastAPI 서버
@app.get("/curl")
async def get_video():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace;boundary=frame")


