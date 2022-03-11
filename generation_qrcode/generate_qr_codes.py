from scipy.spatial.distance import hamming
import svgwrite as svg

def binary_qrcode(h_distance, nb_bit):
    """renvoie des qr codes sous forme de liste de 0 et 1
    avec nb_bit d'informartions (doit etre pair ou divisible par 3)
    et une distance de hamming de h_distance"""


    bin_ids = []    #liste des nombre en binaire de 0 à 2^nb_bit
    for i in range(2 ** nb_bit):
        bin_id = [int(j) for j in bin(i)[2:]]
        len_bin_id = len(bin_id)
        if len_bin_id < nb_bit:
            bin_id = [0] * (nb_bit - len_bin_id) + bin_id
        bin_ids.append(bin_id)

    flat_qr_codes = bin_ids #liste des qr_codes non mis en forme pour le calcul de la hamming distance


    #mise en forme de la matrice des bits d'informations
    if nb_bit % 3 == 0:
        shape = (int(nb_bit / 3), int(nb_bit / 3 + 3))
        qr_codes = [[[bin_id[0:shape[0]], bin_id[shape[0]:shape[1]], bin_id[shape[1]:len(bin_id)]]] for bin_id in
                    bin_ids]
    elif nb_bit % 2 == 0:
        shape = int(nb_bit / 2)
        qr_codes = [[[bin_id[0:shape], bin_id[shape:len(bin_id)]]] for bin_id in bin_ids]
    else:
        print('Donner un nombre de bit pair ou divisible par 3')
        return


    id_v_qr_code = [0]  #liste des indices des qr_codes à garder (avec une hamming distance inferieure a h_ditance)

    for k in range(len(qr_codes)):

        #ajout des bits de parite
        parity = []
        for line in qr_codes[k][0]:     #un bit de parite par ligne

            if sum(line) % 2 == 0:
                parity.append(0)
            else:
                parity.append(1)

        for i in range(len(line)):  #un bit de parite par colonne de
            column = [row[i] for row in qr_codes[k][0]]
            if sum(column) % 2 == 0:
                parity.append(0)
            else:
                parity.append(1)

        qr_codes[k].append(parity)
        qr_codes[k].append(parity[::-1])    #ajout de l'inverse des bits de parite
        flat_qr_codes[k] += parity + parity[::-1]


        # hamming distance
        len_id_v_qr_code = len(id_v_qr_code)
        add = True  #booleen indiquant si le qr_code est valide (hamming distance entre lui et tous ceux deja valide inferieure a h_distance)
        for index in range(len_id_v_qr_code):
            if hamming(flat_qr_codes[id_v_qr_code[index]], flat_qr_codes[k]) * len(flat_qr_codes[k]) <= h_distance:
                add = False
                break
        if add:
            id_v_qr_code.append(k)

    return id_v_qr_code, [qr_codes[i] for i in id_v_qr_code]



