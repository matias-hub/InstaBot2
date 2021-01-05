import baseDatos
import sqlite3
from perfil import Perfil
from subfunciones import clear
from actualizarTablas import actualizar_seguidores
from followScrip import insta_Foll
from unfolloScript import insta_Unfoll
import time

def menu_prinsipal():
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    print('********************************************************************')
    print('                   bienvenide -- Insta.Bot')
    print('********************************************************************')
    print('')

    print('                     seleccione usuarie:')
    Perfiles = []
    c.execute("SELECT * FROM Usuaries")
    Usuaries = c.fetchall()
    for items in Usuaries:
        print(int(Usuaries.index(items)) + 1, items[0], )
        print('')

    print('0.', 'Otre')

    entrada = 'k'
    while entrada.isdigit() is False:
        entrada = str(input('...   '))

    clear()
    if entrada == '0':
        Use = input('Usuarie...')
        Pas = input('Contraseña...')
        c.execute("INSERT INTO Usuaries VALUES(?,?,?)", (Use, Pas, str(time.strftime("%d/%m---%H:%M"))))
        conn.commit()
        Usuaries = c.fetchall()
        conn.close()
    elif entrada in '101112013141516171819':
        entrada = int(entrada)
        Use = Usuaries[entrada - 1][0]
        Pas = Usuaries[entrada - 1][1]
    clear()

    Perfil.sesion_user = Use
    Perfil.sesion_pass = Pas
    return menu_secundario(Perfil)

def eliminar_use(Perfil):
    print('********************************************************************')
    print('                   Eliminando... -- ' + str(Perfil.sesion_user))
    print('********************************************************************')


    entrada = '0'
    while entrada not in 'siSInoNO':
        entrada = input('Seguro BORRAR '+ str(Perfil.sesion_user) + ".... SI / NO ..?")

    if entrada in 'noNO':
        return menu_prinsipal()
    else:
        connection = sqlite3.connect('Unfollowd.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM seguidos WHERE usuario=?', (Perfil.sesion_user,))
        cursor.execute('DELETE FROM seguidor WHERE usuario=?', (Perfil.sesion_user,))
        cursor.execute('DELETE FROM cuando_seguido WHERE usuario=?', (Perfil.sesion_user,))
        connection.commit()
        connection.close()


        connection = sqlite3.connect('menu.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM lista_perfiles WHERE usuario=?', (Perfil.sesion_user,))
        cursor.execute('DELETE FROM Usuaries WHERE usuario=?', (Perfil.sesion_user,))
        connection.commit()
        connection.close()
        time.sleep(1)
        clear()
        return menu_prinsipal()

def agregar_perf(Perfil):
    print('********************************************************************')
    print('                   Perfiles a agregar -- ' + str(Perfil.sesion_user))
    print('********************************************************************')
    print('')
    print('')

    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    c.execute("SELECT * FROM lista_perfiles WHERE usuario =:usuario", {'usuario': Perfil.sesion_user})
    perfiles_usuario = c.fetchall()
    conn.commit()
    conn.close()

    for items in range(0, len(perfiles_usuario)):
        print(perfiles_usuario[items][0], perfiles_usuario[items][2])
        print('')
    print('')
    print('1. Agregar perfiles a la lista')
    print('2. Eliminar perfiles a la lista')
    print('3. Iniciar, predeterminado')
    print('4. Iniciar, personalizado')
    print('5. Volver')

    entrada_1 = 'pop'
    while entrada_1 not in '12345':
        entrada_1 = str(input('....'))
    time.sleep(0.1)
    if entrada_1 == '1':
        print(
            'Agregue el nombre del perfil a agregar, de a uno a la vez, luego "Enter". Para terminar precione 0 + "Enter"')
        while entrada_1 != str(0):
            entrada_1 = input('...')
            if entrada_1 != str(0):
                connection = sqlite3.connect('menu.db')
                c = connection.cursor()
                c.execute("INSERT INTO lista_perfiles VALUES(?,?,?)", (entrada_1, Perfil.sesion_user, 'pendiente'))
                connection.commit()
                connection.close()
        clear()
        agregar_perf(Perfil)
    elif entrada_1 == '2':
        print(
            'Agregue el nombre del perfil a eliminar, de a uno a la vez, luego "Enter". Para terminar precione 0 + "Enter"')
        while entrada_1 != '0':
            entrada_1 = input('...')
            if entrada_1 != '0':
                connection = sqlite3.connect('menu.db')
                c = connection.cursor()
                c.execute('DELETE FROM lista_perfiles WHERE usuario=? AND perfil=?', (Perfil.sesion_user, entrada_1))
                connection.commit()
                connection.close()
        clear()
        agregar_perf(Perfil)
    elif entrada_1 == '3':

        connection = sqlite3.connect('menu.db')
        c = connection.cursor()
        c.execute("SELECT * FROM lista_perfiles WHERE usuario =? AND echo =?", (Perfil.sesion_user, 'pendiente',))
        perfiles = c.fetchall()
        connection.close()

        Perfiles = []
        for items in range(0, len(perfiles)):
            Perfiles.append(perfiles[items][0])

        Perfil.perfiles_seguir= Perfiles
        clear()
        print('inicio....')

        return insta_Foll(Perfil)

    elif entrada_1 == '4':

        Perfil.lim_dia_unfoll =  int(input('Limite diario ...'))
        Perfil.lim_hora_unfoll = input('Limite cada 30 minutos ...')
        connection = sqlite3.connect('menu.db')
        c = connection.cursor()
        c.execute("SELECT * FROM lista_perfiles WHERE usuario =? AND echo =?", (Perfil.sesion_user, 'pendiente',))
        perfiles = c.fetchall()
        connection.close()

        Perfiles = []
        for items in range(0, len(perfiles)):
            Perfiles.append(perfiles[items][0])

        Perfil.perfiles_seguir = Perfiles
        clear()
        print('inicio....')

        return insta_Foll(Perfil)


    elif entrada_1 == '5':
        clear()
        return menu_secundario(Perfil)

