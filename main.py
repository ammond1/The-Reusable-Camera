import cv2
import numpy as np

#import image
frame = cv2.imread('/Users/admin/Desktop/The Reusable Camera/DSCF5364.jpg')
cv2.imshow('Original Image', frame)

#import lut
def load_cube_lut(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Skip lines until we find the start of the LUT
    lut_data = []
    for line in lines:
        if line.startswith("LUT_3D_SIZE"):
            size = int(line.split()[-1])
            lut_data = np.zeros((size, size, size, 3), dtype=np.float32)
            break

    # Read LUT values
    lut_index = 0
    for line in lines:
        if line.startswith("#") or line.strip() == "":
            continue
        if line.startswith("LUT_3D_SIZE"):
            continue

        values = list(map(float, line.split()))
        x = lut_index // (size * size)
        y = (lut_index % (size * size)) // size
        z = lut_index % size

        lut_data[x, y, z] = values
        lut_index += 1

    return lut_data, size

# Load the LUT
lut, lut_size = load_cube_lut('/Users/admin/Desktop/The Reusable Camera/XT3_FLog_FGamut_to_ETERNA_BT.709_33grid_V.1.01.cube')

#apply lut 
def apply_3d_lut(image, lut, lut_size):
    # Normalize the image pixel values to the range of LUT indices
    normalized_image = (image / 255.0) * (lut_size - 1)
    normalized_image = normalized_image.astype(np.int32)

    # Apply the LUT using vectorized operations
    result_image = lut[
        normalized_image[..., 0],
        normalized_image[..., 1],
        normalized_image[..., 2]
    ]

    # Scale back to 0-255 range
    result_image = (result_image * 255).astype(np.uint8)

    return result_image

frame_after = apply_3d_lut(frame, lut, lut_size)
cv2.imshow('After Image', frame_after)

#closes windows
cv2.waitKey(0)
cv2.destroyAllWindows()