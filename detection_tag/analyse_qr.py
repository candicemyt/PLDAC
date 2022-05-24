import numpy as np
from generation_qrcode.generate_qr_codes import binary_qrcode


id_qr_code, valid_codes =binary_qrcode(3, 8)

def bit_parity(qr_code):
    """renvoie les bits de parité pour une matrice identité"""
    parity = []
    for line in qr_code[0]:  # un bit de parite par ligne
        if sum(line) % 2 == 0:
            parity.append(0)
        else:
            parity.append(1)
    for i in range(len(line)):  # un bit de parite par colonne de
        column = [row[i] for row in qr_code[0]]
        if sum(column) % 2 == 0:
            parity.append(0)
        else:
            parity.append(1)
    return parity


def correction(qr_code_analyse,err):
    """
    Corrige le QR code à partir d'une liste d'erreur err
    """

    res = qr_code_analyse.copy()
    #on regarde ou se trouve le bit errone

    if err[-1]==1 and sum(err[:-1])==0:
        # le bit errone est un bit de parité
        # on calcule la matrice de bits de parité en fonction de la matrice identité
        par=bit_parity([qr_code_analyse[0]])
        res[1]=par
        res[2]=np.split(par)
    if err[-1]==0:
        #le bit errone est un bit de la matrice identité
        #on récuère la ligne et la colonne du pixel qui pose probleme
        l=err[0:2].index(1)
        c=err[2:6].index(1)
        #on change la valeur du bit
        res[0][l][c]=abs(res[0][l][c]-1)
    return res


def erreurs(qr_code_analyse):
    """
    Détermine les erreurs présentes dans le QR code
    """
    erreurs=[]
    #on teste les lignes
    for l in range(2):
        if np.mod(np.sum(qr_code_analyse[0][l]),2)==qr_code_analyse[1][l]:
            erreurs.append(0)
        else:
            erreurs.append(1)
    #on teste les colonnes
    for c in range(4):
        col=0
        for l in range(2):
            col+=qr_code_analyse[0][l][c]
        if np.mod(col,2)==qr_code_analyse[1][2+c]:
            erreurs.append(0)
        else:
            erreurs.append(1)
    #on teste la matrice de parité inverse
    inv = sum(np.flip(qr_code_analyse[1])==qr_code_analyse[2])
    if inv == 6:
        erreurs.append(0)
    else :
        erreurs.append(1)
    return erreurs


def in_liste_valide(qr_code_analyse):
    """
    Détermine si un qr_code est dans la liste de QR codes valides
    """
    for i in id_qr_code:
        if valid_codes[i] == qr_code_analyse:
            return i
    return -1


def analyse_unidirectionnel(qr_code):
    """
    Tente de déterminer l'identité d'un qr code dans une direction
    fait une correction d'un bit si nécessaire
    """
    #on recupere la matrice identite
    id = qr_code[0:2]
    par = qr_code[2:]
    #on recupere la matrice de parité
    par1 = par[0] + par[1][0:2]
    #on recupere la matrice de parité inverse
    par2 = par[1][2:] + par[2]
    #on met le tout sous forme de liste
    qr_code_analyse = [id, par1, par2]
    #on regarde si le QR code fait partie des qr_code valides
    c = in_liste_valide(qr_code_analyse)
    #si c'est le cas on retourne l'id du qr code
    if c >= 0:
        return c
    #sinon il y a des erreurs dans le QR code, on regarde où elles sont
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
    """
    Essaie de déterminer l'identité d'un qr code
    fait une rotation de 180° si nécessaire
    => renvoie l'id du qr_code, et -1 sinon
    """
    #on fait l'analyse dans un sens
    c=analyse_unidirectionnel(qr_code)
    #si on a trouvé un id on s'arrête et on le renvoit
    if c >= 0:
        return c
    #sinon on fait une rotation de 180 degré et on fait l'analyse correspondante
    new_qr_code=np.flip(qr_code).tolist()
    c = analyse_unidirectionnel(new_qr_code)
    if c >= 0:
        return c
    #les deux analyses n'ont pas marchées
    # il y a trop d'erreurs dans le QR code ou alors le qr-code n'en est pas un
    print("Trop d'erreurs dans le QR code")
    return -1