def eliminar_perf(Perfil):
    print('********************************************************************')
    print('                    Dejar de seguir con -- ' + str(Perfil.sesion_user))
    print('********************************************************************')
    print('')
    print('')

    print('1. Actualizar lista de seguidores')
    print('2. Eliminar un perfil de la tabla')
    print('3. Iniciar, predeterminado')
    print('4. Iniciar, personalizado')
    print('5. Volver')
    entrada = 'pop'
    while entrada not in '12345':
        entrada = str(input("..."))
    if entrada in '1':
        actualizar_seguidores(Perfil)
    elif entrada in '2':
        print('')
        print('')
        print('escriba un perfil a eliminar de la lista + enter, para finalizar 0')
        print('')
        print('')
        entrada = 1
        while entrada != '0':
            entrada = str(input("eliminar..."))
            connection = sqlite3.connect("Unfollowd.db")
            cursor = connection.cursor()
            cursor.execute("""  UPDATE seguidos SET dejado =? WHERE usuario=? AND seguidores = ?""",
                           ('unfollowed', Perfil.sesion_user, entrada))
            connection.commit()
            connection.close()
        return eliminar_perf(Perfil)
    elif entrada == '3':
        clear()
        return insta_Unfoll(Perfil)
    elif entrada == '4':

        Perfil.lim_dia_unfoll =  int(input('Limite diario ...'))
        Perfil.lim_hora_unfoll = input('Limite cada 10 minutos ...')
        clear()
        return insta_Unfoll(Perfil)

    else:
        return menu_secundario(Perfil)

def configuracion(Use, Pas, config):
    print('limite, dia seguir', config[2])
    print('limite, 30 minutos seguir', config[3])
    print('limite, dia dejar de seguir', config[4])
    print('limite, 10 minutos dejar de seguir', config[5])
    print('Solo dejar de seguir no seguidores',config[8])
    print('Taza de seguidos/seguidores para dejar',config[9])
    print('Dejar de seguir a partir de x seguidos:',config[10])
    print('Esperar x dias antes de dejar de seguir', config[11])

    print('')
    print('1. Cambiar')
    print('2. Volver')
    print('3. Restablecer')

    entrada = '0'
    while entrada not in '123':
        entrada = input('...')

    connection = sqlite3.connect('menu.db')
    cursor = connection.cursor()

    if entrada in '1':
        entrada = int(input('limite, dia seguir'))
        cursor.execute("""	UPDATE ajustes SET lim_dia_foll = ? WHERE usuario = ? """, (entrada, Use))

        entrada = int(input('limite, 30 minutos seguir'))
        cursor.execute("""	UPDATE ajustes SET lim_hora_foll = ? WHERE usuario = ? """, (entrada, Use))

        entrada = int(input('limite, dia dejar de seguir'))
        cursor.execute("""	UPDATE ajustes SET lim_dia_unfoll = ? WHERE usuario = ? """, (entrada, Use))

        entrada = int(input('limite, 10 minutos dejar de seguir'))
        cursor.execute("""	UPDATE ajustes SET lim_hora_unfoll = ? WHERE usuario = ? """, (entrada, Use))

        entrada='pop'
        while entrada not in 'siSISinoNoNO':
            entrada = input('Solo dejar de seguir "no seguidores" (SI/NO)')
        cursor.execute("""	UPDATE ajustes2 SET Solo_seg = ? WHERE usuario = ? """, (entrada, Use))

        entrada = float(input('Taza de seguidos/seguidores para dejar'))
        cursor.execute("""	UPDATE ajustes2 SET dosres = ? WHERE usuario = ? """, (entrada, Use))

        entrada = int(input('Dejar de seguir a partir de x seguidos:'))
        cursor.execute("""	UPDATE ajustes2 SET mas_de_tantos = ? WHERE usuario = ? """, (entrada, Use))

        entrada = int(input('Esperar x dias antes de dejar de seguir'))
        cursor.execute("""	UPDATE ajustes2 SET dias = ? WHERE usuario = ? """, (entrada, Use))

        connection.commit()
        connection.close()

    elif entrada in '3':
        cursor.execute("""	UPDATE ajustes SET lim_dia_foll = ? WHERE usuario = ? """, (400, Use))

        cursor.execute("""	UPDATE ajustes SET lim_hora_foll = ? WHERE usuario = ? """, (30, Use))

        cursor.execute("""	UPDATE ajustes SET lim_dia_unfoll = ? WHERE usuario = ? """, (300, Use))

        cursor.execute("""	UPDATE ajustes SET lim_hora_unfoll = ? WHERE usuario = ? """, (10, Use))

        cursor.execute("""	UPDATE ajustes2 SET Solo_seg = ? WHERE usuario = ? """, ('NO', Use))

        cursor.execute("""	UPDATE ajustes2 SET dosres = ? WHERE usuario = ? """, (1.3, Use))

        cursor.execute("""	UPDATE ajustes2 SET mas_de_tantos = ? WHERE usuario = ? """, (1000, Use))

        cursor.execute("""	UPDATE ajustes2 SET dias = ? WHERE usuario = ? """, (7, Use))

        connection.commit()
        connection.close()
    clear()
    menu_secundario(Use, Pas)

