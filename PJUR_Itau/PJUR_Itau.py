from selenium import webdriver
import csv
import os
import re
import shutil
import sys
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime

import pandas as pd
import pyautogui
from PyPDF2 import PdfFileReader, PdfFileWriter

import tools
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException,
                                        UnexpectedAlertPresentException)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

sys.path.insert(0, r"C:\Users\evand\Desktop\python")


class PJUR_Itau():
    """Doc String: Casse que irá retornar a execução total PJUR."""
    caminho_base = r"C:\Users\evand"
    downloads = r"{0}\Downloads".format(caminho_base)
    inicio_download = 0
    email = r"evandro15almeida@gmail.com"
    usuario = r"45642.OP06"
    senha = r"Eaac33DM*"

    def inicia_driver(self):
        path = r"chromedriver.exe"
        prefs = {"download.default_directory": self.downloads,
                 "profile.default_content_setting_values.automatic_downloads": 1,
                 "plugins.always_open_pdf_externally": True,
                 "download.prompt_for_download": False,
                 "profile.default_content_setting_values.notifications": 2,
                 "profile.managed_default_content_settings.stylesheets": 2,
                 # "profile.managed_default_content_settings.cookies": 2,
                 "profile.managed_default_content_settings.javascript": 1,
                 "profile.managed_default_content_settings.plugins": 1,
                 "profile.managed_default_content_settings.popups": 2,
                 "profile.managed_default_content_settings.geolocation": 2,
                 "profile.managed_default_content_settings.media_stream": 2
                 }
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option("prefs", prefs)

        chromeOptions.add_argument("--disable-web-security")
        chromeOptions.add_argument("--allow-running-insecure-content")
        chromeOptions.add_argument("--disable-extensions")
        chromeOptions.add_argument("--disable-print-preview")

        driver = webdriver.Chrome(executable_path=path,
                                  chrome_options=chromeOptions)
        return driver

    def limpar_downloads(self, downloads):
        """Doc String: ."""
        for file in os.listdir(downloads):
            if file.startswith("doc"):
                os.remove(downloads + "\\" + file)

    def login_PJUR(self):
        """Doc String: ."""
        while True:
            try:
                driver.get("https://www.google.com/?gws_rd=ssl")
                driver.get("https://ww39.itau.com.br/j146/pjuridico/")
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located
                                               ((By.XPATH,
                                                 """//*[@id="username"]""")))
                driver.find_element_by_xpath(
                    """//*[@id="username"]""").send_keys(self.usuario)
                driver.find_element_by_xpath(
                    """//*[@id="password"]""").send_keys(self.senha)
                driver.find_element_by_xpath("""//*[@id="button1"]""").click()
                break

            except TimeoutException:
                continue

    def navegaPjur(self):
        teste = 0
        fileOut = "ListaLinks.csv"
        pastaArquivos = r"{0}\Pjur".format(self.caminho_base)
        caminhos = [os.path.join(pastaArquivos, nomeArquivo)
                    for nomeArquivo in os.listdir(pastaArquivos)]
        reinicia = (len(caminhos))

        with open(r"Fila_Pjur.csv") as listaPjur:
            leitorCSV = csv.reader(listaPjur)
            next(leitorCSV, None)

            for linha in leitorCSV:
                """Rotina que fará a navegação nos documentos."""
                pyautogui.hotkey("ctrl", "l")
                javascript = "javascript:redirect('" + pyautogui.KEY_NAMES[71] + "/sistemas/o9/aspx/pjo9_proc_pesq.aspx" + pyautogui.KEY_NAMES[34] + \
                    "psdestino=" + \
                    pyautogui.KEY_NAMES[71] + "/modulos/andamento/consulta.aspx" + \
                    pyautogui.KEY_NAMES[34] + "acao=e', 'O9', 'F');"""
                pyautogui.typewrite(javascript, 0.02)
                pyautogui.press("enter")

                if teste == 1:
                    teste = 0

                nomeCasoID = linha[0]
                pastaDeletar = pastaArquivos + "\\" + nomeCasoID
                id = linha[2]
                try:
                    frame = driver.find_element_by_xpath(
                        """//*[@id="framePrincipal"]""")
                    driver.switch_to.frame(frame)
                except Exception as erro:
                    pass
                finally:
                    pass

                time.sleep(1)
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located
                                                ((By.XPATH,
                                                  """//*[@id="txtNumProcesso"]""")))
                driver.find_element_by_xpath(
                    """//*[@id="txtNumProcesso"]""").clear()
                driver.find_element_by_xpath(
                    """//*[@id="txtNumProcesso"]""").send_keys(id)
                driver.find_element_by_xpath(
                    """//*[@id="btnPesquisar"]""").click()
                time.sleep(2)
                index = 1

                try:
                    alert = driver.switch_to_alert()
                    alert_text = alert.text
                    alert.accept()
                    time.sleep(1)
                except:
                    while True:
                        time.sleep(1)
                        index = index + 1
                        listaLinks = []
                        existe = False

                        for a in driver.find_elements_by_xpath("""//*[@id="aspnetForm"]/table[2]/tbody/tr/td[5]/input[contains(@onclick,'exibirPopUpDocumentos')]"""):
                            existe = True
                            x = re.findall(
                                r"'\d+',", a.get_attribute("onclick"))[0]
                            x = x = re.findall(r"\d+", x)[0]
                            x = "https://ww39.itau.com.br/pjuridico/Modulos/Andamento/Andamentodocumento.aspx?andamento={0}&pasta={1}".format(
                                x, id)
                            listaLinks.append("{0},{1}".format(x, nomeCasoID))

                        if existe is False:
                            break

                        df = pd.DataFrame(listaLinks)
                        df.to_csv(fileOut, mode="a", index=False, header=False)
                        javascript = "__doPostBack('ctl00$ctl00$cphc$corpo$ucListaAndamento$pgDados','{0}')".format(
                            index)
                        try:
                            driver.execute_script(javascript)
                        except:
                            teste = 1
                            break

    def pega_links_documentos(self):
        fileOut = "ListalinksDocumentos.csv"
        pastaArquivos = ".\\PjurDocs".format(self.caminho_base)

        with open(r"ListaLinks.csv") as listaLinks:
            leitorCSV = csv.reader(listaLinks)

            for linha in leitorCSV:
                driver.get(linha[0])
                pasta = linha[1]
                indexTr = 0
                listaLinksDocumentos = []
                for a in driver.find_elements_by_xpath("""//*[@id="imgBaixar"]"""):
                    indexTr = indexTr + 1
                    tr = driver.find_element_by_xpath(
                        """//*[@id="ctl00_ctl00_cphc_corpo_Panel1"]/table/tbody/tr[{0}]""".format(indexTr)).text
                    nomeDocumento = tr.replace(" ", "_").replace(
                        "/", "").replace(":", "")

                    x = re.findall(r"\d", a.get_attribute("onclick"))
                    x = "".join(x)
                    x = "https://ww39.itau.com.br/pjuridico/Modulos/Documentos/Download.ashx?id={0},{1},{2}".format(
                        x, pasta, nomeDocumento)
                    listaLinksDocumentos.append(x)

                df = pd.DataFrame(listaLinksDocumentos)
                df.to_csv(fileOut, mode="a", index=False, header=False)

    def download_links(self, inicio_download):

        pastaDownloads = r"{0}\downloads".format(self.caminho_base)
        pyautogui.moveTo(100, 150)
        pyautogui.click()
        with open(r"ListalinksDocumentos.csv") as listaLinksDocumentos:
            leitorCSV = csv.reader(listaLinksDocumentos)
            for _ in range(inicio_download):
                next(leitorCSV, None)

            for linha in leitorCSV:
                self.inicio_download = self.inicio_download + 1
                time.sleep(1)
                nomeDocumento = ""
                doc = ""
                pastaArquivos = ".\\PjurDocs"
                documento_a_mover = ""
                url = linha[0]
                img = ".\\img\\alertaWindows.PNG"
                driver.get(url)

                pyautogui.moveTo(0, 150)
                pyautogui.click()
                time.sleep(2)
                if tools.image_match(img):
                    time.sleep(1)

                time.sleep(1)
                nomeDocumento = linha[2]
                pastaArquivos = "{0}\\{1}".format(
                    pastaArquivos, linha[1])
                try:
                    os.makedirs(pastaArquivos)
                except:
                    pass

                pastaArquivos = "{0}\\{1}".format(
                    pastaArquivos, nomeDocumento)

                if len(os.listdir(pastaDownloads)) != 0:
                    for doc in os.listdir(pastaDownloads):
                        documento_a_mover = pastaDownloads + "\\" + doc
                        while True:
                            pyautogui.moveTo(0, 150)
                            pyautogui.click()
                            if "crdownload" in doc:
                                time.sleep(2)
                            else:
                                break

                            for doc in os.listdir(pastaDownloads):
                                documento_a_mover = pastaDownloads + "\\" + doc
                                break

                        tools.mover_arquivo(
                            pastaDownloads + "\\" + doc, pastaArquivos + "." + doc.split(".")[1])

                else:
                    html = driver.page_source
                    if "Documento não encontrado no repositório" in html or "Object reference not set to an instance of an object" in html:
                        with open('erros.txt', 'a') as arq:
                            arq.write(str(linha))
                            arq.write('\n')

                    elif "O servidor Access Manager WebSEAL" in html or "Usuário atingiu o limite de execuções" in html or "TRAN/LTERM STOPPED" in html or "Falha no processamento, informe o administrador do sistema" in html or "The request failed with the error message" in html:
                        self.inicio_download = self.inicio_download - 1
                        driver.get(
                            "https://ww39.itau.com.br/j146/pjuridico/Autenticacao/logout.aspx")
                        driver.get("https://ww39.itau.com.br/j146/pjuridico/")
                        time.sleep(30)

                    elif "viewport" in html:
                        pyautogui.moveTo(0, 150)
                        pyautogui.click()
                        time.sleep(2)
                        pyautogui.hotkey("ctrl", "s")
                        time.sleep(4)
                        pyautogui.press("enter")
                        time.sleep(2)

                        for doc in os.listdir(pastaDownloads):
                            documento_a_mover = pastaDownloads + "\\" + doc
                            while True:
                                pyautogui.moveTo(0, 150)
                                pyautogui.click()
                                if ".png" not in doc and ".jpg" not in doc and ".bmp" not in doc:
                                    time.sleep(2)
                                else:
                                    break

                                for doc in os.listdir(pastaDownloads):
                                    documento_a_mover = pastaDownloads + "\\" + doc
                                    break

                            tools.mover_arquivo(
                                pastaDownloads + "\\" + doc, pastaArquivos + ".png")

                    else:
                        arquivo = open(pastaArquivos + ".htm", 'w')
                        arquivo.write(html)
                        arquivo.close()


if __name__ == "__main__":

    robo = "PJUR"
    driver = ""

    try:
        r = PJUR_Itau()
        driver = r.inicia_driver()
        inicio_download_default = tools.conta_arquivo(
            r"PjurDocs", r"erros.txt")
        r.inicio_download = int(pyautogui.prompt(
            text='Insira o inicio', title='Iniciar', default=inicio_download_default-1))
        r.login_PJUR()

        while True:
            try:
                r.limpar_downloads(r.downloads)
                # r.navegaPjur()
                # r.pega_links_documentos()
                r.download_links(r.inicio_download)
                break
            except Exception as erro:
                pass

    except Exception as erro:

        tb = traceback.format_exc()
        tools.enviar_email(['{0}}'], '%s - ERRO' % robo,
                           '(Para uso do desenvolvedor) \n Algo errado aconteceu \n  erro: \n {1}'.format(email, str(tb)))
        tools.log(robo, erro)

    finally:
        driver.quit()