def draw_qrcodes(qr_codes,outline, spacing):

    #reformatage des qr codes en matrice
    shape = len(qr_codes[0][0][0])
    qr_codes_reshaped = []
    for qr_code in qr_codes:
        parity_bits = qr_code[1] + qr_code[2]
        i= 0
        j=shape
        while j <= len(parity_bits):
            qr_code[0].append(parity_bits[i:j])
            i+=shape
            j+=shape
        qr_codes_reshaped.append(qr_code[0])


    #initialisation du fichier svg
    d = svg.Drawing(filename=f"out/qr_codes_{outline}outlinev3.svg", size=("2000px", "2000px"))
    size = 10   #taille des bits
    cpt = 0     #compteur permettant la disposition des qr codes dans le fichier
    cpt_outline = 0     #compteur permettant de calibrer correctement les contours
    x = size*5*((cpt//16) + 1)*spacing[1] #abscisses du bit a dessiner (1.8 = gestion de l'espacement entre les colonnes de qr_codes)
    y = size*5  #ordonnée du bit a dessiner


    #dessin des qr_codes
    for qr_code in qr_codes_reshaped:

        #ajout de differents bit en fonction de l'outline
        if outline == 0:    #seulement un bit au dessus pour l'orientation visible pour l'homme
            d.add(d.rect(insert=(x + size * 3 / 2, y), size=(size, size), fill='black'))
            y += size+3/4*size

        elif outline == 1:  #ajout de lignes noires au dessus et en dessous de la matrice
            orientation_line = [1]*shape
            orientation_line[shape//2] = 0  #un bit blanc dans la ligne du dessus pour l'orientation visible pour l'homme
            qr_code.insert(0,orientation_line)
            qr_code.append([1]*shape)

        elif outline == 2:  #ajout de lignes blanches puis noires au dessus et en dessous de la matrice
            qr_code.insert(0,[0]*shape)
            orientation_line = [1] * shape
            orientation_line[shape // 2] = 2     #un bit blanc dans la ligne du dessus pour l'orientation visible pour l'homme
            qr_code.insert(0, orientation_line)
            qr_code.append([0] * shape)
            qr_code.append([1] * shape)


        #dessin des bits des qr_codes
        for line in qr_code:

            if outline >= 1:    #pour un ou deux contours on ajoute un bit noir au debut de chaque ligne
                d.add(d.rect(insert=(x, y), size=(size, size), fill='black'))
                x += size

            if outline == 2:    #pour deux contours on ajoute un bit blanc au debut de chaque ligne
                if cpt_outline == 0 or cpt_outline == len(qr_code)-1:   #un bit noir au niveau des coins
                    d.add(d.rect(insert=(x, y), size=(size, size), fill='black'))
                    x += size
                else:
                    d.add(d.rect(insert=(x, y), size=(size, size), fill='white'))
                    x += size

            cpt_outline+=1  #gestion des bits noirs aux coins

            for b in line:  #dessin des bits de la matrice
                if b == 1:
                    d.add(d.rect(insert=(x, y), size=(size, size), fill='black'))
                elif b == 0:
                    d.add(d.rect(insert=(x, y), size=(size, size), fill='white'))
                else:
                    d.add(d.rect(insert=(x, y), size=(size, size), fill='white'))
                    d.add(d.rect(insert=(x, y+(size*1/4)), size=(size, size*3/4), fill='black'))
                x += size

            if outline == 2: #pour deux contours on ajoute un bit blanc a la fin de chaque ligne
                if cpt_outline == 1 or cpt_outline == len(qr_code) :
                    d.add(d.rect(insert=(x, y), size=(size, size), fill='black'))
                    x += size
                else:
                    d.add(d.rect(insert=(x, y), size=(size, size), fill='white'))
                    x += size

            if outline >= 1:    #pour un ou deux contours on ajoute un bit noir a la fin de chaque ligne
                d.add(d.rect(insert=(x, y), size=(size, size), fill='black'))
                x += size

            y += size   #a la fin de chaque ligne on augmente l'ordonnee pour passer a la ligne suivante
            x = size*5*((cpt//16) + 1) *spacing[1]  #on remet x a sa valeur d'initialisation (1.8 = gestion de l'espacement entre les colonnes de qr_codes)

        cpt_outline = 0 #gestion des bits noirs aux coins
        # gestion du placement des qr_codes dans le fichier
        cpt += 1
        if cpt % 16 == 0:   #on fait des lignes de 16 (16*16=256)
            y = size*5  #valeur initaiale du y
            x = size*5*((cpt//16) + 1 ) *spacing[1]  #nouvelle abscisse pour la prochaine colonne (1.8 = gestion de l'espacement entre les colonnes de qr_codes)
        else:
            y += size * spacing[0]#espacement entre les lignes de qr_codes

    #sauvegarde du fichier
    d.save()



####################### generation qr_codes optimaux ############################


id_qr_code, qr_codes = binary_qrcode(3, 8)
outline = 2
#espacements : grand = (2,2), moyen = (1, 1.8), petit = (0.5, 1.6)
draw_qrcodes(qr_codes[1::], outline=outline,spacing=(1,1.8))


############ etude des qr codes optimaux #############

# for h_distance in range(2,5):


#     for nb_bit in [6,8,9]:
#         id_qr_code, qr_codes = qrcode(h_distance, nb_bit)
#         print('---------------\t', nb_bit, ' bits avec une hamming distance de ', h_distance, '\t---------------\n')
#         print('\t ', len(id_qr_code), ' QR codes\n')
#         f = open(f"QR_codes_{nb_bit}bits_{h_distance}distance.txt", 'w')
#         for qr_code in qr_codes:
#             f.write(str(qr_code) +'\n')
#         #print(id_qr_code, '\n', qr_codes,'\n\n')


# id_qr_code, qr_codes = qrcode(6, 8)
# print('\t ', len(id_qr_code), ' QR codes\n')