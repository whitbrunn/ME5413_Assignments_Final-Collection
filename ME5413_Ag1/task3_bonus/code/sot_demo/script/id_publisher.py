#!/usr/bin/env python3
#coding=utf-8

import rospy
from std_msgs.msg import String

def talker():
    rospy.init_node('id_publisher', anonymous=True)

    pub = rospy.Publisher('me5413/nusnetID', String , queue_size=10)

    #更新频率是1hz
    rate = rospy.Rate(1)
    
    rospy.loginfo(f"Initialing NUSID node...")

    while not rospy.is_shutdown():
        nusid = "E1373698"
        rospy.loginfo("NUSID: %s" % nusid)

        msg = String()
        msg.data =  nusid
        pub.publish(msg)

        rate.sleep()

if __name__ == '__main__':
    
    talker()