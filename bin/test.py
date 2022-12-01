from tensorflow import keras
import numpy as np
import pickle
import os
import cv2

BASE_DIR    = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODELS_DIR  = os.path.join(BASE_DIR, 'models')
LABELS_DIR  = os.path.join(BASE_DIR, 'labels')
HEIGHT, WIDTH = 64, 64
DIM = (HEIGHT, WIDTH)
# rede 72 curr = '20221029_1707'
curr = '20221029_1707'
model = keras.models.load_model(MODELS_DIR+'/model-'+curr+'.h5')
labels = pickle.loads(open(LABELS_DIR+'/labels-'+curr+'.pickle', "rb").read())
print(len(labels))

def __draw_label(img, text, pos, bg_color):
   font_face = cv2.FONT_HERSHEY_SIMPLEX
   scale = 1
   color = (255, 255, 255)
   thickness = cv2.FILLED
   margin = 2
   txt_size = cv2.getTextSize(text, font_face, scale, thickness)

   end_x = pos[0] + txt_size[0][0] + margin
   end_y = pos[1] - txt_size[0][1] - margin

#    cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
   cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)
   
# Open the device at the ID 0
# Use the camera ID based on
# /dev/videoID needed
cap = cv2.VideoCapture(0)

object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=70)
#Check if camera was opened correctly
if not (cap.isOpened()):
    print("Could not open video device")

# 2) fetch one frame at a time from your camera
while(cap):
    
    # frame is a numpy array, that you can predict on 
    ret, frame = cap.read()
    height, width, _ = frame.shape

    # resize image
    resized = np.expand_dims(cv2.resize(frame, DIM), axis=0)

    # 3) obtain the prediction
    # depending on your model, you may have to reshape frame
    prediction = model.predict(resized)
    result = labels[prediction.argmax(axis=1)[0]]
    print(prediction)
    print(result)
    # you may need then to process prediction to obtain a label of your data, depending on your model. Probably you'll have to apply an argmax to prediction to obtain a label.

    # 4) Adding the label on your frame
    __draw_label(frame, f'{result}', (40,40), (0,0,0))

    # 5) Display the resulting frame
    cv2.imshow("preview",frame)
   
    #Waits for a user input to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
