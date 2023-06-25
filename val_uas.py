import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import tf
from visualization_msgs.msg import Marker

def publisher_node():
    rospy.init_node('minimal_publisher', anonymous=True)
    pub = rospy.Publisher('codeuas', String, queue_size=10)
    rate = rospy.Rate(10) 

    while not rospy.is_shutdown():
        message = "Valrama Wardhana Hariwidjaja was here"
        rospy.loginfo(message)
        pub.publish(message)
        rate.sleep()

def callback(data):
    rospy.loginfo("Received message: %s", data.data)

def subscriber_node():
    rospy.init_node('minimal_subscriber', anonymous=True)
    rospy.Subscriber('codeuas', String, callback)

def robot_simulator():
    rospy.init_node('robot_simulator', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  

    while not rospy.is_shutdown():
        # Generate control commands for the simulated robot
        cmd_vel = Twist()
        cmd_vel.linear.x = 0.2
        cmd_vel.angular.z = 0.1
        pub.publish(cmd_vel)
        rate.sleep()

def transform_listener():
    rospy.init_node('transform_listener')
    listener = tf.TransformListener()

    rate = rospy.Rate(10)  

    while not rospy.is_shutdown():
        try:
            listener.waitForTransform('/frame1', '/frame2', rospy.Time(0), rospy.Duration(1.0))
            (trans, rot) = listener.lookupTransform('/frame1', '/frame2', rospy.Time(0))
            rospy.loginfo("Translation: x=%.2f, y=%.2f, z=%.2f", trans[0], trans[1], trans[2])
            rospy.loginfo("Rotation: x=%.2f, y=%.2f, z=%.2f, w=%.2f", rot[0], rot[1], rot[2], rot[3])

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            pass

        rate.sleep()

def marker_publisher():
    rospy.init_node('marker_publisher', anonymous=True)
    pub = rospy.Publisher('codeuas_marker', Marker, queue_size=10)
    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        marker = Marker()
        # Set marker properties
        marker.header.frame_id = "map"  # Frame ID tempat marker ditampilkan
        marker.type = Marker.SPHERE  # Jenis marker (dalam contoh ini: bola)
        marker.action = Marker.ADD  # Aksi yang diambil (dalam contoh ini: menambahkan marker)
        marker.pose.position.x = 1.0  # Posisi X marker dalam koordinat dunia
        marker.pose.position.y = 2.0  # Posisi Y marker dalam koordinat dunia
        marker.pose.position.z = 0.5  # Posisi Z marker dalam koordinat dunia
        marker.pose.orientation.x = 0.0  # Orientasi X marker
        marker.pose.orientation.y = 0.0  # Orientasi Y marker
        marker.pose.orientation.z = 0.0  # Orientasi Z marker
        marker.pose.orientation.w = 1.0  # Orientasi W marker
        marker.scale.x = 0.2  # Skala X marker
        marker.scale.y = 0.2  # Skala Y marker
        marker.scale.z = 0.2  # Skala Z marker
        marker.color.a = 1.0  # Alpha (transparansi) marker (0.0 - 1.0)
        marker.color.r = 1.0  # Komponen merah warna marker (0.0 - 1.0)
        marker.color.g = 0.0  # Komponen hijau warna marker (0.0 - 1.0)
        marker.color.b = 0.0  # Komponen biru warna marker (0.0 - 1.0)

        pub.publish(marker)
        rate.sleep()

def process_lidar_data():
    rospy.init_node('lidar_processor')
    rospy.Subscriber('/scan', LaserScan, lidar_callback)

def lidar_callback(data):
    ranges = data.ranges  # Mendapatkan data jarak dari sensor LIDAR
    min_range = min(ranges)  # Mencari jarak terdekat
    rospy.loginfo("Minimum range: %.2f meters", min_range)

if __name__ == '__main__':
    try:
        publisher_node()
        subscriber_node()
        robot_simulator()
        transform_listener()
        marker_publisher()
        process_lidar_data()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
