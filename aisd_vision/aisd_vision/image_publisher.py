import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_publisher')
        # Create publisher for Image messages on the 'video_frames' topic
        self.publisher_ = self.create_publisher(Image, 'video_frames', 10)
        timer_period = 0.1  # Timer to run callback 10 times per second
        self.timer = self.create_timer(timer_period, self.timer_callback)
        # Open the default webcam (index 0)
        self.cap = cv2.VideoCapture(0)
        # Bridge to convert between ROS 2 and OpenCV images
        self.br = CvBridge()

    def timer_callback(self):
        # Read a frame from the webcam
        ret, frame = self.cap.read()
        if ret == True:
            # Convert OpenCV image to ROS 2 Image message and publish
            self.publisher_.publish(self.br.cv2_to_imgmsg(frame))

def main(args=None):
    rclpy.init(args=args)
    image_publisher = ImagePublisher()
    rclpy.spin(image_publisher)
    image_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
