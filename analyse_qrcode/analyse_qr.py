import numpy as np
from generation_qrcode.generate_qr_codes import binary_qrcode, bit_parity

id_qr_code, valid_codes =binary_qrcode(3, 8)

def correction(qr_code_analyse,err):
    """corrige le QR code à partir d'une liste d'erreur err"""
    res=qr_code_analyse.copy()
    #on regarde où est le bit érroné
    if err[-1]==1 and sum(err[:-1])==0:
        # le problème correspond aux bits de parité
        # on calcul la matrice de bits de parité en fonction de la matrice identité
        par=bit_parity([qr_code_analyse[0]])
        res[1]=par
        res[2]=np.split(par)
    if err[-1]==0:
        #le problème correspond à la matrice identité
        #on récuère la ligne et la colonne du pixel qui pose pb
        l=err[0:2].index(1)
        c=err[2:6].index(1)
        #on change la valeur du bit
        res[0][l][c]=abs(res[0][l][c]-1)
    return res

def erreurs(qr_code_analyse):
    """détermine les erreurs présentes dans le QR code"""
    tmp=[]
    #on teste les lignes
    for l in range(2):
        if np.mod(np.sum(qr_code_analyse[0][l]),2)==qr_code_analyse[1][l]:
            tmp.append(0)
        else:
            tmp.append(1)
    #on teste les colonnes
    for c in range(4):
        col=0
        for l in range(2):
            col+=qr_code_analyse[0][l][c]
        if np.mod(col,2)==qr_code_analyse[1][2+c]:
            tmp.append(0)
        else:
            tmp.append(1)
    #on teste la matrice de parité inverse
    inv=sum(np.flip(qr_code_analyse[1])==qr_code_analyse[2])
    if inv == 6:
        tmp.append(0)
    else :
        tmp.append(1)
    return tmp

def in_liste_valide(qr_code_analyse):
    """détermine si un qr_code est dans la liste de QR codes valides"""
    for i in id_qr_code:
        if valid_codes[i] == qr_code_analyse:
            return i
    return -1

def analyse_unidirectionnel(qr_code):
    """essaie de déterminer l'identité d'un qr code
    fait une correction de 1 bit si nécessaire"""
    id = qr_code[0:2]
    par = qr_code[2:]
    par1 = par[0] + par[1][0:2]
    par2 = par[1][2:] + par[2]
    qr_code_analyse = [id, par1, par2]
    c = in_liste_valide(qr_code_analyse)
    if c >= 0:
        return c
    #il y a des erreurs dans le QR code, on regarde où elles sont
    err = erreurs(qr_code_analyse)
    #si il y a plus d'une erreur on s'arrête
    #1 bit erreur dans le QR code correspond à 1 ou 2 erreurs dans err
    if sum(err) <= 2:
        nouv_qr = correction(qr_code_analyse, err)
        c = in_liste_valide(nouv_qr)
        if c >= 0:
            return c
    return -1

def analyse(qr_code):
    """essaie de déterminer l'identité d'un qr code
    fait une rotation de 180° si nécessaire"""
    c=analyse_unidirectionnel(qr_code)
    if c >= 0:
        return c
    #on vas fait une rotation de 180 degré
    new_qr_code=np.flip(qr_code).tolist()
    c = analyse_unidirectionnel(new_qr_code)
    if c >= 0:
        return c
    print("il y a trop d'erreurs dans le qr code")
    return -1

#test
if __name__ == '__main__':
    """c= [[0,0,1,1],[1,0,1,1],[1,1,1,1],[0,0,0,0],[1,1,1,1]]
    print(analyse(c))
    new_c = np.flip(c).tolist()
    print(analyse(new_c))"""
    c= [[1, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0]]
    print(analyse(c))