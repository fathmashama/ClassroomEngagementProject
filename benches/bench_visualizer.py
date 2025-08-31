import cv2
import json

IMG_SRC = r"C:\Users\hp\Desktop\class-engagement-project\data\images.jpg"
ROI_JSON = r"C:\Users\hp\Desktop\class-engagement-project\benches\roi_config.json"

img = cv2.imread(IMG_SRC)

with open(ROI_JSON, "r") as f:
    polygons = json.load(f)

# Draw polygons
for key, pts in polygons.items():
    pts = [(int(x), int(y)) for (x, y) in pts]
    for i in range(len(pts)):
        cv2.line(img, pts[i], pts[(i+1) % len(pts)], (0, 255, 0), 2)
    cv2.putText(img, key, pts[0], cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

cv2.imshow("Bench Visualization", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
