import cv2
import face_recognition
import os
import glob
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime,wikipedia, pyjokes , pyfacebook
import openpyxl
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import  winsound
import smtplib



cap = cv2.VideoCapture(0)

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

rate = engine.getProperty("rate")
engine.setProperty('rate', 180)



engine.runAndWait()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()


def release_video():
    cap.release()
    cv2.destroyAllWindows()

def take_command():
    
    try:
        with sr.Microphone() as source:
            listener.energy_threshold=1000
            listener.adjust_for_ambient_noise(source,1.2)
            print('listening...')
            voice = listener.listen(source)
            global command
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'sarah' in command:
                command = command.replace('sarah', 'sarah')
                print(command)
    except:
        pass
    return command

def run_sarah():
    joker = pyjokes.get_joke()
    global timeNow_
    timeNow_ = datetime.datetime.now().strftime('%I:%M %p')
    TheTimeMSE = "Current time is {}".format(timeNow_)
    
    bankOfQue = {
    'time': TheTimeMSE,
    'hello' or 'hi' : 'hi my frind',
    'how are you': 'fine thank you i am ready for your question',
    'doing': 'nothing ... i am waitiing for your question',
    'faculty': 'faculty of artificial intelligance',
    'years': 'it is only 4 years ',
    'artificial intelligence': " artificial intelligence is a field, which combines computer science and robust datasets, to enable problem-solving. It also encompasses sub-fields of machine learning and deep learning",
    'projects': 'students  made a lot such as smart Homes, medical Robot, line follower cars, traffic lights ',
    'supervisor': 'The Dean of the College is Prof. Dr. Reda Saleh, Vice President for Community Service and Environmental Development, the Supervisor of the College, and the Vice Dean for Education and Student Affairs for Prof. Dr. Tamer Medhat Ibrahim',
    'joke': joker,
    "doctor's" : 'Tamer Medhat, Ali Siam, Mahmoud Yassin, Ahmed Seddik, Fatima Mohamed Talaat, Mohamed Abdo Qassem, Zainab Hassan, Noura Al-Rashidi',
    'assistant': 'Ahmed Hisham, Muhammad Al-Sardi, Abdel Mawli Youssef, Esraa Hassan, Mona Al-Najjar, Marwa Al-Siddiq, Mahmoud Al-Sabbagh and Samar Al-Badawihi',
    'fields': 'The College of Artificial Intelligence consists of 4 fields, the first is machine programming and information retrieval, the second is robotics and smart machines, the third is technology of integrated network systems, the fourth is data science and technology',
    'departments': 'The College of Artificial Intelligence consists of 2 departments, the General department and bio Artificial intelligence department ',
    'laboratories' : 'The College of Artificial Intelligence consists of 3 main halls and 7 laboratories',
    'history': 'First, let us introduce you to the Faculty of Artificial Intelligence. A decision was issued by the Prime Minister No. (871) on 4/8/2019 establishing the Faculty of Artificial Intelligence at Kafrelsheikh University. The Faculty of Artificial Intelligence at Kafrelsheikh University seeks to support excellence in Egypt and provide state institutions with knowledge to enhance Economic growth and improving the lives of Egyptians.',
    'college mission': "The college's mission is as follows: First, to support the state’s efforts to build and maintain innovation based on artificial intelligence, growth and productivity in Egypt by focusing on transformation efforts to deep learning and machine learning. Second, supporting the industrial and business sectors in Egypt with human cadres with artificial intelligence skills. Third, supporting the innovation sector in Egypt in the field of artificial intelligence and helping emerging companies to grow into Egyptian companies capable of global excellence.",
    'after graduate': 'After the graduation The student receives Bachelors degree in Artificial Intelligence ',
    'answer' and 'dont know' and 'help': 'just say any question about the facilty and i will answer you ',
    'search': ' if you want to search of something say i want to get information'
    }
    
    command = take_command()
    print(command)
    for i in bankOfQue.keys():
        if i in command:
            talk(bankOfQue[i])
            break
        
    if 'play' and 'video' in command:
           song = command.replace('play', '')
           talk('playing ' + song)
           pywhatkit.playonyt("artificial intelligance")
           
    elif 'thank' in command:
        talk("your welcome")
        
    elif i not in command:
        talk("please say again")
        
    else:
        talk('next question') 
    
    
