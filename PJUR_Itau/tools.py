import shutil
import time
import zipfile
import os
import smtplib
import pyautogui
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from datetime import date, timedelta, datetime
from requests import Session
from requests.auth import HTTPBasicAuth
import zeep
from zeep.transports import Transport

'''
def log(robo,erro):

	session = Session()
	session.auth = HTTPBasicAuth('admin', 'jive@2017')
	transport_with_basic_auth = Transport(session=session)

	client = zeep.Client(
		wsdl="https://jiveassetdev.service-now.com/x_jam_bd_logs_robos.do?wsdl",
		transport=transport_with_basic_auth
	)

	
	insert = client.service.insert(
		erro = erro,
		robo = robo
	)
'''

def conta_arquivo(caminhoDiretorio, caminhoErros=None):
    if caminhoErros is not None:
        try:
            num_lines = sum(1 for line in open(caminhoErros))
        except:
            num_lines = 0
    else: 
        num_lines = 0
    return sum([len(files) for r, d, files in os.walk(caminhoDiretorio)]) + num_lines

def existe_alerta(driver):
    try:
        driver.switch_to.default_content()
        driver.switch_to_alert()
    except:
        return False


def fecha_alerta_pega_texto(driver):
    try:
        driver.switch_to.default_content()
        alert = driver.switch_to_alert()
        alert_text = alert.text
        if driver.accept_next_alert:
            alert.accept()
        else:
            alert.dismiss()
            return alert_text
    finally:
        # accept_next_alert = True
        return True


def image_match(img):
    icon_pos = pyautogui.locateOnScreen(img)
    if icon_pos:
        pyautogui.click(icon_pos[0]+10, icon_pos[1]+10)
        return True
    else:
        return False


def mover_arquivo(arquivo, destino):
    shutil.move(arquivo, destino)


def dezipar(arquivo, destino):
    with zipfile.ZipFile(arquivo) as zf:
        zf.extractall(destino)


def dezipar_senha(arquivo, destino, senha):

    try:
        with zipfile.ZipFile(arquivo) as zf:
            zf.extractall(destino, pwd=senha)
            return True
    except:
        return False


def delete(caminho):

    try:
        os.remove(caminho)
        return True
    except:
        return False


def enviar_email(destinatarios, assunto, mensagem):

    email = "evandro15almeida@gmail.com"
    senha = "donamara86"

    corpo_do_email = """{0}""".format(mensagem)

    # make up message
    msg = MIMEText(corpo_do_email)
    msg['Subject'] = assunto
    msg['From'] = email
    msg['To'] = ", ".join(destinatarios)

    # sending
    session = smtplib.SMTP("smtp.gmail.com:587")
    session.starttls()
    session.login(email, senha)
    session.sendmail(email, destinatarios, msg.as_string())
    session.quit()


def enviar_anexo_email(send_to, subject, text, file=None):
    assert isinstance(send_to, list)

    # define content
    email = "evandro15almeida@gmail.com"
    senha = "donamara86"

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    with open(file, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(file)
        )
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
    msg.attach(part)

    smtp = smtplib.SMTP("smtp.gmail.com:587")
    smtp.starttls()
    smtp.login(email, senha)
    smtp.sendmail(email, send_to, msg.as_string())
    smtp.quit()


def dia_util_anterior(hoje):

    feriados = open(
        r"C:\Users\jive.automate\Desktop\ROTINAS\feriados.txt", "r").readlines()

    # isso é uma atribuição de variavel com a data de hoje, para loopar corretamente
    ontem = hoje

    while True:

        ontem = ontem - timedelta(1)

        data = "{0}/{1}/{2}".format('{:02d}'.format(ontem.day),
                                    '{:02d}'.format(ontem.month), str(ontem.year))
        dia_da_semana = ontem.isocalendar()[2]

        if (data in feriados):
            continue

        # 7 é domingo, 6 é sábado.
        elif (dia_da_semana == 6 or dia_da_semana == 7):
            continue

        else:
            return data


def dia_util_anteontem(hoje):

    feriados = open(
        r"C:\Users\jive.automate\Desktop\ROTINAS\feriados.txt", "r").readlines()

    # isso é uma atribuição de variavel com a data de hoje, para loopar corretamente

    ontem = hoje - timedelta(1)

    while True:

        ontem = ontem - timedelta(1)

        data = "{0}/{1}/{2}".format('{:02d}'.format(ontem.day),
                                    '{:02d}'.format(ontem.month), str(ontem.year))
        dia_da_semana = ontem.isocalendar()[2]

        if (data in feriados):
            continue

        # 7 é domingo, 6 é sábado.
        elif (dia_da_semana == 6 or dia_da_semana == 7):
            continue

        else:
            return data
