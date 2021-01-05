from Crawler.browser import Browser
browser = Browser.driver

def login(browser):
    url = "https://www.instagram.com/accounts/login/?source=auth_switcher"
    browser.get(url)
    u_input = browser.find_one('input[name="username"]')
    u_input.send_keys(browser.sesion_user)
    p_input = browser.find_one('input[name="password"]')
    p_input.send_keys(browser.sesion_pass)

    login_btn = browser.find_one(".L3NKy")
    login_btn.click()

def buscarNumSeguidores(self):
    source = self.get_source(self)
    seguidores = source.split('<span class="g47SY " title="')[1]
    seguidores = seguidores.split('">')[0]
    seguidores = seguidores.replace(".", "")
    seguidores = seguidores.replace(",", "")
    seguidores = float(seguidores.replace("k", "000"))
    return  math.floor(seguidores)