cascPath=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


def face_extractor(frame):
    faces = faceCascade.detectMultiScale(
        frame,
        scaleFactor=1.1,
        minNeighbors=5,
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    for (x, y, w, h) in faces:
        global cropped_face
        cropped_face = frame[y:y+h+50, x:x+w+50]

    return cropped_face




def IterationN():
    i = 0
    cv2.imshow('Sarah', frame)
    for i in range(150):
        if cv2.waitKey(1) == 13 or i == 50: #13 is the Enter Key
            break
    cv2.destroyAllWindows()
    cap.release()



def Make_Folder():
    global name_of_folder
    name_of_folder = input("Enter your Name: ")
    parent_dir = r"E:\AI\Projects\security robot\Security Robot\Security Robot\registered"
    path_of_newdir = os.path.join(parent_dir, name_of_folder)
    the_final_path = os.mkdir(path_of_newdir)
    the_final_dir = r"E:\AI\Projects\security robot\Security Robot\Security Robot\registered\{}".format(str(name_of_folder))
    global the_final_Dir
    the_final_Dir = os.path.join(the_final_dir, name_of_folder)    
    
    


known_faces = []
known_names = []
known_faces_paths = []



registered_faces_path = r'E:\AI\Projects\security robot\Security Robot\Security Robot\registered/'

for name in os.listdir(registered_faces_path):
    images_mask = '%s%s\\*.jpg' % (registered_faces_path, name)
    images_paths = glob.glob(images_mask) 
    known_faces_paths += images_paths
    known_names += [name for x in images_paths]


def get_encodings(img_path):
    image = face_recognition.load_image_file(img_path)
    encodings = face_recognition.face_encodings(image)

    while len(encodings)>0:
        encoding= encodings[0]
        return encoding

known_faces = [get_encodings(img_path) for img_path in known_faces_paths]


def face_Recognition():
    count = 0
    global frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(frame_rgb)
        for face in faces: # top, right, bottom, left
            top, right, bottom, left = face
            face_code = face_recognition.face_encodings(frame_rgb, [face])[0]

            results = face_recognition.compare_faces(known_faces, face_code, tolerance=0.6)
            if any(results):
                name = known_names[results.index(True)]
                engine.say("I am sarah ")
                engine.say(f"Hi glad to see you {name}")
                engine.say("what do you want to ask about our faculty")
                engine.runAndWait()
                IterationN()
            else:
                engine.say("Can you type your your name please ")
                Make_Folder()
                while True:
                    ret, frame = cap.read()
                    if face_extractor(frame) is not False:
                        count += 1
                        face = cv2.resize(face_extractor(frame), (600, 600))
                                            
                        file_name_path = the_final_Dir  +" "+str(count) + '.jpg'
                        cv2.imwrite(file_name_path, face)
                        
                        cv2.imshow('Face Cropper', face)
                        
                    else:
                         print("Face not found")
                         pass

                    if cv2.waitKey(1) == 13 or count == 50: #13 is the Enter Key
                        break
                    
                release_video()
                engine.say("I am sarah ")
                engine.say(f"Hi my new friend glad to see you {name_of_folder}")
                engine.say("what do you want to ask about our faculty")
                engine.runAndWait()



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
    release_video()

times = datetime.datetime.now()
the_time_now = times.strftime("%H")
evining_time = ["20","21","22","23","00","01", "02", "03", "04", "05"]

if the_time_now in evining_time:
    night_detection()
    
    
else:
    
    face_Recognition()
    
    while True:
        run_sarah()
        if 'thank' in command:
            talk("goodbye")
            break



