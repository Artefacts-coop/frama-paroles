import sys
import sqlite3
import shutil


# Récupérer les arguments de la ligne de commande
args = sys.argv[1:]

# Récupérer le premier argument
file_input = args[0]


def replicate_db(file_input, file_output, columns_to_drop):
    """Copie la base de données sqlite file_input dans file_output, en supprimant certaines colonnes de certaines tables

    Args:
        file_input (str): Chemin vers la base de données d'origine
        file_output (str): Chemin vers la base de données répliquée
        columns_to_drop (dict): Dictionnaire avec les tables comme clés, et la liste des colonnes à supprimer comme valeurs
    """

    # Copier le fichier d'origine
    shutil.copyfile(file_input, file_output)

    # Créer la base de données répliquée
    conn_dst = sqlite3.connect(file_output)
    cur_dst = conn_dst.cursor()

    # Pour chaque table dans la base de données d'origine
    print(columns_to_drop)
    for table, columns in columns_to_drop.items():

        print(columns)

        for column_name in columns:
            if column_name in columns_to_drop.get(table, []):
                # Supprimer la colonne de la table
                cur_dst.execute(f"ALTER TABLE {table} DROP COLUMN {column_name};")
                # Mettre à jour la base de données de destination
                conn_dst.commit()

        # Mettre à jour la base de données de destination
        conn_dst.commit()

    # Fermer les curseurs
    cur_dst.close()

    # Fermer les connexions
    conn_dst.close()


replicate_db(
    file_input,
    "data.sqlite",
    {
        "members": ["username", "nickname", "email", "roles"],
        "posts": ["message"],
        "channels": ["display_name", "header", "purpose"],
    },
)
