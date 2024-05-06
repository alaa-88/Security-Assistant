import cv2
import  winsound
import smtplib



cap = cv2.VideoCapture(0)


def mail_alart(to,text):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('secbot88robot@gmail.com', 'secret508')
    server.sendmail('secbot88robot@gmail.com',to, text)
    winsound.Beep(500, 200)

def night_detection():
    while cap.isOpened():
        ret ,frame1 =cap.read()
        ret ,frame2 =cap.read()
        diff = cv2.absdiff(frame1 , frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5), 0)
        _, thresh = cv2.threshold(blur , 20, 255 , cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None , iterations =3)
        contours, _ =cv2.findContours(dilated , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if cv2.contourArea(c) <5000:
                continue
            x ,y, w , h =cv2.boundingRect(c)
            cv2.rectangle(frame1, (x, y), (x+w , y+h), (0,255,0) , 2)
            mail_alart("alaaelkady888@gmail.com","There is a movement in the college sir, you have to pay attention to this notice ")
            winsound.Beep(500, 200)
        cv2.imshow ('Sarah camera',  frame1)
        if cv2.waitKey(1) == ord('q'):
            break
        
        
    cap.release()
    cv2.destroyAllWindows()


night_detection()



