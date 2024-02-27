import cv2
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import numpy as np


def perspective_transform(img, verbose=False):
    """
    Get bird's eye view from input image
    """
    # 1. Visually determine 4 source points and 4 destination points
    # 2. Get M, the transform matrix, and Minv, the inverse using cv2.getPerspectiveTransform()
    # 3. Generate warped image in bird view using cv2.warpPerspective()

    ## TODO

    # For gazebo images
    pts1 = np.float32([[70, 360], [153, 320], [587, 360], [500, 320]])
    pts2 = np.float32([[0, 450], [0, 390], [610, 450], [610, 390]])

    # # For rosbag images in 375 x 1242 resolution
    # pts1 = np.float32([[400, 320], [470, 280], [780, 320], [742, 280]])
    # pts2 = np.float32([[150, 330], [150, 260], [1092, 330], [1092, 260]])

    M = cv2.getPerspectiveTransform(pts1, pts2)
    Minv = cv2.getPerspectiveTransform(pts2, pts1)

    warped_img = cv2.warpPerspective(
        img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR
    )

    ####

    return warped_img, M, Minv


test_img_save_path = "out/mp1/test_gazebo.png"
warped_img_save_path = "out/mp1/warped_gazebo.png"

img = cv2.imread("out/mp1/test.png")

ax: Axes
fig, ax = plt.subplots()
ax.imshow(img)
ax.grid(True)
ax.set_xticks([20 * i for i in range(63)])
ax.set_yticks([20 * i for i in range(20)])
ax.tick_params(axis="x", rotation=90)
plt.savefig(test_img_save_path, dpi=600)


warped_img, M, Minv = perspective_transform(img)
cv2.imwrite(warped_img_save_path, warped_img)
