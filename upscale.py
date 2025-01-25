import cv2
from cv2 import dnn_superres

def UpScale(path):
    # Create an SR object - only function that differs from c++ code
    sr = dnn_superres.DnnSuperResImpl_create()
     
    # Read image
    image = cv2.imread(path)
    # Read the desired model
    path = "EDSR_x4.pb"
    sr.readModel(path)
    sr.setModel("edsr", 4)
    result = sr.upsample(image)
    return result
    #cv2.imwrite("./upscaled3.png", result)


