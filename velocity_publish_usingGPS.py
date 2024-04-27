from haversine import haversine
import os
import rospy
from sensor_msgs.msg import NavSatFix
from math import sqrt, pow
from haversine import haversine
from std_msgs.msg import Float64

class velocity_print:
    
    def __init__(self):
        rospy.init_node('velocity', anonymous=True)
        rospy.Subscriber('/gps/fix', NavSatFix, self.fix_callback)
        


        self.is_status = False
        self.pre_second = 0
        self.pre_lat = 0
        self.pre_lon = 0
        
        rate = rospy.Rate(0.5) #출력 주기 ex)5초주기면 1/5 =0.2, 10초주기면 1/10 =0.1 대입

        
        while not rospy.is_shutdown():
            if self.is_status:
                self.calculate()
                rate.sleep()
                
    def fix_callback(self, msg):
        self.is_status = True
        self.secs = msg.header.stamp.secs
        self.nsecs = msg.header.stamp.nsecs
        self.latitude = msg.latitude
        self.longitude = msg.longitude
        
        self.second = self.secs + self.nsecs*10**-9
        
    
    def velocity(self):
        
        self.now_second = self.second
        self.time_diff = self.now_second - self.pre_second
        self.pre_second =  self.now_second
        print("{}second".format(self.time_diff))
        
        return self.time_diff
        
    def distance(self):
        self.now_lat = self.latitude
        self.now_lon = self.longitude
        
        distance_meter = haversine((self.now_lat, self.now_lon),(self.pre_lat,self.pre_lon)) *1000

        self.pre_lat = self.now_lat
        self.pre_lon = self.now_lon

        print("{}m".format(distance_meter))
        
        return distance_meter
    
    def calculate(self):
        
        self.distance_meter = self.distance()
        self.time_diff = self.velocity()
        
        self.velocity_ms = self.distance_meter / self.time_diff
        self.velocity_ms = round(self.velocity_ms,1)
        print("{}m/s".format(self.velocity_ms))
        print("{}km/h\n".format(self.velocity_ms*3.6))

        velocity_pub = rospy.Publisher("/now_velocity", Float64, queue_size=10)
        velocity_pub.publish(self.velocity_ms)

        
        
if __name__ == '__main__':
    
    try:
        vel = velocity_print()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
        