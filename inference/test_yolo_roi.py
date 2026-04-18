import cv2
from inference.yolo_detector import get_yolo_roi

# Load face-cropped image
img = cv2.imread("face_crop.jpg")

roi = get_yolo_roi(img)

if roi is None:
    print("YOLO found no ROI. Fallback will be used.")
    cv2.imshow("Fallback Face Crop", img)
else:
    print("YOLO ROI extracted")
    cv2.imshow("YOLO ROI", roi)

cv2.waitKey(0)
cv2.destroyAllWindows()
