import cv2
import sys
import mediapipe as mp

# mediapipe 객체
mp_drawing = mp.solutions.drawing_utils
mp_drawing_style = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands  # 손 인식

cap = cv2.VideoCapture(0)

if not cap.isOpened(): # 카메라 정상동작 확인
    print("카메라 오류")
    sys.exit(1) # 종료

hands = mp_hands.Hands() # 손 인식 객체 생성

while True:
    res,frame = cap.read()  # 카메라 데이터

    if not res: # 프레임 감지 확인
        print("프레임을 읽을 수 없음")
        break

    frame = cv2.flip(frame,1) # 좌우반전
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # BGR -> 
    results = hands.process(image) # image에서 손을 찾고 결과 리턴

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_style.get_defalt_hand_landmarks_style(),
                mp_drawing_style.get_defalt_hand_connections_style(),
            )
    
    cv2.imshow("HandTracking",frame) # 출력

    key = cv2.waitKey(5) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()
cap.release()