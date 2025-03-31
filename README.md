# 🎱 Snooker Ball Detection & Closest Ball Finder

## 📌 Overview

This Python script detects **red balls** on a snooker table image and identifies the one **closest to any pocket**.

It uses basic computer vision techniques with OpenCV and NumPy to process the image, find contours, filter relevant balls, and visualize the result with Matplotlib.

---

## 🧠 How It Works

1. **Image Preprocessing**
   - Loads the image (`snooker.png`) and converts it to **RGB** and **HSV** formats for better color filtering.

2. **Red Color Detection**
   - Applies HSV thresholds to detect two red ranges (`[0-10]` and `[170-180]` in hue).
   - Combines both masks to form the full red mask.

3. **Contour Detection**
   - Finds contours of detected regions.
   - Filters them based on minimum radius to remove noise.
   - Calculates average color inside each region to validate it's truly red.

4. **Ball Filtering**
   - Computes the average color of all red candidates.
   - Filters outliers by comparing their color to the average.

5. **Closest Ball Calculation**
   - Defines standard **6 pocket coordinates**.
   - Measures distance from each ball to all pockets.
   - Finds and highlights the closest red ball.

6. **Visualization**
   - Draws:
     - ⚪ White dots for all filtered red balls.
     - 🟢 Green dot for the ball closest to a pocket.


