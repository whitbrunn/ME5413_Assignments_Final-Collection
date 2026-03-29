## ME5413 Homework 1: Perception  
-- by Mai Jingyang, GitHub @Whitbrunn, please contact maij@u.nus.edu for any questions.

### 1. Installation

Please refer to `requirements.txt`.

### 2. What we have

2.1 In folder `task1_tracking/`,

- Files,
    - `task1.ipynb`: The main code notebook with comprehensive interpretations, which is divided into Section 1.0-1.5.
    - `TP_demo.py`: A script that achieves SOT using TM, mainly based on opencv library.
    - `Detr_demo.py`: A fully-functional script that achieves SOT using ODA, where the detection part is based on a pretained model Detr(https://huggingface.co/docs/transformers/en/model_doc/detr), and the association part is based on DeepSort(https://github.com/Sharpiless/Yolov5-deepsort-inference).
    - `Improved_demo.py`: A fully-functional script that achieves SOT using Yolov5-DeepSort with pretained weight `yolov5m.pt` (v4.0), adapted from https://github.com/Sharpiless/Yolov5-deepsort-inference.
    - `AIDetector_pytorch.py`, `YoloDetector_pytorch`, `tracker.py`: The dependency files for ODA method and Yolov5-DeepSort method.

- Folder,
    - `detr-resnet-50/`: you should download the model weight from [here](https://huggingface.co/facebook/detr-resnet-50).
    - `results/`: A folder that contains 3 folders w.r.t 3 methods, each of them contains all tracking results of seq 1-5. Each line in each result *.txt file represents the tracking bounding box w.r.t each frame, in (top_left_x, top_left_y, width, height) format.
    - `utils/`, `models/`, `deep_sort/`, `Improved/`: The dependency folders for ODA method and Yolov5-DeepSort method.


2.2 In folder `task2_prediction/`,

- Files,
    - `task2.ipynb`: The only code notebook with comprehensive interpretations, which is divided into Section 2.1-2.5. All functions are achieved in this file.

- Folder,  
    - `visualization/`: A folder that contains 2 folder, `CVM/` and `CAM/`, containing prediction *.png results w.r.t constant velocity model and constant acceleration model respectively.

2.3 In folder `task3_bonus/`,

- Folder,
    - `code/`: only one folder inside `sot_demo/`, which is a ROS1 package.
    - `rosbags/`: I think it the given data.


### 3. How to use

3.1 Task1,

- Make sure you have all the files and folders mentioned above in 2.1.
- Extract data in `data/` folder.
- Easily run and read the `task1.ipynb` block by block. 
- Pay attention that it's recommended to run `Detr_demo.py` other than Section 1.2, and the improved method is implemented by `Improved_demo.py`! 
- These above notes and more details are carefully written in `task1.ipynb`.
- All tracking *.txt results will be stored in `task1_tracking/results/`.

3.2 Task2,

- Make sure you have all the files and folders mentioned above in 2.2.
- Extract data in `task2_data/` folder.
- Easily run and read the `task2.ipynb` block by block.
- All prediction *.png results will be stored in `task2_prediction/visualization/`.

3.3 Task3,

- You should put folder `sot_demo/` into your `ROS_WORKSPACE/src/`, and then `catkin_make` your workspace.

### 4. One More Thing

Good assignment guide and challenge & realistic experimental data.