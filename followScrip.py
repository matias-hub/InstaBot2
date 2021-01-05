from Crawler.browser import Browser
import sqlite3
import time
import random


def insta_Foll(Perfil):

    browser = Browser(Perfil)

    Lim_30_minutos = Perfil.lim_hora_foll
    Lim_diario = Perfil.lim_dia_foll

    print('limite_diario: ', Lim_diario)
    print('limite_mediahora: ', Lim_30_minutos)

    # habre una ventana, loguea y va hacia el perfil
    browser.login()

    Hora_inicio = int(time.strftime("%H"))

    # abre lista de personas que  dejado de seguir en el pasado
    connection = sqlite3.connect("Unfollowd.db")
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM cuando_seguido WHERE usuario = ? ", (Perfil.sesion_user,))
    items = cursor.fetchall()
    dontfollow = []
    for item in items:
        dontfollow.append(item[2])
    connection.close()

    # circula en perfiles donde agregar
    for perfil in Perfil.perfiles_seguir:
        # ir al perfil señalado
        browser.driver.get('https://www.instagram.com/' + perfil + '/?hl=en')

        # lee la cantidad de followers
        followers = browser.buscarNumSeguidores()

        # abrer la lista defollowers
        time.sleep(3)
        browser.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()
        time.sleep(5)

        # variables reseteables en cada perfil
        personas = []
        personas2 = []
        estado = []
        Per_Es = {}

        # da tiempo a cargar
        time.sleep(10)

        # scrollea hacia abajo y luego al inicio para cargar
        path = ("/html/body/div[4]/div/div/div[2]/ul/div/li[12]")
        path2 = ("/html/body/div[5]/div/div/div[2]/ul/div/li[12]")
        if browser.check_exists_by_xpath(path,) is True:
            element = browser.driver.find_element_by_xpath(path);
            browser.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        elif browser.check_exists_by_xpath(path2,) is True:
            element = browser.driver.find_element_by_xpath(path2);
            browser.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(2)

        # mira toda la lista de seguidores
        for i in range(1, int(followers - 10)):
            # scroll dentro de ventana de dialogo
            path = ("/html/body/div[4]/div/div/div[2]/ul/div/li[" + str(i) + "]")
            path2 = ("/html/body/div[5]/div/div/div[2]/ul/div/li[" + str(i) + "]")
            if browser.check_exists_by_xpath(path,) is True:
                element = browser.driver.find_element_by_xpath(path);
                browser.driver.execute_script("arguments[0].scrollIntoView(true);", element);
            elif browser.check_exists_by_xpath(path2, ) is True:
                element = browser.driver.find_element_by_xpath(path2);
                browser.driver.execute_script("arguments[0].scrollIntoView(true);", element);
            else:
                time.sleep(2)
                if browser.check_exists_by_xpath(path, ) is True:
                    element = browser.driver.find_element_by_xpath(path);
                    browser.driver.execute_script("arguments[0].scrollIntoView(true);", element);
                else:
                    print('break')
                    break
            time.sleep(0.1)

            # obtiene los nombres de los perfiles y si se pueden seguir
            source = browser.driver.page_source
            elementos = source.split('wo9IH')
            elementos.pop(0)
            if 'uu6c_' not in elementos[-1]:
                elementos.pop(-1)
            for t in range(+len(Per_Es) - len(elementos), -1):
                personas.append(str(elementos[t]).split('><img alt="')[1])
                personas2.append(str(personas[-1]).split("\'s profile picture")[0])
                if 'profile picture" class' in personas2[-1]:
                    personas2.pop(-1)
                estado.append(str(elementos[t]).split('type="button">')[-1])
                # armar un diccionario con usuario y condicon
                Per_Es[str(personas2[-1])] = str(estado[-1]).split('</button>')[0]

            # si el usuario sigue al perfil corrije un diccionario
            if Perfil.sesion_user in Per_Es:
                Per_Es[Perfil.sesion_user] = 'Following'

            # chekea que no se cargue la lista y le da tiempo o pasa a otro perfil
            if len(personas2) < (i + 1):
                print('Instagram con lag, reiniciaando . . . ')
                browser.quit()
                Perfil.lim_dia_foll=Lim_diario
                Perfil.lim_hora_foll=limite_mediahora
                return insta_Foll(Perfil)

            if len(personas2) < (i + 2):
                time.sleep(30)
                path = ("/html/body/div[4]/div/div/div[2]/ul/div/li[" + str(i - 10) + "]")
                if browser.check_exists_by_xpath(path, ) is True:
                    element = browser.driver.find_element_by_xpath(path);
                    browser.driver.execute_script("arguments[0].scrollIntoView(true);", element);
                time.sleep(30)
                path = ("/html/body/div[4]/div/div/div[2]/ul/div/li[" + str(i) + "]")
                if browser.check_exists_by_xpath(path, ) is True:
                    element = browser.driver.find_element_by_xpath(path);
                    browser.driver.execute_script("arguments[0].scrollIntoView(true);", element);
                time.sleep(5)

            if personas2[i - 1] in dontfollow:
                print('Viendo perfil numero: ', i, '%30s' % personas2[i - 1], ', Ya fue seguida en algun momento')
            else:
                print('Viendo perfil numero: ', i, '%30s' % personas2[i - 1], ',', Per_Es[personas2[i - 1]],
                      Lim_30_minutos, Lim_diario)

            # sigue a las personas que puede, que no alla dejado de seguir
            if Per_Es[personas2[i - 1]] == 'Follow' and personas2[i - 1] not in dontfollow:
                time.sleep(2)
                Lim_30_minutos = Lim_30_minutos - 1
                Lim_diario = Lim_diario - 1

                # clikea
                button = ("/html/body/div[4]/div/div/div[2]/ul/div/li[" + str(i) + "]/div/div[2]/button")
                button2 = ("/html/body/div[4]/div/div/div[2]/ul/div/li[" + str(i) + "]/div/div[3]/button")
                button3 = ("/html/body/div[5]/div/div/div[2]/ul/div/li[" + str(i) + "]/div/div[2]/button")
                button4 = ("/html/body/div[5]/div/div/div[2]/ul/div/li[" + str(i) + "]/div/div[3]/button")
                if browser.check_exists_by_xpath(button, ) is True:
                    browser.driver.find_element_by_xpath(button).click()
                    time.sleep(random.randint(2, 3))
                elif browser.check_exists_by_xpath(button2, ) is True:
                    browser.driver.find_element_by_xpath(button2).click()
                    time.sleep(random.randint(2, 3))
                elif browser.check_exists_by_xpath(button3, ) is True:
                    browser.driver.find_element_by_xpath(button3).click()
                    time.sleep(random.randint(2, 3))
                elif browser.check_exists_by_xpath(button4, ) is True:
                    browser.driver.find_element_by_xpath(button4).click()
                    time.sleep(random.randint(2, 3))
                else:
                    print('FALLO EL CLICK')

                # guarda la fecha cuando se agrego
                connection = sqlite3.connect("Unfollowd.db")
                cursor = connection.cursor()
                cursor.execute('INSERT INTO cuando_seguido VAlUES(?,?,?)',
                               (Perfil.sesion_user, personas2[i - 1], str(time.strftime("%d/%m/%Y"))))
                connection.commit()

            # si termina un perfil lo guarda
            if i > int(followers - 15):
                conn = sqlite3.connect('menu.db')
                c = conn.cursor()
                c.execute("UPDATE lista_perfiles SET echo = 'listo' WHERE perfil =? AND usuario = ?", (perfil, Perfil.sesion_user))
                conn.commit()
                conn.close()

            # chekea limite diario y horario
            if Lim_diario < 1:
                print('Limite diario')
                break
            if Lim_30_minutos < 1:
                print('********************************************************************')
                print('Inicio del descanso', str(time.strftime("%H:%M:%S")))
                print('********************************************************************')
                time.sleep(random.randint(Espera * 59, Espera * 69))
                Lim_30_minutos = limite_mediahora
                print('Fin del descanso', str(time.strftime("%H:%M:%S")))
                print('********************************************************************')
    browser.driver.close()

