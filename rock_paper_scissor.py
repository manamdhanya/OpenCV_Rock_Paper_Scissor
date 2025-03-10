import cv2
import mediapipe as mp
import random
import time

np_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

cam = cv2.VideoCapture(0)


mycoordinatedata = {} 

myfingers = []
userinput = ""
computerchoices = ["Scissor","Paper","Rock"]
computerinput = random.choice(computerchoices)
currenttime = time.time()
counter = 0
result = ""

while True:
    _, image = cam.read()
    image = cv2.flip(image, 1)
    results = hands.process(image)
    height, width, _ = image.shape
    checktime = time.time()
    if results.multi_hand_landmarks:
        for handid, hand_landmarks in enumerate(results.multi_hand_landmarks):
            np_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
            for id, lms in enumerate(hand_landmarks.landmark): 
                x_cord = lms.x * width
                y_cord = lms.y * height
                mycoordinatedata[id] = (x_cord,y_cord)
                if all(k in mycoordinatedata for k in [8, 5, 12, 9, 16, 13, 20, 17, 4, 1]):
                    if (mycoordinatedata[8][1] < mycoordinatedata[5][1] and  mycoordinatedata[12][1] < mycoordinatedata[9][1] and  mycoordinatedata[16][1] < mycoordinatedata[13][1] and  mycoordinatedata[20][1] < mycoordinatedata[17][1]):
                        userinput = "Paper"
                        cv2.putText(image,userinput,(200,200),cv2.FONT_HERSHEY_COMPLEX,7,(255,255,255),4,cv2.LINE_AA)
                    elif (mycoordinatedata[8][1] < mycoordinatedata[5][1] and  mycoordinatedata[12][1] < mycoordinatedata[9][1] and  mycoordinatedata[16][1] > mycoordinatedata[13][1] and  mycoordinatedata[20][1] > mycoordinatedata[17][1]):
                        userinput = "Scissor"
                        cv2.putText(image,userinput,(200,200),cv2.FONT_HERSHEY_COMPLEX,7,(255,255,255),4,cv2.LINE_AA)
                    else:
                        userinput = "Rock"
                        cv2.putText(image,userinput,(200,200),cv2.FONT_HERSHEY_COMPLEX,7,(255,255,255),4,cv2.LINE_AA)
                else:
                    print("Some keys are missing.")
        if checktime -  currenttime >= 1:
            print(5-counter)
            currenttime = time.time()
            counter += 1
            if counter == 5:
                print(f"Computer: {computerinput}\n User: {userinput}")
                counter = 0
                computeroldchoice = computerinput
                if userinput == "Scissor" and computerinput == "Paper":
                    result = "You Win"
                elif userinput == "Paper" and computerinput == "Scissor":
                    result = "You Win"
                elif userinput == "Rock" and computerinput == "Paper":
                    result = "You Win"
                elif userinput == computerinput:
                    result = "Drawn"
                else:
                    result = "Computer Wins"
                computerinput = random.choice(computerchoices)
    


    cv2.putText(image, result, (500, 700), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 105, 97), 4, cv2.LINE_AA)
    cv2.putText(image, str(5 - counter), (1000, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 105, 97), 4, cv2.LINE_AA)
    cv2.imshow("Project", image)
    if cv2.waitKey(1) & 0xFF == 27:  
        break

cam.release()
cv2.destroyAllWindows()
