import rclpy
from rclpy.node import Node
from aisd_msgs.msg import Hand
from geometry_msgs.msg import Twist

class Move(Node):
    def __init__(self):
        super().__init__('move')
        # Subscribe to Hand messages from the hands node
        self.subscription = self.create_subscription(
            Hand, 'cmd_hand', self.listener_callback, 10)
        # Publisher for velocity commands to the robot
        self.vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

    def listener_callback(self, msg):
        angle = 0.0
        linear = 0.0
        
        # Determine turning direction based on index finger x position
        # If index finger is on the right side of the screen (x > 0.55)
        if msg.xindex > 0.55:
            self.get_logger().info('right')
            angle = -0.1
        # If index finger is on the left side of the screen (x < 0.45)
        elif msg.xindex < 0.45:
            self.get_logger().info('left')
            angle = 0.1
        else:
            angle = 0.0
            
        # Determine forward movement based on relative position of index and pinky
        # If index finger is to the right of the pinky (open hand), move forward
        if msg.xindex > msg.xpinky:
            self.get_logger().info('come')
            linear = 0.5
        else:
            self.get_logger().info('stay')
            linear = 0.0
            
        # Create and populate a Twist message
        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angle
        
        # Publish only if there is a subscriber (like turtlesim or Create3)
        if self.vel_publisher.get_subscription_count() > 0:
            self.vel_publisher.publish(twist)
        else:
            self.get_logger().info('waiting for subscriber')

def main(args=None):
    rclpy.init(args=args)
    move = Move()
    rclpy.spin(move)
    move.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
