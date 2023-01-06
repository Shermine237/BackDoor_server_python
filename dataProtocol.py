# Pour etablir un protocol pour le transfert des donnees sur le canal

MAX_DATA_SIZE = 1024    # 1ko


def recieve_data(socket_p, data_len):
    current_data_len = 0
    total_data_recu = None
    # current_data_len c'est la taille des data qui sont en ce moment recu, au depart c'est 0
    # tant que le current_data_len n'est pas egal au data_len on continue la reception
    while current_data_len < data_len:
        # on reccupere les data avec la methode recv() en envoyant en parametre la taille max a reccuperer
        # la taille max a recuperer par tour est generalement MAX_DATA_SIZE = 1024
        # alors on divise le data_len en plusieurs morceaux inferieur a MAX_DATA_SIZE = 1024
        # si le data_restant_len est plus grand que MAX_DATA_SIZE = 1024 on le divise pour ne reccuperer que 1024
        # ainsi a la prochaine bouche on reccupere le reste et si le reste est toujour plus grand que 1024 on divise
        data_restant_len = data_len - current_data_len
        if data_restant_len > MAX_DATA_SIZE:
            data_restant_len = MAX_DATA_SIZE

        data_recu = socket_p.recv(data_restant_len)      # on recoit les donnees

        if not data_recu:    # si on ne recoit rien on quite en retournant None
            return None
        taille_data_recu = len(data_recu)
        current_data_len += taille_data_recu

        # si total_data_recu est toujour vide (au 1er tour de boucle) on lui donne les data recu
        # s'il a deja les data on ajoute juste les data recus
        if not total_data_recu:
            total_data_recu = data_recu
        else:
            total_data_recu += data_recu

        # mode verbeux : on l'affiche lorsque la taille des donnees est egal ou superieur a 1Mo
        if data_len >= MAX_DATA_SIZE * 1024:
            pourcentage = int((current_data_len / data_len) * 100)
            print(f"Total recu : {current_data_len}/ {data_len}     {pourcentage}%")

    return total_data_recu
