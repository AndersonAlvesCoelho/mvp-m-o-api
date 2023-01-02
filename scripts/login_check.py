import pandas as pd
import os
from datetime import date, timedelta
from selenium import webdriver
from datetime import date
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.service import Service as ChromiumService
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait


def checkLoginBrands(login, password, brand):

    if brand == "ApSystems":
        return apylogin(login, password)
    elif brand == "Aurora":
        return auroralogin(login, password)
    elif brand == "Canadian":
        return canadianlogin(login, password)
    elif brand == "Foxess":
        print("Foxess")
        return True
    elif brand == "Fronius":
        return froniuslogin(login, password)
    elif brand == "Fusion":
        return fusionlogin(login, password)
    elif brand == "GoodWe":
        return goodwelogin(login, password)
    elif brand == "Growatt":
        print("Growatt")
        return True
    elif brand == "Hoymiles":
        return hoymileslogin(login, password)
    elif brand == "Solarman":
        return solarmanlogin(login, password)
    elif brand == "Isolar":
        print("Isolar")
        return True
    elif brand == "SolarView":
        print("SolarView")
        return True
    elif brand == "Solarz":
        return solarzlogin(login, password)
    elif brand == "Solis":
        return solislogin(login, password)


#Fronius (headless)
def froniuslogin(login, pwrd):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # adiciona a opacao headless
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    navegador = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(
        chrome_type=ChromeType.CHROMIUM).install()), options=options)

    # Entra no site
    navegador.get("https://www.solarweb.com/PvSystems/Widgets")
    navegador.maximize_window()

    email_id = 'username'
    pass_id = 'password'
    login_id = 'submitButton'

    email_element = navegador.find_element(By.ID, email_id)
    password_element = navegador.find_element(By.ID, pass_id)
    login_element = navegador.find_element(By.ID, login_id)

    email_element.send_keys(f'{login}')
    password_element.send_keys(f'{pwrd}')

    login_element.click()
    try:
        check_path = '/html/body/article/div[1]/div/h3'
        check_path_ele = navegador.find_element(
            By.XPATH, check_path)  # Econtra o erro de login
        check = 0
    except:
        check = 1
    return check


# Canadian
def canadianlogin(login, pwrd):

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_argument("--headless")
    navegador = webdriver.Chrome(service=ChromiumService(
        ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
    navegador.get("https://monitoring.csisolar.com/login")  # Entra no site

    navegador.maximize_window()

    spam_class = '//*[@id="app"]/div[5]/div[3]/div/div[4]/button[1]'

    navegador.find_element(By.XPATH, spam_class).click()

    email_path = '//*[@id="app"]/div[5]/div[5]/div/section/div[2]/div[2]/div[3]/div/input'
    password_path = '//*[@id="app"]/div[5]/div[5]/div/section/div[2]/div[2]/div[4]/input'
    login_path = '//*[@id="app"]/div[5]/div[5]/div/section/div[2]/div[2]/button'

    email_element = navegador.find_element(By.XPATH, email_path)
    password_element = navegador.find_element(By.XPATH, password_path)
    login_element = navegador.find_element(By.XPATH, login_path)

    email_element.send_keys(f'{login}')
    password_element.send_keys(f'{pwrd}')

    login_element.click()
    try:
        time.sleep(3)
        check_login = "/html/body/div[1]/div[6]/div/div[3]/button"
        # Encontra o check box do erro de login
        checkelement = navegador.find_element(By.XPATH, check_login)
        check = 0
    except:
        check = 1
    return check


# Aurora
def auroralogin(login, pwrd):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")  # adiciona a opacao headless
    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(
        chrome_type=ChromeType.CHROMIUM).install()), options=options)

    # Site que se quer abrir
    # Entra no site
    driver.get("https://www.auroravision.net/ums/v1/loginPage?redirectUrl=https:%2F%2Fwww.auroravision.net%2Fdash%2Fhome.jsf&cause=MISSING_TOKEN")
    driver.maximize_window()

    driver.implicitly_wait(20)

    loginn = driver.find_element(By.ID, "userId")  # userAcct
    password = driver.find_element(By.ID, "password")

    loginn.send_keys(f'{login}')

    password.send_keys(f'{pwrd}')

    driver.find_element(By.NAME, "login-btn").click()

    try:
        # encontra o elemento do erro de login
        error = driver.find_element(By.ID, 'error_message_password').text
        check = 0
    except:
        check = 1

    return check


