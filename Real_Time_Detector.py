import numpy as np
import cv2
import tensorflow as tf
from keras.models import load_model
from tensorflow.keras.preprocessing import image
import time
import serial


ser1 = serial.Serial()
ser1.baudrate = 9600
ser1.port = 'COM3'
ser1.open()

fire_cascade = cv2.CascadeClassifier('cascade.xml')
model = load_model('fire_detection_model.h5')

cap = cv2.VideoCapture(0)  # Start video capturing
count = 0
target_size = (224, 224)  # Set target size to (224, 224)

while cap.isOpened():
    ret, img = cap.read()  # Capture a frame
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
    fire = fire_cascade.detectMultiScale(img, 12, 5)  # Test for fire detection

    for (x, y, w, h) in fire:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Highlight the area of image with fire
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        resized_img = cv2.resize(roi_color, target_size)  # Resize to (224, 224)
        resized_img = resized_img.astype('float') / 255.0
        resized_img = image.img_to_array(resized_img)

        # Add batch dimension
        resized_img = np.expand_dims(resized_img, axis=0)  # Shape becomes (1, 224, 224, 3)
        
        pred1 = model.predict(resized_img, verbose=0)
        
        predicted_class = np.argmax(pred1, axis=1)

        # Define class names
        class_names = ['fire', 'no_fire']

        # Output the prediction
        print("Predicted class:", class_names[predicted_class[0]])
        
        if class_names[predicted_class[0]] == 'fire':
            print("message sent")
            ser1.write(str.encode('p'))
        # Convert prediction to string and handle encoding
        # print('Fire is detected..!' + str(count))  
        count += 1
        time.sleep(0.2)  # Wait
        
    cv2.imshow('img', img)
    ser1.write(str.encode('s'))
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break

ser1.close()
cap.release()
cv2.destroyAllWindows()
