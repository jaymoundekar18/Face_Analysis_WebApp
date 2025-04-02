# Importing all the required libraires 
import cv2
from PIL import Image, ImageTk
import customtkinter as ct
import tkinter as tk
from tkinter import ttk
import facenet_pytorch
from tkinter import messagebox
from facenet_pytorch import MTCNN
from deepface import DeepFace
import numpy as np

# Setting the app appearance and theme
ct.set_appearance_mode("system")
ct.set_default_color_theme("green")
detector = MTCNN()

class App(ct.CTk):
    def __init__(self):
        super().__init__()

        self.title("Face App")
        self.geometry("700x700")
        self.iconbitmap(r"D:\code\MTCNN_Prac\FACE APPS\FaceApp\face1.ico")

        self.faceDetection = False

    # Setting up the main frame
        self.main_frame = ct.CTkScrollableFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        
    # Title Frame
        self.titlelabelframe = ct.CTkFrame(self.main_frame, width=600, height=100, fg_color="transparent")
        self.titlelabelframe.pack(pady=20)

    # Title label inside title frame
        self.titlelabel = ct.CTkLabel(self.titlelabelframe, text="Face App",fg_color="transparent",text_color=("black"),font=("arial black",32))
        self.titlelabel.pack()
        
    # Setting up Camera Frame
        self.cameraframe = ct.CTkFrame(self.main_frame, width=500, height=300)
        self.cameraframe.pack()

    # Display Camera window in the camera frame
        self.camera_label = ct.CTkLabel(self.cameraframe,text="")
        self.camera_label.pack()
        
    # Calling the video stream function
        self.video_stream = cv2.VideoCapture(0)
        self.show_cam()

    # Setting up Button Frame
        self.dropbarframe = ct.CTkFrame(self.main_frame, width=600, height=100, fg_color="transparent")
        self.dropbarframe.pack(pady=20)

    # Initializing Buttons 
        self.capBtn = ct.CTkButton(self.dropbarframe,text="Capture \n Image",command=self.capture_image)
        self.capBtn.grid(row=0, column=0,padx=10)

        self.detectBtn = ct.CTkButton(self.dropbarframe,text="Live Face \n Detection", command=self.detectFace)
        self.detectBtn.grid(row=0, column=1,padx=10)

        self.recogBtn = ct.CTkButton(self.dropbarframe,text="Face \n Recognition", command=self.recogFace)
        self.recogBtn.grid(row=0, column=2,padx=10)

        self.analyzeBtn = ct.CTkButton(self.dropbarframe,text="Face \n Analysis", command=self.analysisFace)
        self.analyzeBtn.grid(row=0, column=3,padx=10)

    ## Display Frame to display all the click button function
        self.displayFrame = ct.CTkFrame(self.main_frame, width=600, height=300)
        self.displayFrame.pack()

    # Show captured image
        self.capImageLabel = ct.CTkLabel(self.displayFrame, text=None)
        self.capImageLabel.pack(pady=20)

    # Show captured info
        self.capInfo = ct.CTkLabel(self.displayFrame, text="")
        self.capInfo.pack(pady=20)
        

    ## End button Frame 
        self.endFrame = ct.CTkFrame(self.main_frame, width=600, height=300)
        self.endFrame.pack()    

    # End Button
        self.endButton = ct.CTkButton(self.endFrame,text="Close App", command=self.close_app)
        self.endButton.pack()


## Working functions

# Close app function

    def close_app(self):
        if messagebox.askokcancel("Quit","Do you want to quit the application?"):
            self.destroy()


    
# Camera function to display realtime video stream
    def show_cam(self):

        if self.faceDetection:
            ret, frame = self.video_stream.read()
            if ret:
                
                frame_pil = Image.fromarray(frame)
                faces, _ = detector.detect(frame_pil)

                if faces is not None:
                    self.capInfo.configure(text="")
                    for face in faces:
                        x, y, w, h = map(int, face)
                        cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)
                        
                    newframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(newframe)
                    image = image.transpose(Image.FLIP_LEFT_RIGHT)
                    image = ImageTk.PhotoImage(image)
                
                    self.camera_label.configure(image=image)
                    self.camera_label.image = image

                else:
                    self.capInfo.configure(text="No Face Detected")

            self.after(1, self.show_cam)


        else:
            ret, frame = self.video_stream.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                image = Image.fromarray(image)
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
                image = ImageTk.PhotoImage(image)

                self.camera_label.configure(image=image)
                self.camera_label.image = image

            self.after(1, self.show_cam)


    
# Clear display frame

    def clear_display(self):
        self.capInfo.configure(text="")
        self.capImageLabel.configure(image="")
        self.after_cancel(self.show_cam)
        self.faceDetection = False
        print("DISPLAY FRAME CLEARED")

# Capture image from the video stream
    def capture_image(self):
        self.clear_display()
        # self.faceDetection = False
        ret, frame = self.video_stream.read()
        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        image = Image.fromarray(image)
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
        image = ImageTk.PhotoImage(image)
        self.capImageLabel.configure(text="",image=image)
        self.capImageLabel.image=image
        # self.capInfo.configure(text="IMAGE CAPTURED",text_color=("green"),font=("arial black",24))
        print("IMAGE CAPTURED SUCCESSFULLY \n")
        messagebox.showinfo("","Image captured Successfully !")


# Live Face Detection

    def detectFace(self):
        self.clear_display()
        self.faceDetection = True
        print("FACE DETECTION STARTED \n")
        self.capImageLabel.configure(text="")
        

# Face Recognition

    def recogFace(self):
        
        self.clear_display()
        print("FACE RECOGNITION STARTED \n")

        ret, frame = self.video_stream.read()

        if ret:

            image = np.array(frame)
            self.capImageLabel.configure(text="Searching!! \n DO NOT CLOSE THE WINDOW!")

            try:

                result = DeepFace.find(img_path=image, db_path=r"D:\code\MTCNN_Prac\vsd")
                x,y = result[0].shape

                if x > 1:

                    print(f"Number of face detected : {len(result)}")
                    print("Face matches with : ")
                    for i in range(len(result)):
                            a = result[i]['identity'][0]
                            b = a.split("\\")
                            pname = b[4]

                            self.capImageLabel.configure(text="Face matches with " + pname.capitalize())
                            print(f"{pname}")

                else :
                    print(f"No match found in the database")
                    self.capImageLabel.configure(text="No match found in the database")

            except:
                print("Face Capture error")
                self.capImageLabel.configure(text="FACE NOT CAPTURED PROPERLY!")


# Face Analysis

    def analysisFace(self):
        self.clear_display()
        print("FACE ANALYSIS STARTED \n")
        self.capImageLabel.configure(text="Analyzing!! \n PLEASE DO NOT CLOSE THE WINDOW!")

        ret, frame = self.video_stream.read()
        if ret:
            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            image = Image.fromarray(image)
            image = np.array(frame)

            try:
                print("Analyzing")
                data =  DeepFace.analyze(image)
                print(data)

                lst = ''
                for i in data[0]:
                        
                        if isinstance(data[0][i], dict):
                            continue
                        print(i)

                        lst += f"{i} : {data[0][i]}\n " 

                self.capImageLabel.configure(text=f"Face Description :\n\n {lst.title()} ")

            except:
                print("Face Capture error")
                self.capImageLabel.configure(text="FACE NOT CAPTURED PROPERLY!")
            
                
                
## Main function to run the app
if __name__ == "__main__":
    app = App()
    app.mainloop()









