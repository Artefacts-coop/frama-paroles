import sqlite3
import pandas as pd
import streamlit as st
from streamlit_timeline import timeline
import altair as alt
import datetime


def main():

    db_channels = []

    # Interaction avec la base de données
    conn = sqlite3.connect("fake_data.sqlite")
    cursor = conn.cursor()

    # Requête des canaux
    results = requete(conn, f"SELECT * FROM channels")
    for r in results:
        db_channels.append(r[1])

    # --------------------------------------------

    # Sidebar
    st.sidebar.header("Anthropologue de la parole", divider="rainbow")

    year = st.sidebar.select_slider(
        "Année",
        options=list(range(2020, datetime.datetime.now().year + 1)),
        value=(2020, datetime.datetime.now().year),
    )

    channels = st.sidebar.multiselect(
        "Canaux", options=db_channels, default=db_channels
    )

    # Main
    st.header(f"Anthropologue de la parole {year[0]}-{year[1]}")
    if channels:
        st.subheader(f'Canaux : {", ".join(channels)}', divider="violet")

    # Requête des posts
    query = (
        "SELECT * FROM posts LEFT JOIN members ON posts.member_id=members.id WHERE channel_id IN (SELECT id FROM channels WHERE name IN (%s)) AND posts.create_at >= %s AND posts.create_at < %s"
        % (
            ",".join(['"' + channel + '"' for channel in channels]),
            datetime.datetime(year[0], 1, 1).timestamp(),
            datetime.datetime(year[1], 12, 31).timestamp(),
        )
    )
    results = requete(conn, query)
    posts = results

    # Affichage des statistiques des posts
    c = st.container()
    c.write("Nombre de posts : " + str(len(posts)))

    df_posts = pd.DataFrame(posts)    
    chart_data = pd.DataFrame(
        {
            "genres": ["Hommes", "Femmes"],
            "nombre de posts": [
                df_posts[df_posts[8] == "h"][8].count(),
                df_posts[df_posts[8] == "f"][8].count(),
            ],
            "col3": ["#FFC0CB", "#AAC7E6"],
        }
    )

    c.bar_chart(chart_data, x="genres", y="nombre de posts", color="col3")

    # --------------------------------------------

    # Fermeture de la connexion à la base de données
    conn.close()


def requete(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results


if __name__ == "__main__":
    main()
