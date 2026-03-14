import rclpy
from rclpy.node import Node
import serial
from geometry_msgs.msg import PoseStamped, Twist
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
import time


class SerialGoalSender(Node):
    def __init__(self):
        super().__init__('serial_goal_sender')

        # ----------------------------
        # SERIAL CONNECTION TO ARDUINO
        # ----------------------------
        try:
            self.ser = serial.Serial('/dev/ttyACM1', 115200, timeout=0.1)
            self.get_logger().info("Connected to Arduino on /dev/ttyACM1")
        except Exception as e:
            self.get_logger().error(f"Failed to open serial: {e}")
            self.ser = None

        # ----------------------------
        # NAV2 CLIENT + CMD_VEL PUBLISHER
        # ----------------------------
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.current_goal = None       # Save last goal for resume
        self.nav_goal_handle = None

        # Timer for serial polling
        self.create_timer(0.1, self.check_serial)

        # ----------------------------
        # LOCATION MAP
        # ----------------------------
        self.goal_map = {
            7: (4.33, -5.58, 0.0),
            6: (-0.10, -0.06, 0.0),
            11: (0.0, 0.0, 0.0),
            5: (0.82, -5.16, 0.0),
            12: (0.0, 0.0, 0.0),
        }


    # ---------------------------------------------------------
    # SEND NAV2 GOAL
    # ---------------------------------------------------------
    def send_goal(self, x, y, yaw):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.orientation.w = 1.0

        self.current_goal = (x, y, yaw)  # Save for resume

        self.nav_client.wait_for_server()

        send_goal_future = self.nav_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.goal_response_callback)

        self.get_logger().info(f"Goal sent → ({x}, {y}, {yaw})")


    def goal_response_callback(self, future):
        self.nav_goal_handle = future.result()
        if not self.nav_goal_handle.accepted:
            self.get_logger().warn("Goal was rejected by Nav2")
            return
        self.get_logger().info("Goal accepted by Nav2")


    # ---------------------------------------------------------
    # STOP ROBOT (cancel nav + force zero velocity)
    # ---------------------------------------------------------
    def stop_robot(self):
        self.get_logger().warn("STOP command received!")

        # Cancel Nav2 goal
        if self.nav_goal_handle:
            cancel_future = self.nav_goal_handle.cancel_goal_async()
            self.get_logger().info("Nav2 goal cancelled")

        # Publish zero velocity several times to override Nav2
        for _ in range(10):
            twist = Twist()
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.vel_pub.publish(twist)
            time.sleep(0.05)

        self.get_logger().info("Robot fully STOPPED.")


    # ---------------------------------------------------------
    # RESUME LAST GOAL
    # ---------------------------------------------------------
    def resume_last_goal(self):
        if self.current_goal is None:
            self.get_logger().warn("No previous goal to resume!")
            return

        x, y, yaw = self.current_goal
        self.get_logger().info("Resuming last goal...")
        self.send_goal(x, y, yaw)


    # ---------------------------------------------------------
    # SERIAL CHECK LOOP
    # ---------------------------------------------------------
    def check_serial(self):
        if self.ser is None:
            return
        
        if self.ser.in_waiting:
            line = self.ser.readline().decode(errors="ignore").strip()
            num = ''.join([c for c in line if c.isdigit()])

            if num == '':
                return

            value = int(num)
            self.get_logger().info(f"Received: {value}")

            # STOP command
            if value == 60000:
                self.stop_robot()
                return

            # RESUME command (you can change this)
            if value == 120000:
                self.resume_last_goal()
                return

            # NAVIGATION commands
            if value in self.goal_map:
                x, y, yaw = self.goal_map[value]
                self.send_goal(x, y, yaw)
            else:
                self.get_logger().info(f"Ignored unknown command: {value}")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main(args=None):
    rclpy.init(args=args)
    node = SerialGoalSender()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

