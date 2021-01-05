from Crawler.browser import Browser
import sqlite3
import time
import random


def insta_Unfoll(Perfil):

    browser = Browser(Perfil)

    Lim_30_minutos = Perfil.lim_hora_unfoll
    Lim_diario = Perfil.lim_dia_unfoll

    print('limite_diario: ', Lim_diario)
    print('limite_mediahora: ', Lim_30_minutos)

    # habre una ventana, loguea y va hacia el perfil
    browser.login()

    Hora_inicio = int(time.strftime("%H"))

    seguidos = []
    nodejados = []
    dejados = []

    # utiliza los datos de la base
    connection = sqlite3.connect("Unfollowd.db")
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM cuando_seguido WHERE usuario = ? ", (Perfil.sesion_user, ))
    auxdata = cursor.fetchall()
    for i in range(0, len(auxdata)):
        seguidos.append(auxdata[i][2])

    connection = sqlite3.connect("Unfollowd.db")
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM seguidos WHERE usuario = ? AND dejado = ? ", (Perfil.sesion_user, 'unfollowed'))
    auxdata = cursor.fetchall()
    for i in range(0, len(auxdata)):
        dejados.append(auxdata[i][2])

    cursor.execute("SELECT rowid, * FROM seguidos WHERE usuario = ? AND dejado = ? ", (Perfil.sesion_user, 'not-unfollowed'))
    auxdata = cursor.fetchall()
    for i in range(0, len(auxdata)):
        nodejados.append(auxdata[i][2])
    connection.close()

    # elimina repetidos
    seguidos = list(dict.fromkeys(seguidos))
    print(len(seguidos), seguidos)

    connection = sqlite3.connect("Unfollowd.db")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM cuando_seguido WHERE usuario =?', (user,))
    perfiles_seguidos = cursor.fetchall()
    connection.close()
    cuando_seguidos = []

    for seg in perfiles_seguidos:
        if seg[-1] != '01/01/2001':
            cuando_seguidos.append(seg[1])
    for seg in seguidos:
        if seg not in cuando_seguidos:
            seguidos.remove(seg)

    # circula entre todos los perfiles que sigue el usuario
    for seg in seguidos:
        browser.driver.get('https://www.instagram.com/' + seg + '/')
        time.sleep(3)

        # levanta cantidad de seguidores

        followers = browser.buscarNumSeguidores()
        following = browser.buscarNumSeguidos()

        perfiles_mirar = []

        for items in seguidos:
            if items in nodejados or items in dejados:
                ''
            else:
                perfiles_mirar.append(items)

            # se ovserva hace cuanto se agrego al usuario
            connection = sqlite3.connect("Unfollowd.db")
            cursor = connection.cursor()
            cursor.execute('SELECT rowid, *  FROM cuando_seguido WHERE usuario = ? AND seguidores = ? ',
                           (Perfil.sesion_user, seg))
            items = cursor.fetchall()
            if len(items) < 1:
                cursor.execute('INSERT INTO cuando_seguido VAlUES(?,?,?)',
                               (Perfil.sesion_user, seg, str(time.strftime("%d/%m/%Y"))))
                connection.commit()
            connection.close()
            items = items[0]
            fecha = items[3]
            fecha = fecha.split('/')

            fecha_a = str(time.strftime("%d/%m/%Y"))
            fecha_a = fecha_a.split('/')

            diferencia = (int(fecha_a[1]) - int(fecha[1])) * 30 + int(fecha_a[0]) - int(fecha[0])
            diferencia = abs(diferencia)

            print('followers: ', followers, '   following: ', following, '     lim min:  ', Lim_minutos,
                  '     lim dia:  ', Lim_diario, '        ', seg, )

            if Perfil.solo_seguidores is True:
                masde = followers - 1

            # si no sigue al usuario, o sigue a mas perfiles de los que lo siguen, o tiene mas de 1000 seguidores, lo deja de seguir
            if seg not in seguidor or (followers * dosres) < following or followers > masde and diferencia > dias:
                if browser.check_exists_by_class('glyphsSpriteFriend_Follow',) is True:
                    time.sleep(3)
                    browser.driver.find_element_by_class_name('glyphsSpriteFriend_Follow').click()
                    time.sleep(4)
                    if browser.check_exists_by_class('-Cab_', ) is True:
                        browser.driver.find_element_by_class_name('-Cab_').click()
                    elif browser.check_exists_by_class('aOOlW -Cab_   ', ) is True:
                        browser.find_element_by_class_name('aOOlW -Cab_   ').click()
                    time.sleep(5)
                    unfollowd = True

                else:
                    print('no se encuentra el boton para dejar de seguir, salteado')

                if unfollowd is True:
                    # los perfiles dejados, quedan guardados para no volver a seguirlos
                    connection = sqlite3.connect("Unfollowd.db")
                    cursor = connection.cursor()
                    cursor.execute("""  UPDATE seguidos SET dejado =? WHERE usuario=? AND seguidores = ?""",
                                   ('unfollowed', Perfil.sesion_user, seg))
                    connection.commit()
                    connection.close()

                    # control para no ir mas rapido de lo que instagram deja
                    Lim_minutos = Lim_minutos - 1
                    Lim_diario = Lim_diario - 1
                    if Lim_diario < 1:
                        return
                    if Lim_minutos < 1:
                        print('********************************************************************')
                        print('Inicio del descanso', str(time.strftime("%H:%M:%S")))
                        print('********************************************************************')
                        time.sleep(400)
                        Lim_minutos = limite_mediahora
                        print('Fin del descanso', str(time.strftime("%H:%M:%S")))
                        print('********************************************************************')
            else:
                # si no fue dejado, se lo guarda para no volver a pasar por este devuelta
                connection = sqlite3.connect("Unfollowd.db")
                cursor = connection.cursor()
                cursor.execute("""  UPDATE seguidos SET dejado =? WHERE usuario=? AND seguidores = ?""",
                               ('not-unfollowed', Perfil.sesion_user, seg))
                connection.commit()
                connection.close()

        connection = sqlite3.connect("Unfollowd.db")
        cursor = connection.cursor()
        cursor.execute("SELECT rowid, * FROM seguidos WHERE usuario= ? AND seguidores = ?", (Perfil.sesion_user, seg))
        items = cursor.fetchall()

        # Todo el print para que entienda mejor el usuario
        if Perfil.solo_seguidores is True:
            if seg not in seguidor and diferencia > 7:
                print(str(seguidos.index(seg)), ' de ', str(len(seguidos)), '%30s' % items[0][2],
                      '   Dejado, No es seguidor')
                print('')
            else:
                print(str(seguidos.index(seg)), ' de ', str(len(seguidos)), '%30s' % items[0][2],
                      '   No fue dejado')
                print('')
        else:
            if seg not in seguidor and diferencia > 7:
                print(str(seguidos.index(seg)), ' de ', str(len(seguidos)), '%30s' % items[0][2],
                      '   Dejado, No es seguidor')
                print('')
            elif (followers * 1.3) < following and diferencia > 7:
                print(str(seguidos.index(seg)), ' de ', str(len(seguidos)), '%30s' % items[0][2],
                      '   Dejado, Muchos mas seguidos que seguidores')
                print('')
            elif followers > 1000 and diferencia > 7:
                print(str(seguidos.index(seg)), ' de ', str(len(seguidos)), '%30s' % items[0][2],
                      '   Dejado, Muchos seguidores')
                print('')
            elif (seg not in seguidor or (followers * 1.3) < following or followers > 10000) and diferencia < 7:
                print(str(seguidos.index(seg)), ' de ', str(len(seguidos)), '%30s' % items[0][2],
                      '   Agregado recientenmente')
                print('')
            else:
                print(str(seguidos.index(seg)), ' de ', str(len(seguidos)), '%30s' % items[0][2],
                      '   No fue dejado')
                print('')

    browser.close()