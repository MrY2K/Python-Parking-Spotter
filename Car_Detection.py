import cv2                      # OpenCV for computer vision operations
import numpy as np              # Numerical operations and array handling
from ultralytics import YOLO    # YOLOv8 implementation for object detection

# Load YOLOv8 pre-trained model
model = YOLO('yolov8n.pt')

# Parking spot parameters
OCCUPANCY_THRESHOLD = 30            # Frames a car needs to stay to be considered parked
EMPTY_SPOT_COLOR = (0, 255, 0)      # Green
OCCUPIED_SPOT_COLOR = (0, 0, 255)   # Red

class ParkingMonitor:
    def __init__(self, video_path, spots_file):
        self.cap = cv2.VideoCapture(video_path)
        self.spots = self.load_spots(spots_file)
        self.spot_status = {i: {'occupied': False, 'counter': 0} for i in range(len(self.spots))}
        self.car_positions = {}
        self.frame_count = 0
        
        # Video dimensions
        self.desired_width = 800
        ret, frame = self.cap.read()
        if not ret:
            raise ValueError("Could not read video file")
        
        self.original_height, self.original_width = frame.shape[:2]
        self.aspect_ratio = self.original_height / self.original_width
        self.new_height = int(self.desired_width * self.aspect_ratio)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    @staticmethod
    def load_spots(filename):
        spots = []
        with open(filename, 'r') as f:
            for line in f.readlines():
                coords = list(map(int, line.strip().split(',')))
                spots.append(np.array([(coords[i], coords[i+1]) for i in range(0, 8, 2)]))
        return spots

    def is_point_in_polygon(self, point, polygon):
        return cv2.pointPolygonTest(polygon, point, False) >= 0

    def process_frame(self, frame):
        # Resize frame
        resized = cv2.resize(frame, (self.desired_width, self.new_height))
        
        # Detect vehicles
        results = model.predict(resized, conf=0.5, classes=[2, 3, 5, 7])  # Cars, trucks, buses, etc.
        
        current_cars = {}
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            center = ((x1 + x2) // 2, (y1 + y2) // 2)
            current_cars[center] = (x1, y1, x2, y2)

            # Draw bounding box
            cv2.rectangle(resized, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.circle(resized, center, 5, (255, 0, 0), -1)

        # Update car positions and spot status
        for spot_id, polygon in enumerate(self.spots):
            spot_occupied = False
            for center, bbox in current_cars.items():
                if self.is_point_in_polygon(center, polygon):
                    spot_occupied = True
                    break

            if spot_occupied:
                self.spot_status[spot_id]['counter'] = min(self.spot_status[spot_id]['counter'] + 1, OCCUPANCY_THRESHOLD)
            else:
                self.spot_status[spot_id]['counter'] = max(self.spot_status[spot_id]['counter'] - 1, 0)

            # Update occupancy status
            self.spot_status[spot_id]['occupied'] = self.spot_status[spot_id]['counter'] >= OCCUPANCY_THRESHOLD

        # Draw parking spots
        for spot_id, polygon in enumerate(self.spots):
            color = OCCUPIED_SPOT_COLOR if self.spot_status[spot_id]['occupied'] else EMPTY_SPOT_COLOR
            cv2.polylines(resized, [polygon], True, color, 2)
            cv2.putText(resized, str(spot_id), tuple(polygon[0]), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

        # Display statistics
        occupied = sum(1 for s in self.spot_status.values() if s['occupied'])
        cv2.putText(resized, f"Occupied: {occupied}/{len(self.spots)}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        return resized

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            processed_frame = self.process_frame(frame)
            cv2.imshow('Parking Monitor', processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

# Usage
if __name__ == "__main__":
    monitor = ParkingMonitor('carPark.mp4', 'parking_spots.txt')
    monitor.run()