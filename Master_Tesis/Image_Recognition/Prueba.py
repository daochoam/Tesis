from Detect import Detector
import fnmatch
import cv2

path = 'Image_Recognition/7.jpg'

Bottles = cv2.imread(path, cv2.COLOR_BGR2RGB)
window_name = 'Bottle'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.imshow(window_name, Bottles)

# Create an instance of the Detector class
Obj_Detector = Detector(model_type="ML2R", score_thresh=0.8)
print(Obj_Detector)
# Initialize and load the model
predict = Obj_Detector.Predict()
# Check if the model was successfully loaded
if predict != -1:
    # Make predictions
    prediction = Obj_Detector.Image_Predict(Bottles, predict)
    # Perform image segmentation
    image_show = Obj_Detector.Image_Segment(Bottles, prediction)

    # # If you want to detect contours, uncomment this line
    Contornos = Obj_Detector.Detect_Contours(prediction)

    # Display the original image
    window_name = 'image'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, image_show)
    cv2.waitKey(0)
else:
    print('Failed to load the model. Please train the model first.')
