from detection import *
from analyse_qr import analyse


liste_mat  = detection("images_tests/4tagsfourmis.png")
qr_codes=[]
for mat in liste_mat:
    _id=analyse(mat)
    if _id > -1:
        qr_codes.append(_id)
print(qr_codes)


