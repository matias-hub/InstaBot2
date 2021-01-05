import sqlite3

def bases_datos():
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS Usuaries(
               usuario text,
               contra text,
               tiempo text
               );""")
    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS lista_perfiles(
               perfil text,
               usuario text,
               echo text
               );""")
    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS ajustes(
               usuario text,
               lim_dia_foll INTEGER,
               lim_hora_foll INTEGER,
               lim_dia_unfoll INTEGER,
               lim_hora_unfoll INTEGER
               );""")
    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS ajustes2(
               usuario text,
               Solo_seg text,
               dosres INTEGER,
               mas_de_tantos INTEGER,
               dias INTEGER
               );""")
    conn.commit()
    conn.close()

    conn = sqlite3.connect("Unfollowd.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS seguidos (
        usuario text,
        seguidores text,
        dejado text)""")
    conn.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS cuando_seguido (
        usuario text,
        seguidores text,
        momento text)""")
    conn.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS seguidor (
        usuario text,
        seguidores text)""")
    conn.commit()
    conn.close()