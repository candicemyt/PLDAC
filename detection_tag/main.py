from detection import *
from analyse_qr import analyse

#liste_mat  = detection("images_tests/QR_reel_test.png")
liste_mat  = detection("images_tests/4tagsfourmis.png")
qr_codes=[]
for mat in liste_mat:
    _id=analyse(mat)
    if _id > -1:
        qr_codes.append(_id)
print(qr_codes)


# c= [[0,0,1,1],[1,0,1,1],[1,1,1,1],[0,0,0,0],[1,1,1,1]]
# print(analyse(c))
# new_c = np.flip(c).tolist()
# print(analyse(new_c))
# c= [[1, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0]]
# print(analyse(c))