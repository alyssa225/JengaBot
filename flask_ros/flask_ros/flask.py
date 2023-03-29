from flask import Flask, redirect, url_for, request, render_template, jsonify
import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class FlaskNode(Node):
    def __init__(self):
        super().__init__('my_node')
        self.app = Flask(__name__)

        self.steps_ready = False

        # define Flask routes here
        @self.app.route('/')
        def homepage():
            return "Welcome, this is my super empty home page for my winter project!"

        @self.app.route('/alexa', methods=['POST'])
        def handle_request():
            json_data = request.get_json()
            # Send a response
            response = {'message': 'Pulling Jenga block!'}

            my_msg = String()
            my_msg.data = "something"
            self.instruction_publisher_.publish(my_msg)
            
            return jsonify(response)

        # start Flask app on a separate thread
        self.app_thread = threading.Thread(target=self.app.run)
        self.app_thread.start()

        # initialize a publisher to /gpt_instruction topic with String message type
        self.instruction_publisher_ = self.create_publisher(String, '/pull_block', 10)

    def __del__(self):
        # stop Flask app when node is destroyed
        self.app_thread.join()

def main(args=None):
    """Start and spin the node."""
    rclpy.init(args=args)
    node = FlaskNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()