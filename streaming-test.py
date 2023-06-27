from ultralytics import YOLO
import cv2
from ultralytics.yolo.utils.plotting import Annotator
import torch

model = YOLO('yolov8n.pt')

cap = cv2.VideoCapture(0) #use opencv to get the webcam as a capture device
cap.set(3, 640) #CV_CAP_PROP_FRAME_WIDTH
cap.set(4, 480) #CV_CAP_PROP_FRAME_HEIGHT



def find_new_objects(old_objects, new_objects, threshold):
    """
    This function takes in the objects from two consecutive runs and attempts to match them to sort out which bounding boxes
    are new and which have just moved slightly
    """
    matches = []
    unmatched = []

    for new_box in new_objects:
        matched = False
        for old_box in old_objects:
            new_coords = new_box.xyxy[0] #get the coordinates of the new box
            old_coords = old_box.xyxy[0] #get the coordinates of the old box
            new_class = new_box.cls[0] #get the class of the new box
            old_class = old_box.cls[0] #get the class of the old box

            #check if the potential match has the same class
            if new_class == old_class:
                
                #check if the coordinates are similar enough
                diff = torch.sub(new_coords, old_coords) #subtract the old coordinates from the new coordinates
                diff = torch.abs(diff)
                diff = torch.sum(diff)

                #if it's below the threshold, add to the matches
                if diff < threshold:
                    matches.append(new_box)
                    matched = True
        if not matched:
            unmatched.append(new_box)

    
    #print("Matched classes:")
    #for item in matches:
    #    print(model.names[int(item.cls[0])])
    #print("Unmatched classes:")
    for item in unmatched:
        print(f'New object detected: {model.names[int(item.cls[0])]}')
        

while True:
    _, frame = cap.read()
    
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = model.predict(img)


    for r in results: #what does this do? Are there ever multiple results?
        
        annotator = Annotator(frame)
        boxes = r.boxes

        new_objects = boxes

        #print("object classes detected: ")
        for box in boxes:
            
            b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls[0].item() #get class labels
            #print(f'class number: {int(c)}; class name: {model.names[int(c)]}') #print out the class number and name of the object detected

            #actually annotate the image
            annotator.box_label(b, model.names[int(c)])

        #I love graceful error handling 
        try:
            #call the function to identify new objects
            find_new_objects(current_objects, new_objects, threshold=50)
        except:
            continue

    frame = annotator.result() #get the result from the annotator

    cv2.imshow('YOLO V8 Detection', frame) #show the image we have generated

    if cv2.waitKey(1) & 0xFF == ord('q'): #quit when the 'q' key is pressed
        break

    current_objects = new_objects

cap.release()
cv2.destroyAllWindows()