# APSystem
def apylogin(login, pwrd):

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")  # adiciona a opacao headless
    navegador = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(
        chrome_type=ChromeType.CHROMIUM).install()), options=options)
    navegador.implicitly_wait(15)

    navegador.get('https://apsystemsema.com/ema/index.action')  # Entra no site

    navegador.maximize_window()
    email_id = 'username'
    pass_id = 'password'
    login_id = 'Login'

    email_element = navegador.find_element(By.ID, email_id)
    password_element = navegador.find_element(By.ID, pass_id)
    login_element = navegador.find_element(By.ID, login_id)

    email_element.send_keys(f'{login}')
    password_element.send_keys(f'{pwrd}')

    login_element.click()
    try:
        # encontra o elemento do erro de login
        check_box = navegador.find_element(By.ID, 'ok')
        check = 0
    except:
        check = 1
    return check


# fusion
def fusionlogin(login, pwrd):

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")  # adiciona a opacao headless
    navegador = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(
        chrome_type=ChromeType.CHROMIUM).install()), options=options)
    navegador.implicitly_wait(120)

    # Entra no site
    navegador.get(
        'https://la5.fusionsolar.huawei.com/unisso/login.action?service=%2Funisess%2Fv1%2Fauth%3Fservice%3D%252F')

    navegador.maximize_window()
    email_id = '/html/body/div/div[2]/div[2]/div/div[3]/div[1]/div[2]/div[2]/div[3]/input[1]'
    pass_id = '/html/body/div/div[2]/div[2]/div/div[3]/div[1]/div[3]/div[3]/input'
    login_id = '/html/body/div/div[2]/div[2]/div/div[3]/div[4]/div/div/span'

    # Fazer login
    email_element = navegador.find_element(By.XPATH, email_id)
    password_element = navegador.find_element(By.XPATH, pass_id)
    login_element = navegador.find_element(By.XPATH, login_id)

    email_element.send_keys(f'{login}')
    password_element.send_keys(f'{pwrd}')
    time.sleep(1)
    login_element.click()
    try:
        # Encontra o elemento do erro de login
        check_box = navegador.find_element(By.ID, 'messageIcon')
        check = 0
    except:
        check = 1
    return check


