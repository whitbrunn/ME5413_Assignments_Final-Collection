#!/usr/bin/env python3
#coding=utf-8

import rospy
from vision_msgs.msg import Detection2D
from sensor_msgs.msg import Image
import rospkg
import rosbag
import cv2
from std_msgs.msg import String
import numpy as np


def line2bbox(line):
    if line != "NaN":
        bbox = tuple([int(x) for x in line.split(",")]) # bbox: (x,y,width,height)
    else:
        bbox = line
    return bbox

rospack = rospkg.RosPack()
pkg_path = rospack.get_path("sot_demo")

seq_id = 3

pub = rospy.Publisher('me5413/nusnetID', String , queue_size=10)
pub1 = rospy.Publisher('me5413/track', Detection2D, queue_size=10)
pub2 = rospy.Publisher('me5413/groundtruth', Detection2D, queue_size=10)
pub3 = rospy.Publisher('me5413/viz_output', Image, queue_size=10)


with open(pkg_path+ f"/results/seq{seq_id}/trackresults_improved_seq{seq_id}.txt") as f:
    tbbox_lst = f.read().splitlines()
with open(pkg_path+ f"/results/seq{seq_id}/groundtruth.txt") as g_f:
    gtbbox_lst = g_f.read().splitlines()

bag_path = pkg_path+f"/rosbags/seq{seq_id}.bag"
bag = rosbag.Bag(bag_path)


def img_sub_sot_pub():
    global pub1
    global pub2
    global pub3
    rospy.init_node('sot_bbox_publisher', anonymous=True)
    #Subscriber函数第一个参数是topic的名称，第二个参数是接受的数据类型 第三个参数是回调函数的名称
    topic_name = '/me5413/image_raw'
    
    rate = rospy.Rate(3)

    img_lst = []
    for topic, msg, t in bag.read_messages(topics=['/me5413/image_raw']):
        # rospy.loginfo(len(msg))
        # rospy.loginfo(f"msg: {type(msg)}")
        # rospy.loginfo(f"msg  data: {type(msg.data)}")
        img_lst.append(msg.data)

    det_bbox = Detection2D()
    gt_bbox = Detection2D()
    id_msg = String()

    rate = rospy.Rate(1)

    i = 0
    for topic, msg, t in bag.read_messages(topics=['/me5413/image_raw']):
        if rospy.is_shutdown():
            break
        nusid = "E1373698"
        #rospy.loginfo("NUSID: %s" % nusid)
        
        id_msg.data =  nusid
        pub.publish(id_msg)

        imgb = msg.data
        # print(type(imgb))

        # with open("debug.jpg", "wb") as f:
        #     f.write(imgb)


        img_arr = np.frombuffer(imgb, dtype=np.uint8)
        frame = img_arr.reshape((msg.height,msg.width, -1))
        # print(frame.shape)
        frame = frame.copy()
        
        # print(type(img_arr))

        if tbbox_lst[i] != "NaN":
            x, y,width, height = line2bbox(tbbox_lst[i])
            
            det_bbox.id = i+1 # begin at 1
            det_bbox.x = x
            det_bbox.y = y
            det_bbox.width = width
            det_bbox.height = height
            
            pub1.publish(det_bbox)
            # rospy.loginfo(f"det_bbox: {det_bbox}")

            p1 = (int(x), int(y))
            p2 = (int(x + width), int(y + height))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1) # Draw a tracking block
            cv2.putText(frame, "Tracking", (p1[0],p1[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,0,0),2)
        else:
            pass
        
        gx, gy, gw, gh = line2bbox(gtbbox_lst[i])
        
        gt_bbox.id = i+1
        gt_bbox.x = gx
        gt_bbox.y = gy
        gt_bbox.width = gw
        gt_bbox.height = gh
        
        pub2.publish(gt_bbox)
        # rospy.loginfo(f"gt_bbox: {gt_bbox}")

        gp1 = (int(gx), int(gy))
        gp2 = (int(gx + gw), int(gy + gh))
        cv2.rectangle(frame, gp1, gp2, (255,255,0), 2, 1) # Draw a gt block
        cv2.putText(frame, "Ground Truth", (gp1[0],gp1[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,0),2)


        msg.data = frame.tobytes()
        pub3.publish(msg)


        rate.sleep()
        i+=1

if __name__ == '__main__':
    
    img_sub_sot_pub()