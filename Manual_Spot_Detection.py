import cv2

# Load the first frame from the video
cap = cv2.VideoCapture('carPark.mp4')
ret, frame = cap.read()
cap.release()

if not ret:
    print("Error: Could not read video file")
    exit()

# Resize parameters
desired_width = 800
original_height, original_width = frame.shape[:2]
aspect_ratio = original_height / original_width
new_height = int(desired_width * aspect_ratio)
resized_frame = cv2.resize(frame, (desired_width, new_height), interpolation=cv2.INTER_AREA)

# Parking spot storage
all_spots = []
current_spot = []

# Mouse callback function
def mouse_callback(event, x, y, flags, param):
    global current_spot
    if event == cv2.EVENT_LBUTTONDOWN:
        current_spot.append((x, y))
        if len(current_spot) == 4:
            all_spots.append(current_spot.copy())
            current_spot.clear()

# Create window and set callback
cv2.namedWindow('Parking Lot Spot Picker')
cv2.setMouseCallback('Parking Lot Spot Picker', mouse_callback)

while True:
    display_frame = resized_frame.copy()
    
    # Draw existing spots
    for spot in all_spots:
        for i in range(4):
            cv2.line(display_frame, spot[i], spot[(i+1)%4], (0, 255, 0), 2)
    
    # Draw current working spot
    if len(current_spot) > 0:
        for i, pt in enumerate(current_spot):
            cv2.circle(display_frame, pt, 5, (0, 0, 255), -1)
            if i > 0:
                cv2.line(display_frame, current_spot[i-1], pt, (0, 255, 255), 2)
        if len(current_spot) == 4:
            cv2.line(display_frame, current_spot[-1], current_spot[0], (0, 255, 255), 2)
    
    # Show instructions
    cv2.putText(display_frame, 'Click 4 points per parking spot', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(display_frame, 'Press S: Save | D: Undo | C: Clear | Q: Quit', (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    cv2.imshow('Parking Lot Spot Picker', display_frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        # Save spots to file
        with open('parking_spots.txt', 'w') as f:
            for spot in all_spots:
                f.write(','.join(f"{x},{y}" for x, y in spot) + '\n')
        print(f"Saved {len(all_spots)} spots to parking_spots.txt")
    elif key == ord('d'):
        if current_spot:
            current_spot.pop()
    elif key == ord('c'):
        current_spot.clear()
    elif key == ord('q'):
        break

cv2.destroyAllWindows()