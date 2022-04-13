from detection import *
from analyse_qr import *

liste_mat  = detection("images_tests/QR_reel_test.png")
# for mat in liste_mat:
#     print(analyse(mat))


# c= [[0,0,1,1],[1,0,1,1],[1,1,1,1],[0,0,0,0],[1,1,1,1]]
# print(analyse(c))
# new_c = np.flip(c).tolist()
# print(analyse(new_c))
# c= [[1, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0]]
# print(analyse(c))