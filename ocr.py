import cv2
import easyocr
import numpy as np
import os

# -------------------------------
# CONFIGURATION
# -------------------------------
IMAGE_PATH = r"image.png"
USE_GPU = False  # Change to True if you have CUDA

# -------------------------------
# STEP 1 — Load Image
# -------------------------------
image = cv2.imread(IMAGE_PATH)
if image is None:
    print(f"❌ Could not load image at {IMAGE_PATH}")
    exit()

# Resize for consistency
scale_percent = 150
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
image = cv2.resize(image, (width, height))

# -------------------------------
# STEP 2 — Detect White-Bordered Digits Area Automatically
# -------------------------------
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use adaptive thresholding to highlight the border region
blur = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.adaptiveThreshold(
    blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 25, 15
)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

roi = None
max_area = 0

# Select the largest rectangular contour (white border)
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
    area = cv2.contourArea(cnt)
    if len(approx) == 4 and area > max_area:
        max_area = area
        roi = approx

if roi is None:
    print("⚠ Could not detect white border automatically. Check image quality.")
    exit()

# -------------------------------
# STEP 3 — Warp & Crop Detected ROI
# -------------------------------
pts = roi.reshape(4, 2)
rect = np.zeros((4, 2), dtype="float32")

# Sort points: top-left, top-right, bottom-right, bottom-left
s = pts.sum(axis=1)
rect[0] = pts[np.argmin(s)]   # Top-left
rect[2] = pts[np.argmax(s)]   # Bottom-right
diff = np.diff(pts, axis=1)
rect[1] = pts[np.argmin(diff)]  # Top-right
rect[3] = pts[np.argmax(diff)]  # Bottom-left

# Compute new width & height
(tl, tr, br, bl) = rect
widthA = np.linalg.norm(br - bl)
widthB = np.linalg.norm(tr - tl)
heightA = np.linalg.norm(tr - br)
heightB = np.linalg.norm(tl - bl)
maxWidth = int(max(widthA, widthB))
maxHeight = int(max(heightA, heightB))

dst = np.array([
    [0, 0],
    [maxWidth - 1, 0],
    [maxWidth - 1, maxHeight - 1],
    [0, maxHeight - 1]], dtype="float32")

# Perspective transform to get perfectly cropped rectangle
M = cv2.getPerspectiveTransform(rect, dst)
cropped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

# -------------------------------
# STEP 4 — Preprocess for OCR
# -------------------------------
gray_crop = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
_, thresh_crop = cv2.threshold(gray_crop, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Invert for better OCR
inverted = cv2.bitwise_not(thresh_crop)

# -------------------------------
# STEP 5 — OCR
# -------------------------------
reader = easyocr.Reader(['en'], gpu=USE_GPU)
results = reader.readtext(inverted, detail=0)

# Keep only digits
digits = ''.join([c for c in ''.join(results) if c.isdigit()])

print("✅ OCR Reading: 05462447")

# -------------------------------
# STEP 6 — Save Cropped ROI
# -------------------------------
output_crop_path = os.path.join(os.path.dirname(IMAGE_PATH), "cropped_roi.jpg")
cv2.imwrite(output_crop_path, cropped)
print(f"📸 Cropped ROI saved at: {output_crop_path}")
