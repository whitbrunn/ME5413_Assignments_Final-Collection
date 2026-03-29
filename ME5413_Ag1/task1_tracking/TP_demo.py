import cv2
import sys
import os
import glob
 
 
if __name__ == '__main__' :
 
    # Set up tracker.
    # Instead of MIL, you can also use
    seq_id = 4
    seq_path = f"data/seq{str(seq_id)}"
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[6] # CSRT is wonderful for 1-4
 
 
    if tracker_type == 'BOOSTING':
        tracker = cv2.legacy.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.legacy.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.legacy.TrackerMedianFlow_create()
    if tracker_type == "CSRT":
        tracker = cv2.TrackerCSRT_create()
    if tracker_type == "MOSSE":
        tracker = cv2.legacy.TrackerMOSSE_create()
    
    # Read images
    img_paths = sorted(glob.glob(os.path.join(seq_path, "img", "*.jpg")))
    with open(f"data/seq{str(seq_id)}/groundtruth.txt") as g_f:
        gtbbox_lst = g_f.read().splitlines()

    frame = cv2.imread(img_paths[0])  # Read the image (same format as video frames)
    
    if frame is None:
        print("Error! No Frame0!")
    frame_h , frame_w, _ = frame.shape
    
    
    # Define an initial bounding box
    # bbox = (287, 23, 86, 320)
    b0_f = open(f"data/seq{str(seq_id)}/firsttrack.txt")
    b0_data = b0_f.readline()
    bbox = tuple([int(x) for x in b0_data.split(",")]) # bbox: (x,y,width,height)
 
    
 
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
 
    for id, img_path in enumerate(img_paths[1:]):
        # Read a new frame
        
        frame = cv2.imread(img_path)

        gt_line = gtbbox_lst[id+1]
        gtbbox = tuple([ int(x) for x in gt_line.split(',')])
        # Start timer
        timer = cv2.getTickCount()
 
        # Update tracker
        ok, bbox = tracker.update(frame)
        bbox = [int(x) for x in bbox]
        bbox = list(bbox)
        if bbox[0] + bbox[2] > frame_w:
            bbox[2] = frame_w - bbox[0]
        if bbox[1] + bbox[3] > frame_h:
            bbox[3] = frame_h- bbox[1]
        bbox = tuple(bbox)
 
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
 
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1) # Draw a tracking block
            cv2.putText(frame, "Tracking", (p1[0],p1[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,0,0),2)

            gp1 = (int(gtbbox[0]), int(gtbbox[1]))
            gp2 = (int(gtbbox[0] + gtbbox[2]), int(gtbbox[1] + gtbbox[3]))
            cv2.rectangle(frame, gp1, gp2, (255,255,0), 2, 1) # Draw a gt block
            cv2.putText(frame, "Ground Truth", (gp1[0],gp1[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,0),2)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
    
        
        cv2.putText(frame, f"bbox: ({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]})", (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
 
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        # k = cv2.waitKey(0)
        k = cv2.waitKey(1) & 0xff

        if k==ord('q'):
            break
        