import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import threshold_mean
from skimage.measure import label, regionprops
from skimage.io import imread, imshow
from skimage.transform import rotate
from math import pi
from analyse_qrcode.analyse_qr import analyse

def split(qr_code_image_rotate,col=6,lin=7):
    mat_qr_code=[]
    test = np.array_split(qr_code_image_rotate, lin, axis=0)
    for line in test:
        line_qr_code = []
        for pixel in np.array_split(line, col, axis=1):
            tmp = np.where(pixel == True, -1, 1)
            if np.sum(tmp) < -2:
                line_qr_code.append(0)
            else:
                line_qr_code.append(1)
        mat_qr_code.append(line_qr_code)
    return np.array(mat_qr_code)

######## pre traitement de l'image #########

image = imread("images_tests/4tagsfourmis.png")
#image=imread("images_tests/planche_test.png")
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
reel_qr_code=[]
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
    mat_qr_code=split(qr_code_image_rotate)
    if mat_qr_code[:, 0].sum() > 2 and mat_qr_code[:, 5].sum()> 2:
        if mat_qr_code[0].sum() > 2 and mat_qr_code[6].sum() > 2:
            mat_qr_code = split(qr_code_image_rotate, lin=9,col=8)
        else:
            mat_qr_code=split(qr_code_image_rotate,col=8)
        if mat_qr_code.shape[1]-6!=0:
            mat_qr_code = mat_qr_code[:, 1:-1]
            if mat_qr_code.shape[0]-7!=0:
                mat_qr_code = mat_qr_code[1:-1,:]
    mat_qr_code=mat_qr_code[1:-1,1:-1].tolist()
    print(f'matrice binaire detection {num_detect}: ', mat_qr_code)
    plt.figure()
    plt.title(f"matrice binaire detection {num_detect}")
    plt.imshow(np.array(mat_qr_code),cmap='Greys')
    num_detect += 1
    _id=analyse(mat_qr_code)
    print(_id)
    if _id>-1:
        reel_qr_code.append(_id)
plt.show()
print(reel_qr_code)


