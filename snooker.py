import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = './snooker.png'
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
red_lower = np.array([0, 120, 70])
red_upper = np.array([10, 255, 255])
mask1 = cv2.inRange(hsv_image, red_lower, red_upper)

red_lower2 = np.array([170, 120, 70])
red_upper2 = np.array([180, 255, 255])
mask2 = cv2.inRange(hsv_image, red_lower2, red_upper2)

red_mask = mask1 | mask2
contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

red_positions = []
filtered_positions = []
red_colors = []

for contour in contours:
    (x, y), radius = cv2.minEnclosingCircle(contour)
    if radius > 5:  
        red_positions.append((int(x), int(y)))
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.circle(mask, (int(x), int(y)), int(radius), 255, -1)
        mean_color = cv2.mean(image_rgb, mask=mask)[:3]
        red_colors.append(mean_color)

if red_colors:
    avg_red_color = np.mean(red_colors, axis=0)
    threshold = 50  
    for position, color in zip(red_positions, red_colors):
        if all(abs(c1 - c2) <= threshold for c1, c2 in zip(color, avg_red_color)):
            filtered_positions.append(position)

pockets = [
    (0, 0),
    (image.shape[1] // 2, 0),
    (image.shape[1] - 1, 0),
    (0, image.shape[0] - 1),
    (image.shape[1] // 2, image.shape[0] - 1),
    (image.shape[1] - 1, image.shape[0] - 1),
]
closest_ball = None
min_distance = float('inf')

for ball in filtered_positions:
    for pocket in pockets:
        distance = np.sqrt((ball[0] - pocket[0]) ** 2 + (ball[1] - pocket[1]) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_ball = ball


output_image = np.zeros_like(image, dtype=np.uint8)
for ball in filtered_positions:
    cv2.circle(output_image, ball, 2, (255, 255, 255), -1)

if closest_ball:
    cv2.circle(output_image, closest_ball, 5, (0, 255, 0), -1)

plt.figure(figsize=(10, 5))
plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
