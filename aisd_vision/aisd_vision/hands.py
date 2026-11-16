import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands
from aisd_msgs.msg import Hand

class Hands(Node):
    def __init__(self):
        super().__init__('hands')
        # Subscribe to video_frames topic to receive images
        self.subscription = self.create_subscription(
            Image, 'video_frames', self.listener_callback, 10)
        # Initialize converter between ROS and OpenCV images
        self.br = CvBridge()
        # Publisher of Hand messages to the cmd_hand topic
        self.hand_publisher = self.create_publisher(Hand, 'cmd_hand', 10)
        # Constants for MediaPipe hand landmarks
        self.PINKY_FINGER_TIP = 20
        self.INDEX_FINGER_TIP = 8

    def listener_callback(self, msg):
        # Convert the ROS Image message to an OpenCV image
        image = self.br.imgmsg_to_cv2(msg)

        # Analyse the image for hands using MediaPipe
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as myhands:

            # To improve performance, optionally mark the image as not writeable
            image.flags.writeable = False
            # Convert image from BGR to RGB for MediaPipe
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Process the image to find hands
            results = myhands.process(image)

            if results.multi_hand_landmarks:
                # Create a new Hand message
                msg = Hand()
                # Extract x coordinate of pinky tip
                msg.xpinky = results.multi_hand_landmarks[0].landmark[self.PINKY_FINGER_TIP].x
                # Extract x coordinate of index finger tip
                msg.xindex = results.multi_hand_landmarks[0].landmark[self.INDEX_FINGER_TIP].x

                # Publish only if there is a subscriber
                if self.hand_publisher.get_subscription_count() > 0:
                    self.hand_publisher.publish(msg)
                else:
                    self.get_logger().info('waiting for subscriber')

def main(args=None):
    rclpy.init(args=args)
    hands = Hands()
    rclpy.spin(hands)
    hands.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
