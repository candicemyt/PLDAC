import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import threshold_mean
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops, find_contours
from skimage.morphology import closing, square
from skimage.color import label2rgb, rgb2gray
from skimage.io import imread, imshow
from skimage.feature import canny, blob_log, corner_peaks, corner_harris, corner_subpix
from skimage.transform import resize, warp_coords, rotate
from math import pi


######## pre traitement de l'image #########

image = imread("images_tests/4tagszoom.png")
#image_g = rgb2gray(image)
#binarisation
thresh = threshold_mean(image)
binary = image > thresh
binary = binary[:,:,0]


############ detection avec regionprops ##############

label_image = label(binary)
print('nb regions detectees :', len(regionprops(label_image)))
qrcodes_potentiels = []
plt.figure()
num_detect = 1
for region in regionprops(np.squeeze(label_image)):
    a = region.area
    # aire -> (350 - 700 pour les fourmis avec le niveau de zoom actuel) (1000 - 2000 pour les exemples de beetag) (15000 - 25000 pour la planche)
    if a > 350 and a < 700:
        print(f"Detection {num_detect}")
        num_detect+=1
        #print('coords :', region.coords)
        print('aire :', a)
        print('orientation ', region.orientation)
        y1,x1,y2,x2 = region.bbox
        plt.plot(x1, y1, color='green', marker='+', markersize=5)
        plt.plot(x2, y2, color='green', marker='+', markersize=5)
        qrcodes_potentiels.append((region.image, region.coords, region.orientation))
imshow(image)

#traitement des regions detectees
num_detect = 1

for qr_code in qrcodes_potentiels:
    qr_code_image = qr_code[0]
    coord_qr_code = qr_code[1]
    orientation_qr_code = qr_code[2]
    mat_qr_code = []
    # affichage regions detectees
    #plt.figure()
    #plt.title(f"Detection {num_detect}")
    #imshow(qr_code_image)

    #re orientation des regions detectees
    plt.figure()
    plt.title(f"Detection {num_detect} pivotée")
    qr_code_image_rotate = rotate(qr_code_image, 360 - round(orientation_qr_code, 1)*180/pi)
    imshow(qr_code_image_rotate)

    test = np.array_split(qr_code_image_rotate, 7, axis=0)

    for line in test:
        line_qr_code = []
        for pixel in np.array_split(line, 6, axis=1):
            tmp = np.where(pixel == True, -1, 1)
            if np.sum(tmp) < 0:
                line_qr_code.append(0)
            else:
                line_qr_code.append(1)
        mat_qr_code.append(line_qr_code)
    print(f'matrice binaire detection {num_detect}: ' , mat_qr_code)
    num_detect += 1
plt.show()

