# JENGABELLS

**Group Members:**
Katie Hughes, Alyssa Chen, Hang Yin, Liz Metzger

This package is meant to turn a Franka Emika Panda arm into a Jenga assistant! It uses computer vision to detect Jenga bricks and place them on top of the tower. The robot plans and executes trajectories using a custom MoveGroup API.

Upon starting the package for the first time the robot needs to be calibrated. This process adds a tf to the tf tree between the panda hand and the camera by using known transforms between the camera and an april tag and the end effector and the base of the robot.

Once calibrated it uses a depth map and computer vision to find the top of the tower, the orientation of the top of the tower, and the table. Once these are determined then the program inters a mode where it scans between the top of the tower and the table to find any pushed out blocks. After finding a block, the centroid is added to the tf tree so that the robot can move to the location of the block. Once the robot has moved to the block it will grab the block, pull it out of the tower, move to the top of the tower, and place the block in the appropriate orientation. Once the block is placed the program goes back into scanning mode and looks for another block.

## Changes

This branch of code has a few changes from our original implementation. First, the hand detection model does not perform well when not in our original setup. To get around this, there is a parameter added in the camera node that determines whether to use the model (defaulting to false). If the model is used, it will continuously detect if a person is in frame, and when it detects 80 empty frames in a row it will begin scanning for a block. If the model is not used, you can call the `/scan` service to manually trigger scanning. You can also trigger scanning via an Amazon Alexa! First, say "Hey Alexa, open Robot Jenga Assistant". After that, say "Pull Block". The robot then will automatically transition to the scanning state.

To assist with tuning various offsets when pulling blocks, we also added an `offsets.yaml` config file to the `plan_execute` package. This allows for easy adjustments outside of the node.

## Instructions

* Clone the repository, and from your root workspace, run `vcs import --recursive --input src/hw3group-jengabells/camera/config/jenga_vision.repo src/` to install the necessary april tag packages.
* Plug into the Franka and the realsense camera.
* `ssh student@station`, then `ros2 launch franka_moveit_config moveit.launch.py use_rviz:=false robot_ip:=panda0.robot`. All other commands are run from your own computer.
If you need to calibrate:
   * Run `ros2 launch plan_execute jenga_full.launch.py calibrate:=true`
   * Run `ros2 service call /calibrate std_srvs/srv/Empty` to move the robot into the calibration position. Insert the april tag into the grippers (keep your hand over it until it is in the right place).
   * Run `ros2 launch camera jenga_vision.launch.py calibrate:=true`. Wait until you see a message that indicates that the calibration is complete, then remove the tag. The file `tf.yaml` will be saved in `${root_workspace}/install/camera/share/camera` and will be loaded automatically in future runs. If you want to permanently save it (for example, if the camera will not be moved after this), copy the contents into the `tf.yaml` in your `src` directory.
   * Run `ros2 service call /ready std_srvs/srv/Empty` to return the robot to the ready position. Then you can CTRL-C the program.
Otherwise:
* Run `ros2 launch plan_execute jenga_full.launch.py`
* In the pop up window, ensure that the tower is visible in the color frame and make sure that it is inside the bounding square (if not, adjust the size with the trackbars)
* Remove a piece about halfway from the tower (and ensure you can see it from the camera window). When you step away from the table, the robot will grab and place it!