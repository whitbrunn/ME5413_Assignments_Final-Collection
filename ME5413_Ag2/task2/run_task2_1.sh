#!/bin/bash

# Three variables:
# launch file name
# score{?}.txt(2 times)
# lua name

read -p "Input bag index (eg. 1): " BAG_NAME

BAG_PATH="/home/jy/Cources/ME5413_AG/ME5413_Ag2/task2/data/resbag/res${BAG_NAME}.bag"
MAP_PATH="/home/jy/Cources/ME5413_AG/ME5413_Ag2/task2/data/resmap/res${BAG_NAME}"

mkdir -p "$(dirname "$BAG_PATH")"
mkdir -p "$MAP_PATH"

# gnome-terminal --tab -- bash -c "roscore; exec bash"
# sleep 5  # Wait for roscore to initialize
rosparam set use_sim_time true  # Set simulated time


echo "Rosbag recording...${BAG_PATH}"
# Create a new tmux session to record rosbag

BAG_SE_NAME="rosbag_session${BAG_NAME}"

tmux new-session -d -s $BAG_SE_NAME "
  cd ~; 
  source ~/ctgrapher_ws/devel_isolated/setup.bash;
  rosbag record -O $BAG_PATH /tf /tf_static /ground_truth /odom /scan /imu /clock
"

# Launch cartographer in a new terminal
gnome-terminal --tab -- bash -c "
  cd /home/jy/ctgrapher_ws;
  source ~/ctgrapher_ws/devel_isolated/setup.bash
  roslaunch cartographer_ros demo_jackal_bag1.launch bag_filename:=/home/jy/data/task2.bag;
  exec bash
"

echo "Waiting for rosbag play to finish..."


sleep 290  # Adjust this sleep time as needed
echo "rosbag play has finished. Stopping all processes..."

# Save the map using map_saver
gnome-terminal --tab -- bash -c "
  cd ~;
  rosrun map_server map_saver --occ 70 --free 30 -f ${MAP_PATH}/map map:=/map;
  exec bash
"
sleep 10

echo "Task completed. Map saved at ${MAP_PATH}/map.pgm and ${MAP_PATH}/map.yaml"

# Gracefully shut down rviz
echo "Gracefully shutting down rviz..."
if pgrep -f rviz > /dev/null; then
  pkill -SIGINT -f rviz  # Send SIGINT to rviz for graceful shutdown
  sleep 5  # Wait for rviz to close properly
  if pgrep -f rviz > /dev/null; then
    echo "rviz did not shut down gracefully, forcing termination..."
    pkill -SIGTERM -f rviz  # Force terminate if still running
  else
    echo "rviz has been gracefully terminated."
  fi
else
  echo "No rviz process found, skipping termination."
fi

# Gracefully terminate rosbag recording in tmux session
echo "Stopping rosbag recording..."
tmux send-keys -t $BAG_SE_NAME C-c
sleep 5 
tmux kill-session -t $BAG_SE_NAME
echo "rosbag recording stopped."

# Add this check and rename
if [ -f "${BAG_PATH}.active" ]; then
  mv "${BAG_PATH}.active" "${BAG_PATH}"
  echo "Renamed active bag file to ${BAG_PATH}"
fi


echo "All processes have been gracefully terminated."

EVO_PLOT_PATH="${MAP_PATH}/ape_plot.png"
LUA_PATH="${MAP_PATH}/demo_jackal_bag.lua"
SCORE_TXT_PATH="/home/jy/Cources/ME5413_AG/ME5413_Ag2/task2/data/resscore/res${BAG_NAME}_score.txt"

echo "Computing Absolute Pose Error (APE) and saving plot to ${EVO_PLOT_PATH}..."
# evo_ape bag $BAG_PATH /ground_truth /tf:map.base_link --plot --save_plot ${EVO_PLOT_PATH}

cp /home/jy/ctgrapher_ws/src/cartographer_ros/cartographer_ros/configuration_files/demo_jackal_bag1.lua $LUA_PATH
evo_ape bag $BAG_PATH /ground_truth /tf:map.base_link --align --plot --save_plot ${EVO_PLOT_PATH} > score1.txt
cp -f score1.txt $SCORE_TXT_PATH

echo "APE computation completed. Plot saved at ${EVO_PLOT_PATH}."


