# Python Parking Spotter

This project is a computer vision-based application designed to monitor parking lot occupancy. It uses the YOLOv8 object detection model to identify vehicles and determines whether predefined parking spots are vacant or occupied from a video stream.



## How It Works

![](.assets/Vid_GIF.gif)

The system operates in two main stages:

1.  **Spot Definition (`Manual_Spot_Detection.py`):** The user first runs a utility script that displays the first frame of the input video. By clicking four points for each parking space, the user defines the polygonal area of each spot. These coordinates are saved to a text file (`parking_spots.txt`).

2.  **Detection and Monitoring (`Car_Detection.py`):** The main script reads the video feed and the saved parking spot coordinates. For each frame, it performs the following:
    *   Resizes the frame for consistent processing.
    *   Uses the pre-trained `yolov8n.pt` model to detect vehicles (cars, trucks, buses).
    *   For each detected vehicle, it calculates the center of its bounding box.
    *   It then checks if the center point of any vehicle falls within any of the predefined parking spot polygons.
    *   A counter system with a threshold (`OCCUPANCY_THRESHOLD`) is used to prevent flickering, ensuring a spot is marked 'occupied' only after a vehicle has been detected in it for a set number of frames.
    *   Finally, it visualizes the results on the video, drawing colored polygons over each spot and displaying an overall occupancy count.

## Prerequisites
You will need to have Python installed, along with the following libraries:
*   OpenCV (`opencv-python`)
*   NumPy (`numpy`)
*   Ultralytics (`ultralytics`)

You can install them using pip:
```bash
pip install opencv-python numpy ultralytics
```

## Usage
To run this project, you will need a video file of a parking lot. The scripts are configured to use a file named `carPark.mp4`.

### Step 1: Define Parking Spots
1.  Place your video file (e.g., `carPark.mp4`) in the root directory of the project.
2.  Run the manual spot detection script:
    ```bash
    python Manual_Spot_Detection.py
    ```
3.  A window will appear showing the first frame of your video.
4.  For each parking spot, click on the four corner points to define its boundary. After clicking the fourth point, the spot will be saved and you can begin defining the next one.
5.  Use the following keys for control:
    *   **`S`**: Save all defined spots to `parking_spots.txt`.
    *   **`D`**: Undo the last point clicked for the current spot.
    *   **`C`**: Clear all points for the current, in-progress spot.
    *   **`Q`**: Quit the application.

### Step 2: Run the Parking Monitor
Once you have saved your `parking_spots.txt` file, run the main detection script:
```bash
python Car_Detection.py
```
A new window will open playing the video, with parking spots overlaid in real-time. Empty spots will be outlined in green, and occupied spots will be outlined in red. An occupancy counter will be displayed in the top-left corner. Press `q` to exit the video stream.

## Files
*   **`carPark.mp4`**: The Video Stream of the parking lot.
*   **`Car_Detection.py`**: The main script that performs real-time vehicle detection and parking spot monitoring.
*   **`Manual_Spot_Detection.py`**: A helper script to interactively define the coordinates of parking spots.
*   **`yolov8n.pt`**: The pre-trained YOLOv8 nano model weights for object detection.
*   **`parking_spots.txt` (Generated)**: A text file created by `Manual_Spot_Detection.py` that stores the coordinates of the defined parking spots.