import streamlit as st
import cv2
from PIL import Image
import numpy as np
from facenet_pytorch import MTCNN
# import deepface
from deepface import DeepFace
import sys
st.title('Face App')

st.subheader("\n\n\n\n")


input= ['',"Face Detection","Face Extraction","Face Verification","Face Recognition","Face Analysis"]
st.subheader("Select options from below")
button = st.selectbox(" ",input)

detector = MTCNN()

#################################################

## Face bounding Box
def face_detect(img):
    image = Image.open(img)
    image = np.array(image)
   
    faces, _ = detector.detect(image)


    for face in faces:
        
        x,y,w,h = map(int, face)

        cv2.rectangle(image, (x,y),(w,h),(0,255,0),2)


    return st.image(image, caption='Detected Faces')
    

#################################################

## Face Extraction
def face_extraction(img):

    image = Image.open(img)
    image = np.array(image)

    faces, _ = detector.detect(image)

    for face in faces:
        x,y,w,h = map(int, face)

        extracted_face = image[y:h, x:w]

        st.image(extracted_face, caption='Extracted Face')


#################################################

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


#################################################

## Face Recognition
def face_recognition(img):

    image = Image.open(img)
    image = np.array(image)

    result = DeepFace.find(img_path=image, db_path="Dataset")
    x,y = result[0].shape

    if x > 0:

        st.success(f"Number of face detected : {len(result)}")
        st.write("Face matches with : ")
        for i in range(len(result)):
                a = result[i]['identity'][0]
                b = a.split("/")
                pname = b[1]

                st.write(f"**{pname}**")
                

    else :
        st.error(f"No match found in the database")

#################################################

## Face Analysis
def face_analysis(img):
    
    image = Image.open(img)
    image = image.resize((350,350))
    image = np.array(image)

    #data = DeepFace.analyze(image,  actions=['emotion'])
    #old = data[0]

    #for i in old.keys():
     
        #if isinstance(old[i], dict):
            #continue

        #st.write(f"{i} : {old[i]}")

    # for key, value in data[0].items():
    #     st.write(f"{key} : {value}")

    #act = ['age', 'gender'] #,'emotion', 'race'
    my = dict()

    
    data = DeepFace.analyze(image, actions='age')
    old = data[0]
    for i in old.keys():
        if isinstance(old[i], dict):
            continue
        my[i.capitalize()] = old[i]
        
    for i, val in my.items():
        
        if isinstance(my[i], str):
            st.write(f":green[{i} : {my[i].capitalize()}]")

        elif isinstance(my[i], float):
            st.write(f":green[{i} : {my[i]*100}]")

        else:
            st.write(f":green[{i} : {my[i]}]")

#####################################################################################################################################


## Different processes
if button ==input[1]:
    img = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

    st.write("OR")
    st.write("Take photo from camera") 

    cam = st.camera_input("")


    if img is not None:
        
        face_detect(img)

    elif cam is not None:
              
        face_detect(cam)
        

#################################################

elif button ==input[2]:

    img = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

    st.write("OR")
    st.write("Take photo from camera") 

    cam = st.camera_input("")

    if img is not None:

        face_extraction(img)
    
    elif cam is not None:
        face_extraction(cam)


#################################################

elif button ==input[3]:
        
    img1 = st.file_uploader("Upload first image", type=["png", "jpg", "jpeg"])
    
    img2 = st.file_uploader("Upload Second image", type=["png", "jpg", "jpeg"])

    if img1 is not None and img2 is not None:

        face_verification(img1, img2)


#################################################

elif button ==input[4]:
    
    st.subheader("Face Recognition")

    img = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

    st.write("OR")
    st.write("Take photo from camera") 

    cam = st.camera_input("")

    if img is not None:

        face_recognition(img)
    
    elif cam is not None:
        face_recognition(cam)

   

#################################################

elif button ==input[5]:
    
    st.subheader("Face Attributes")

    img = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

    st.write("OR")

    st.write("Take photo from camera") 

    cam = st.camera_input("")

   

    if img is not None:


        st.subheader("Provided Image")
        st.image(img)

        face_analysis(img)
    
    elif cam is not None:

        st.subheader("Provided Image")
        st.image(cam)

        #face_analysis(cam)