# goodwe
def goodwelogin(login, pwrd):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")  # adiciona a opacao headless
    navegador = webdriver.Chrome(service=ChromiumService(
        ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)

    # entra no site
    navegador.get('https://www.semsportal.com/PowerStation/powerstatus')
    navegador.maximize_window()
    navegador.implicitly_wait(40)

    email_id = 'username'
    pass_id = 'password'
    login_id = 'btnLogin'

    email_element = navegador.find_element(By.ID, email_id)
    password_element = navegador.find_element(By.ID, pass_id)
    login_element = navegador.find_element(By.ID, login_id)

    email_element.send_keys(f'{login}')
    password_element.send_keys(f'{pwrd}')

    login_element.click()
    time.sleep(2)

    check_box = navegador.find_element(By.ID, 'err_msg').text
    if check_box == 'Email ou senha invalidos':  # Comparacao da msg de erro de login
        check = 0
    else:
        check = 1
    return check


# solarman
def solarmanlogin(login, pwrd):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")  # adiciona a opacao headless
    navegador = webdriver.Chrome(service=ChromiumService(
        ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
    navegador.implicitly_wait(20)

    # Entra no site
    navegador.get("https://pro.solarmanpv.com/business/maintain/plant")
    navegador.maximize_window()

    # Remove o spam do site
    spam_path = '/html/body/div[1]/div[1]/div/div/div[3]/div[2]/div/div[3]/button[1]'
    spam_element = navegador.find_element(By.XPATH, spam_path)
    time.sleep(1)
    spam_element.click()
    time.sleep(1)
    # Seleciona o usuario
    user_btnpath = '/html/body/div[1]/div[1]/div/div/div[3]/div[5]/section/div[2]/div[2]/div[1]/div/div[3]'
    user_btn_element = navegador.find_element(By.XPATH, user_btnpath)
    user_btn_element.click()
    email_path = '/html/body/div[1]/div[1]/div/div/div[3]/div[5]/section/div[2]/div[2]/div[2]/div/input'
    pass_path = '/html/body/div[1]/div[1]/div/div/div[3]/div[5]/section/div[2]/div[2]/div[3]/input'
    login_path = '/html/body/div[1]/div[1]/div/div/div[3]/div[5]/section/div[2]/div[2]/button'

    # Coloca o email
    email_element = navegador.find_element(By.XPATH, email_path)
    password_element = navegador.find_element(By.XPATH, pass_path)
    login_element = navegador.find_element(By.XPATH, login_path)

    email_element.send_keys(f'{login}')
    password_element.send_keys(f'{pwrd}')
    time.sleep(1)
    login_element.click()
    time.sleep(1)
    try:
        check_box = navegador.find_element(
            By.XPATH, '/html/body/div[1]/div[1]/div/div/div[4]/div/div[3]/button')  # encontra o erro de login
        check = 0
    except:
        check = 1

    return check


# solarz
def solarzlogin(login, pwrd):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")  # adiciona a opacao headless
    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(
        chrome_type=ChromeType.CHROMIUM).install()), options=options)

    # Site que se quer abrir
    driver.get("https://app.solarz.com.br/login")  # Entra no site
    driver.maximize_window()

    driver.implicitly_wait(7)  # seconds

    loginn = driver.find_element(By.ID, "username")  # userAcct
    password = driver.find_element(By.ID, "password")

    loginn.send_keys(f'{login}')
    password.send_keys(f'{pwrd}')

    login_btn_path = '/html/body/div/div/div[1]/form/input[3]'
    login_elment = driver.find_element(By.XPATH, login_btn_path)
    login_elment.click()
    try:
        # Encontra elemento dentro do user dashboard
        check_login = driver.find_element(
            By.XPATH, '/html/body/div[2]/div[1]/div/div[1]/div')
        check = 1
    except:
        check = 0
    return check


# solis
def solislogin(login, pwrd):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")  # adiciona a opacao headless
    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(
        chrome_type=ChromeType.CHROMIUM).install()), options=options)

    driver.get('https://m.ginlong.com/login.html')

    time.sleep(2)
    driver.maximize_window()

    proff_path = '/html/body/section/button'
    proff_element = driver.find_element(By.XPATH, proff_path)
    proff_element.click()

    loginn = driver.find_element(By.ID, "userName")  # userAcct
    password = driver.find_element(By.NAME, "password")

    loginn.send_keys(f'{login}')
    password.send_keys(f'{pwrd}')

    driver.find_element(By.ID, "login").click()
    time.sleep(5)
    try:
        check_login = driver.find_element(
            By.XPATH, '/html/body/section/div/ul/li[1]/div[1]/div')  # Encontra o erro de login
        if check_login.text == 'Nome de usuário / senha incorretos':
            check = 0
        else:
            driver.quit()
            check = 1
    except:
        driver.quit()
        check = 1
    return check


# hoymiles
def hoymileslogin(login, pwrd):

    df = pd.DataFrame(index=range(1), columns=['Plant_Name', 'Capacity', 'Country_Region',
                      'Address', 'Owner', 'Energy_today', 'Total_Reduction_Carbon', 'Carbon_emission_offset'])

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    navegador = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(
        chrome_type=ChromeType.CHROMIUM).install()), options=options)
    navegador.implicitly_wait(10)

    navegador.get('https://global.hoymiles.com/platform/login')

    navegador.maximize_window()

    email_path = '/html/body/div/div[2]/div[3]/form/div[1]/div[3]/div/div[3]/div/div/span/span/input'
    pass_path = '/html/body/div/div[2]/div[3]/form/div[1]/div[3]/div/div[4]/div/div/span/span/input'
    login_path = '/html/body/div/div[2]/div[3]/form/div[3]/div/div/span/button'

    email_element = navegador.find_element(By.XPATH, email_path)
    password_element = navegador.find_element(By.XPATH, pass_path)
    login_element = navegador.find_element(By.XPATH, login_path)

    email_element.send_keys(f'{login}')
    password_element.send_keys(f'{pwrd}')

    time.sleep(2)
    login_element.click()
    try:
        plant_name = '/html/body/section/section/main/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[2]/div/table/tr[1]/td[2]/span'
        plant_name_element = navegador.find_element(By.XPATH, plant_name)
        # print(plant_name_element.text)
        check = 1
    except:
        check = 0

    return check
