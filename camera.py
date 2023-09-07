
import cv2
import time
import datetime
import smtplib
import os
from email.message import EmailMessage

def send_email():
    msg = EmailMessage()
    #this is sent when a face is detected on your camera
    msg.set_content("a face was detected on your camera")
    msg['Subject'] = f'FACE DETECTED'
    msg['From'] = 'matthewchavis8@gmail.com' #enter sender email
    msg['To'] = 'matthewchavis8@gmail.com' #enter desination email

    email_user = os.environ.get('EMAIL_USER') #set email_user system
    email_password = os.environ.get('EMAIL_PASSWORD') #set system variable
    
    #this connects to the smtp server using ssl/tls
    server = smtplib.SMTP_SSL('smtp.email.com', 465) #secured connection 
    #this method greets the server and initiates communication
    server.ehlo()
    #this method logs in to the email account
    server.login(email_user, email_password)

    #this sends the email
    server.send_message(msg)
    print("E-mail sent!")
    #this closes the connection after ending
    server.quit

#ensures that code is only executed if script is being run directly
if __name__ == "__main__":
    #this initializes video for caputuring video
    #represensts the default webcam(index0)
    cap = cv2.VideoCapture(0)

    #this loads pretrained model for face detectin
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    #gets video frame
    frame_size = (int(cap.get(3)), int(cap.get(4)))
    #video format
    video_format = cv2.VideoWriter_fourcc(*"mp4v")

    #now initializing variables
    detection = False
    detection_stopped_time = None
    time_started = False
    SECONDS_TO_RECORD_AFTER_DETECTION = 5

    #infinite loop that will continue till broken by break statement
    while True:
        #reads frames
        _, frame = cap.read()
        #this method converts frames to grey scale
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #Detects face within greyscale frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if(len(faces) > 0):
            if detection:
                time_started = False
            else:
                detection = True
                current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                out = cv2.VideoWriter(f"{current_time},mp4", video_format, 20.0, frame_size)
                print("started recording!")
                send_email()
        elif detection:
            if time_started:
                if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                    detection = False
                    time_started = False
                    out.release()
                    print("stopped recording!")
                else:
                    timer_started = True
                    detection_stopped_time = time.time()
            if detection:
                out.write(frame) #writes frame
            cv2.imshow("Camera", frame) #displays frame
            if cv2.waitkey(1) == ord('q'): #exit key
                break
    out.release()   
    cap.release()
    cv2.destroyAllWindows()         


