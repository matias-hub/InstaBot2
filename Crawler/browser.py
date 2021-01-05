import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from Crawler.utils import randmized_sleep
from perfil import Perfil
import math
import time

class Browser(Perfil):
    def __init__(self, has_screen):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        service_args = ["--ignore-ssl-errors=true"]
        chrome_options = Options()
        if not has_screen:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            executable_path='chromedriver',
            service_args=service_args,
            chrome_options=chrome_options,
        )
        self.driver.implicitly_wait(5)

    @property
    def page_height(self):
        return self.driver.execute_script("return document.body.scrollHeight")

    def get(self, url):
        self.driver.get(url)

    @property
    def current_url(self):
        return self.driver.current_url

    def implicitly_wait(self, t):
        self.driver.implicitly_wait(t)

    def find_one(self, css_selector, elem=None, waittime=0):
        obj = elem or self.driver

        if waittime:
            WebDriverWait(obj, waittime).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )

        try:
            return obj.find_element(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None

    def find(self, css_selector, elem=None, waittime=0):
        obj = elem or self.driver

        try:
            if waittime:
                WebDriverWait(obj, waittime).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
                )
        except TimeoutException:
            return None

        try:
            return obj.find_elements(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None

    def scroll_down(self, wait=0.3):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        randmized_sleep(wait)

    def scroll_up(self, offset=-1, wait=2):
        if offset == -1:
            self.driver.execute_script("window.scrollTo(0, 0)")
        else:
            self.driver.execute_script("window.scrollBy(0, -%s)" % offset)
        randmized_sleep(wait)

    def js_click(self, elem):
        self.driver.execute_script("arguments[0].click();", elem)

    def open_new_tab(self, url):
        self.driver.execute_script("window.open('%s');" %url)
        self.driver.switch_to.window(self.driver.window_handles[1])

    def close_current_tab(self):
        self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[0])

    def __del__(self):
        try:
            self.driver.quit()
        except Exception:
            pass

    def login(self):
        browser = self
        url = "https://www.instagram.com/accounts/login/?source=auth_switcher"
        browser.get(url)
        u_input = browser.find_one('input[name="username"]')
        u_input.send_keys(browser.sesion_user)
        p_input = browser.find_one('input[name="password"]')
        p_input.send_keys(browser.sesion_pass)

        login_btn = browser.find_one(".L3NKy")
        login_btn.click()
        inicial_url = self.driver.current_url
        current_url = inicial_url
        while inicial_url == current_url:
            time.sleep(1)
            current_url = self.driver.current_url

    def buscarNumSeguidores(self):
        source = self.driver.page_source
        seguidores = source.split('<span class="g47SY " title="')[1]
        seguidores = seguidores.split('">')[0]
        seguidores = seguidores.replace(".", "")
        seguidores = seguidores.replace(",", "")
        seguidores = float(seguidores.replace("k", "000"))
        return math.floor(seguidores)

    def buscarNumSeguidos(self):
        source = self.driver.page_source
        seguidores = source.split('</span> following</a></li></ul>')[1]
        seguidores = seguidores.split('">')[0]
        seguidores = seguidores.replace(".", "")
        seguidores = seguidores.replace(",", "")
        seguidores = float(seguidores.replace("k", "000"))
        return math.floor(seguidores)

    def get(self, url):
        self.driver.get(url)

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def check_exists_by_class(self, clas):
        try:
            self.driver.find_element_by_class_name(clas)
        except NoSuchElementException:
            return False
        return True

    def check_exists_by_name(self, name):
        try:
            self.driver.find_element_by_name(name)
        except NoSuchElementException:
            return False
        return True