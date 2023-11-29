from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import  Callable
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

from anticaptchaofficial.imagecaptcha import *

from .anticaptcha import solve_captcha

URL = "https://lk.rosreestr.ru/eservices/real-estate-objects-online"


def cache(func: Callable, reses: dict = {}):
    def wrapper(*args, **kwargs):
        if args[1] in reses:
            print("cached")
            return reses[args[1]]
        res = func(*args, **kwargs)
        reses[args[1]] = res
        return res

    return wrapper


class PageParser:
    def __init__(self):
        chrome_options = Options()
        chrome_options.page_load_strategy = 'normal'
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=chrome_options)
        # self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    @cache
    def parse(self, cad_id: str):
        self.driver.get(URL)
        time.sleep(2)

        xpath = "/html/body/div/div/div[1]/main/div/div[2]/div[4]/div[4]/label/div/div[1]/input"
        self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        self.driver.find_element(By.XPATH, xpath).send_keys(cad_id)

        captcha_element = self.driver.find_element(By.CLASS_NAME,
                                                   'rros-ui-lib-captcha-content-img')
        captcha_element.screenshot(f'bot/parser/parse_website/captchas/{cad_id} captcha.png')

        captcha_text = solve_captcha(f'.bot/parser/parse_website/captchas/{cad_id} captcha.png')

        captcha_field = "/html/body/div/div/div[1]/main/div/div[2]/div[4]/div[3]/div/div/label/div/div[1]/input"
        self.driver.find_element(By.XPATH, captcha_field).send_keys(captcha_text)

        button = self.driver.find_element(By.CLASS_NAME, "realestateMain-bottom-block").find_element(By.TAG_NAME,
                                                                                                     "button")
        self.wait.until(EC.element_to_be_clickable(button)).click()

        time.sleep(5)

        xpath = '/html/body/div[1]/div/div[1]/main/div/div[2]/div[6]/div/div[1]/div/div[2]/div/div[1]/div/a'
        self.driver.implicitly_wait(10)

        # self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

        # waits for id=row realestateobjects-wrapper__results to appear
        self.driver.find_element(By.CLASS_NAME, "realestateobjects-wrapper__results__cadNumber") \
            .find_element(By.TAG_NAME, "a").click()

        data = self.parse_data()
        self.driver.quit()
        self.__init__()
        return data

    def parse_data(self):
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "build-card-wrapper__info")))
        elements = self.driver.find_elements(By.CLASS_NAME, "build-card-wrapper__info")

        data = {}
        for element in elements:
            sub_elements = element.find_element(By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li")
            div_name = element.find_element(By.TAG_NAME, "h3").text
            data[div_name] = {}
            for sub_element in sub_elements:
                key = sub_element.find_element(By.CLASS_NAME, "build-card-wrapper__info__ul__subinfo__name").text
                options = sub_element.find_elements(By.CLASS_NAME,
                                                    "build-card-wrapper__info__ul__subinfo__options__item__line")
                value = "\n".join([option.text for option in options])
                data[div_name][key] = value

        return data
