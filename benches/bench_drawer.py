import cv2
import json
import os

# Change this to your actual path
IMG_SRC = r"C:\Users\hp\Desktop\class-engagement-project\data\images.jpg"

OUTPUT_JSON = r"C:\Users\hp\Desktop\class-engagement-project\benches\roi_config.json"

# Create benches folder if not exists
os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

# Variables
drawing = False
current_polygon = []
polygons = {}

def mouse_callback(event, x, y, flags, param):
    global drawing, current_polygon
    if event == cv2.EVENT_LBUTTONDOWN:  # Left click = add point
        current_polygon.append((x, y))
    elif event == cv2.EVENT_RBUTTONDOWN:  # Right click = undo last point
        if current_polygon:
            current_polygon.pop()

def main():
    global current_polygon
    img = cv2.imread(IMG_SRC)
    clone = img.copy()

    cv2.namedWindow("Bench Drawer")
    cv2.setMouseCallback("Bench Drawer", mouse_callback)

    bench_id = 1
    while True:
        temp = clone.copy()

        # Draw current polygon
        if current_polygon:
            for i in range(len(current_polygon)):
                cv2.circle(temp, current_polygon[i], 3, (0, 0, 255), -1)
                if i > 0:
                    cv2.line(temp, current_polygon[i-1], current_polygon[i], (0, 255, 0), 2)

        # Draw all saved polygons
        for key, pts in polygons.items():
            for i in range(len(pts)):
                cv2.circle(temp, pts[i], 3, (255, 0, 0), -1)
                if i > 0:
                    cv2.line(temp, pts[i-1], pts[i], (255, 0, 0), 2)

        cv2.imshow("Bench Drawer", temp)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("n"):  # finish current polygon
            if len(current_polygon) > 2:
                polygons[f"bench_{bench_id}"] = current_polygon[:]
                bench_id += 1
                current_polygon = []
        elif key == ord("s"):  # save polygons
            with open(OUTPUT_JSON, "w") as f:
                json.dump(polygons, f)
            print("Saved:", OUTPUT_JSON)
        elif key == ord("q"):  # quit
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
