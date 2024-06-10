import streamlit as st
import cv2
from PIL import Image
import numpy as np
from facenet_pytorch import MTCNN
from deepface import DeepFace
from pathlib import Path

st.title('Face Detection')

st.subheader("\n\n\n\n")



input= ['',"Face Detection","Face Extraction","Face Verification","Face Recognition"]
st.subheader("Select options from below")
button = st.selectbox(" ",input)

detector = MTCNN()

## Face bounding Box
def face_detect(img):
    image = Image.open(img)
    image = np.array(image)
   
    faces, _ = detector.detect(image)


    for face in faces:
        
        x,y,w,h = map(int, face)

        cv2.rectangle(image, (x,y),(w,h),(0,255,0),2)


    return st.image(image, caption='Detected Faces')
    

## Face Extraction
def face_extraction(img):

    image = Image.open(img)
    image = np.array(image)

    faces, _ = detector.detect(image)

    for face in faces:
        x,y,w,h = map(int, face)

        extracted_face = image[y:h, x:w]

        st.image(extracted_face, caption='Extracted Face')


## Face Verification

def face_verification(img1, img2):
    
    image1 = Image.open(img1)
    image1 = np.array(image1)
    image2 = Image.open(img2)
    image2 = np.array(image2)
    
    result = DeepFace.verify(image1, image2)
    res = result['verified']
    if res:
        st.success("Both persons are same")
    else:
        st.error("Both persons are different")


## Face Recognition
def face_recognition(img):
    
    result = DeepFace.find(img_path=img, db_path=r"D:\code\Prac\New folder")
    x,y = result[0].shape
    if x > 0:
        a = result[0]['identity'][0]
        b = a.split("\\")
        pname = b[4]

        st.write(f"Face matches with : {pname}")

    else :
        st.write(f"No match found in the database")


    
if button ==input[1]:
    img = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

    st.write("Or Take photo from camera") 

    cam = st.camera_input("")


    if img is not None:
        
        face_detect(img)

    elif cam is not None:
              
        face_detect(cam)
        

elif button ==input[2]:

    img = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

    st.write("Or Take photo from camera") 

    cam = st.camera_input("")

    if img is not None:

        face_extraction(img)
    
    elif cam is not None:
        face_extraction(cam)


elif button ==input[3]:
        
    img1 = st.file_uploader("Upload first image", type=["png", "jpg", "jpeg"])
    
    img2 = st.file_uploader("Upload Second image", type=["png", "jpg", "jpeg"])

    if img1 is not None and img2 is not None:

        face_verification(img1, img2)


elif button ==input[4]:
    
    #img = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
    img = st.text_input("Enter image path")
    #st.write("Or Take photo from camera") 
    
    path = Path(img)
    #cam = st.camera_input("")
    
    if img:
        
        face_recognition(path)
    
    #elif cam is not None:
       # face_recognition(cam)