def menu_secundario(Perfil):
    clear()

    connection = sqlite3.connect("menu.db")
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM ajustes WHERE usuario = ?", (Perfil.sesion_user,))
    items = cursor.fetchall()

    if len(items) == 0:
        cursor.execute(
            "insert into ajustes (usuario, lim_dia_foll,lim_dia_unfoll,lim_hora_foll,lim_hora_unfoll) VALUES(?,?,?,?,?);",
            [Perfil.sesion_user, 400, 300, 30, 10 ])
        connection.commit()

    cursor.execute("SELECT rowid, * FROM ajustes2 WHERE usuario = ?", (Perfil.sesion_user,))
    items = cursor.fetchall()

    if len(items) == 0:
        cursor.execute(
            "insert into ajustes2 (usuario, Solo_seg,dosres,mas_de_tantos,dias) VALUES(?,?,?,?,?);",
            [Perfil.sesion_user, 'NO', 1.3, 1000, 7])
        connection.commit()

    connection = sqlite3.connect("menu.db")
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM ajustes WHERE usuario = ?", (Perfil.sesion_user,))
    connection.commit()
    config1 = cursor.fetchall()

    Perfil.lim_dia_foll = config1[0][2]
    Perfil.lim_dia_unfoll = config1[0][4]
    Perfil.lim_hora_foll = config1[0][3]
    Perfil.lim_hora_unfoll = config1[0][5]

    connection = sqlite3.connect("menu.db")
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM ajustes2 WHERE usuario = ?", (Perfil.sesion_user,))
    connection.commit()

    config2 =cursor.fetchall()
    connection.close()

    Perfil.solo_seg_seguidores = config2[0][2]
    Perfil.ratio_dejar = config2[0][3]
    Perfil.limite_sup_dejar = config2[0][4]
    Perfil.tiempo_min_dejar = config2[0][5]

    print('********************************************************************')
    print('                   bienvenide -- ' + str(Perfil.sesion_user))
    print('********************************************************************')

    print('')
    print('')
    print('')
    print('v. volver atras')
    print('0. Eliminar usuarie')
    print('1. Agregar Perfiles')
    print('2. Dejar de seguir perfiles')
    print('3. Configuracion')
    print('4. Agregar/Eliminar')
    print('5. Cambiar Contraseña')

    entrada = 'POP'
    while entrada not in '0123453vV':
        entrada = str(input('....  '))
    clear()

    if entrada == str(0):
        eliminar_use(Perfil)
        clear()
        return menu_prinsipal()

    if entrada == str(1):
        clear()
        return agregar_perf(Perfil)

    if entrada == str(2):
        clear()
        return eliminar_perf(Perfil)

    if entrada == str(3):
        clear()
        return configuracion(Perfil)

    if entrada in 'vV':
        clear()
        return menu_prinsipal()

    if entrada == "4":
        clear()
        conn = sqlite3.connect('menu.db')
        c = conn.cursor()
        c.execute("SELECT * FROM lista_perfiles WHERE usuario =? AND echo =?", (Use, 'pendiente',))
        perfiles = c.fetchall()
        conn.close()
        Perfiles = []
        for items in range(0, len(perfiles)):
            Perfiles.append(perfiles[items][0])
        print('inicio....')
        insta_Foll(Perfiles, config[2], config[3], 30, Use, Perfil.sesion_pass)

        insta_Unfoll(config[4], config[5], False, False, Use, Perfil.sesion_pass,config[8],config[9],config[10],config[11])

    if entrada == '5':
        clear()
        conn = sqlite3.connect('menu.db')
        c = conn.cursor()

        print('********************************************************************')
        print('                   Cambiar contraseña -- ' + str(Use))
        print('********************************************************************')

        print('')
        Perfil.sesion_pass = input('Nueva contraseña...')

        c.execute("update Usuaries set contra = ? where usuario = ?", (Perfil.sesion_pass, Use))
        conn.commit()
        conn.close()
        return menu_secundario(Use, Perfil.sesion_pass)

baseDatos.bases_datos()
menu = menu_prinsipal()