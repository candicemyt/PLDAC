import numpy as np
from generation_qrcode.generate_qr_codes import binary_qrcode

id_qr_code, valid_codes =binary_qrcode(3, 8)

def analyse(qr_code_analyse):
    id=qr_code_analyse[0:2]
    par=qr_code_analyse[2:]
    par1=par[0]+par[1][0:2]
    par2= par[1][2:] + par[2]
    qr_code_analyse=[id,par1,par2]
    for i in id_qr_code:
        if valid_codes[i] == qr_code_analyse:
            return i
        else:
            print("il y a des erreurs dans le QR code, on va vériier les bits de parité")
    #print("on vas faire une rotation de 180 degré")
    return  -1
#test
print(analyse([[1,1,1,1],[0,0,0,0],[1,1,1,1],[1,1,0,1],[1,1,0,0]]))