import cv2
import mediapipe as mp
import random
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

cam = cv2.VideoCapture(0)

computerchoices = ["Rock", "Paper", "Scissor"]
computerinput = random.choice(computerchoices)
currenttime = time.time()
counter = 0
result = ""
userinput = ""

while True:
    ret, frame = cam.read()
    
    if not ret:
        print("Camera not detected!")
        break

    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    mycoordinatedata = {}

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            for id, lm in enumerate(hand_landmarks.landmark):
                x = int(lm.x * width)
                y = int(lm.y * height)
                mycoordinatedata[id] = (x, y)

            
            if all(k in mycoordinatedata for k in [8,5,12,9,16,13,20,17]):
                
                if (
                    mycoordinatedata[8][1] < mycoordinatedata[5][1] and
                    mycoordinatedata[12][1] < mycoordinatedata[9][1] and
                    mycoordinatedata[16][1] < mycoordinatedata[13][1] and
                    mycoordinatedata[20][1] < mycoordinatedata[17][1]
                ):
                    userinput = "Paper"
               
                elif (
                    mycoordinatedata[8][1] < mycoordinatedata[5][1] and
                    mycoordinatedata[12][1] < mycoordinatedata[9][1]
                ):
                    userinput = "Scissor"
                
                else:
                    userinput = "Rock"

            cv2.putText(frame, userinput, (200, 200), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 4)

    
    if time.time() - currenttime >= 1:
        currenttime = time.time()
        counter += 1

        if counter == 5:  
            print(f"Computer: {computerinput} | User: {userinput}")

            if userinput == computerinput:
                result = "Draw!"
            elif (userinput == "Rock"     and computerinput == "Scissor") or \
                 (userinput == "Scissor"  and computerinput == "Paper") or \
                 (userinput == "Paper"    and computerinput == "Rock"):
                result = "You Win!"
            else:
                result = "Computer Wins!"

            
            computerinput = random.choice(computerchoices)
            counter = 0

    
    cv2.putText(frame, result, (450, 650), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 4)
    cv2.putText(frame, str(5 - counter), (950, 80), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 4)

    cv2.imshow("Rock Paper Scissors", frame)

    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()
