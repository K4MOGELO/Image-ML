import cv2

image = cv2.imread('uploads/road1.jpg')
rbg_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

image_sp = image.shape

for i in range(image_sp[0]):
    for j in range(image_sp[1]):
        for k in range(image_sp[2]):
            if k > 0 and image[i][j][k]-image[i][j][k-1] < 10 or image[i][j][k]-image[i][j][k-1] < -10:
                image[i][j] = [255, 255, 255]
print(image)

cv2.imshow('new image', image)
cv2.waitKey(0)
cv2.destroyAllWindows

