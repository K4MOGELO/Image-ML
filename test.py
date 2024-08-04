import cv2
import os
import numpy as np




def get_ppm(img_path):
    #-------------------- Pothole detector----------------------------
    
    #reading test image
    img = cv2.imread(img_path) #image name

    #reading label name from obj.names file
    with open(os.path.join("project_files",'obj.names'), 'r') as f:
        classes = f.read().splitlines()

    #importing model weights and config file
    net = cv2.dnn.readNet('project_files/yolov4_tiny.weights', 'project_files/yolov4_tiny.cfg')
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)
    classIds, scores, boxes = model.detect(img, confThreshold=0.6, nmsThreshold=0.4)

    pixel_area = []

    #detection 
    for (classId, score, box) in zip(classIds, scores, boxes):
        area = box[2] * box[3]
        pixel_area.append(area)
        
        cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                    color=(0, 255, 0), thickness=2)
        
    print(pixel_area)
    
    cv2.imshow("pothole",img)
    cv2.imwrite("result1"+".jpg",img) #result name
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #-----------------------------End of Pothole Detector------------------------------------ 
    
    #------------------------------Getting Pixel Per Meter-----------------------------------
    
    # Load the image
    image = cv2.imread(img_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect edges (you may need to adjust the thresholds)
    edges = cv2.Canny(gray, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assume the largest contour is our reference object (you may need to add logic to identify it)
    contour = max(contours, key=cv2.contourArea)

    # Get the bounding box of the reference object
    x, y, w, h = cv2.boundingRect(contour)

    # Known width or height of the reference object in meters
    known_width_meters = 0.5  

    # Width of the reference object in pixels
    reference_width_pixels = w

    # Calculate pixels per meter
    ppm = reference_width_pixels / known_width_meters
    
    #-------------------------End of Pixel Per Meter----------------------
    
    
    
    meter_area = []
    
    for pixel in pixel_area:
        meter_distance = pixel / ppm #getting the actual predicted area of pothole
        meter_area.append(meter_distance)
        
    print (meter_area)


    

get_ppm('img.jpg')