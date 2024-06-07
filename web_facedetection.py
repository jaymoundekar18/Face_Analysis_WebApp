import streamlit as st
import cv2
from mtcnn import MTCNN
from PIL import Image
import numpy as np
st.title('Face Detection')

st.subheader("\n\n\n\n")


# # col1, col2, col3 = st.columns(3)
input= ['',"Face Detection","Face Extraction","Face Recognition"]
st.subheader("Select options from below")
button = st.selectbox(" ",input)

detector = MTCNN()

## Face bounding Box
def face_detect(img):
    image = Image.open(img)
    image = np.array(image)
    faces = detector.detect_faces(image)

    for face in faces:
        x,y,w,h = face['box']

        cv2.rectangle(image, (x,y),(x+w,y+h),(0,255,0),2)

    return st.image(image, caption='Detected Faces')
    


def face_extraction(img):

    image = Image.open(img)
    image = np.array(image)

    faces = detector.detect_faces(image)

    for face in faces:
        x,y,w,h = face['box']

        extracted_face = image[y:y+h, x:x+w]

        st.image(extracted_face, caption='Extracted Face')


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


# elif button ==input[3]:
#     pass