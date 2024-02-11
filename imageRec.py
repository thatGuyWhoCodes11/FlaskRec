from facedb import FaceDB
from PIL import Image
import cv2 as cv
import numpy as np
import uuid

db = FaceDB(path="./facesDatabase")

def drawRectangle(img):
    # preparing image for rectangle drawing
    if(not isinstance(img,Image.Image)):
        img = Image.open(img)
    arrayImage = np.asarray(img)
    BGR_image = cv.cvtColor(arrayImage, cv.COLOR_BGR2RGB)
    # getting x and y values for rectangles
    rects = db.get_faces(img, only_rect=True)
    # drawing rectangles and inserting numbers
    i = 0
    for rect in rects:
        x1 = rect.x
        x2 = rect.x+rect.width
        y1 = rect.y
        y2 = rect.y+rect.height
        BGR_image = cv.rectangle(img=BGR_image, color=(
            0, 0, 254), pt1=(x1, y1), pt2=(x2, y2), thickness=2)
        BGR_image = cv.putText(fontScale=1, text=str(i), img=BGR_image, color=(
            0, 0, 254), fontFace=cv.FONT_HERSHEY_COMPLEX, thickness=2, org=(rect.x+15, rect.y+30))
        i = i+1
    return Image.fromarray(cv.cvtColor(BGR_image, cv.COLOR_RGB2BGR))

def faceCropper(img):
    # preparing image for cropping
    if(not isinstance(img,Image.Image)):
        img = Image.open(img)
    arrayImage = np.asarray(img)
    BGR_image = cv.cvtColor(arrayImage, cv.COLOR_BGR2RGB)
    # getting x and y values for rectangles
    rects = db.get_faces(img, only_rect=True)
    cropped_faces = []
    for rect in rects:
        x1 = rect.x-np.minimum(10, rect.x)
        x2 = np.minimum(rect.x+rect.width+10,rect.x+rect.width)
        y1 = rect.y-np.minimum(10, rect.y)
        y2 = np.minimum(rect.y+rect.height+10,rect.y+rect.height)
        cropped_faces.append(Image.fromarray(cv.cvtColor(BGR_image[y1:y2, x1:x2].copy(), cv.COLOR_RGB2BGR)))
    return cropped_faces

# give an id to each added faces in the cropped faces object
def addFaces(img):
    croppedFaces=faceCropper(img)
    croppedFaces[0].show()
    i = 0
    faces = []
    for face in croppedFaces:
        id = db.add(img=face, id=str(uuid.uuid4()))
        faces.append(id)
    return faces

def editFacesInfo(faceInfos):
    for faceInfo in faceInfos:
        db.update(id=faceInfo["id"],name=faceInfo["name"])
    return
def recognizeFaces(img):
    croppedFaces=faceCropper(img)
    results=[]
    for croppedFace in croppedFaces:
        result=db.recognize(img=croppedFace,include="name")
        if(result == None):
            results.append({"name":"not recognized"})
        else:
            results.append(result[0])
    return results
    