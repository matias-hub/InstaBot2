from Crawler.browser import Browser
import sqlite3
import time

def actualizar_seguidores(Perfil):
    browser = Browser(Perfil)
    browser.login()

    # se dirige a la pagina principal del usuario y levanta el numero de segudores
    browser.get('https://www.instagram.com/' + Perfil.sesion_user + '/')

    seguidores = browser.buscarNumSeguidores()

    print(time.strftime("%H:%M"))

    # habre la lista de seguidores y scrolea hasta el final
    time.sleep(3)
    browser.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
    time.sleep(3)
    seguidor = []
    esperar = 0
    for i in range(1, seguidores):
        source = browser.driver.page_source
        print('viendo  ' + str(i) + ' de ' + str(seguidores) + ' seguidores')
        auxdata1 = source.split('<a class="FPmhX notranslate  _0imsa " title="')
        auxdata = auxdata1[-20:]
        time.sleep(1)
        for I in range(1, len(auxdata)):
            seguidor.append(str(auxdata[I]).split('"')[0])
            seguidor = list(dict.fromkeys(seguidor))
        path = ("/html/body/div[5]/div/div/div[2]/ul/div/li[" + str(i) + "]")
        if browser.check_exists_by_xpath(path,) is True:
            element = browser.driver.find_element_by_xpath(path);
            browser.driver.execute_script("arguments[0].scrollIntoView(true);", element);
        else:
            time.sleep(10)
            esperar = esperar + 1
        if esperar > 10:
            input('seguir ?')
            esperar = 0

    # borra los seguidores anteriores
    connection = sqlite3.connect("Unfollowd.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM seguidor WHERE usuario=? ", (Perfil.sesion_user,))
    connection.commit()

    # guarda todos los seguidores
    for i in range(0, len(seguidor)):
        cursor.execute("INSERT INTO seguidor VALUES(?,?)", (Perfil.sesion_user, seguidor[i]))
        connection.commit()
    connection.close()
    return
