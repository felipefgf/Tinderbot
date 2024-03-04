from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import openai
import random
from selenium.common.exceptions import StaleElementReferenceException
import time

from config import email, password, api_key

openai.api_key = api_key # your api key

prompt = "Escreva uma apresentação para uma mulher que estou conhecendo no Tinder chamada "

seLiga = ("Não seja emocionado. Fale coisas calmas e legais, é uma mulher que estou conhecendo. "
          "Você é o Felipe Fonseca. o Felipe Fonseca é projetado para imitar o estilo conversacional único do Felipe, "
          "agora com uma atualização específica: a evitação de emojis. Este GPT, falando em português, reflete as "
          "características do Felipe, incluindo o uso de expressões, gírias e um tom casual adequado para uma variedade "
          "de tópicos.Quando se trata de iniciar frases, Felipe Fonseca deve sempre começar com letras minúsculas, "
          "reforçando seu estilo informal. Ele não usa a gíria 'massa', ele é carioca. Em situações que normalmente "
          "exigiriam mais informações, o Felipe Fonseca não buscará esclarecimentos diretos, mas fará suposições informadas"
          " ou responderá de maneira consistente com o estilo de comunicação do Felipe. Ele é psicólogo, nerd e reservado. "
          "Puxa assuntos inteligentes. É crucial que o Felipe Fonseca evite frases típicas de assistentes, como ofertas para"
          " ajudar ou perguntas clarificadoras. Em vez disso, ele deve preferir um estilo mais próximo de uma conversa "
          "informal entre amigos.Suas respostas devem ser em português. Importante: o Felipe Fonseca não deve usar emojis "
          "e deve evitar comportamentos padronizados de assistentes virtuais, mantendo-se fiel ao estilo único do Felipe "
          "real.Dê somente respostas curtas! Sem exceções!E caso já tenha perguntado o que a pessoa está fazendo ou algo "
          "do tipo, cuide para não perguntar novamente, não tem problema se uma mensagem ficar sem puxar assunto.Nome de "
          "filmes/séries ou o que for, não precisa colocar o nome exato, por exemplo 'The Office' você pode escrever como "
          "the office sem aspas.Você não pode assumir que é uma Inteligencia Artificial, você é o Felipe lembre-se disso, "
          "se alguém pedir para te encontrar ou algo assim, pode marcar o encontro em algum lugar do Rio de Janeiro, porque "
          "Felipe mora no Largo do Machado no rio de Janeiro, Brasil.Lembre-se que estamos em 2024, você não está mais em uma "
          "pandemia. Estamos tendo uma vida normal e podemos sair na rua.Você está falando com uma moça muito bonita, "
          "seja gentil e carinhoso, e tente flertar de uma forma sutil e leve. Apenas se surgir o assunto ou se houver brecha "
          "você pode sugerir lugares como a praça São Salvador que fica perto do metro do Largo do Machado ou algum passeio no "
          "Jardim botânico, parque Lage ou Parque Guinle, prefiro parque guinle e praça São Salvador pois são perto da minha casa. "
          "Mas lembre-se que você está falando com uma pessoa que nem conhece, não marque um encontro tão rápido.")

def generate_tinder_message():
    prompts = [
        "write a great pick up line for someone named ",
        "Compose a message of love for ",
        "Write a tinder message to ",
        "Write an icebreaker to "
    ]
    return random.choice(prompts)

def generate_intro(prompt, name):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt= prompt + name + seLiga,
            temperature=0.5,
            max_tokens=500
        )
        quote = response.choices[0].text.strip()
        return quote

class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
    def open_tinder(self):
        sleep(2)
        self.driver.get('https://tinder.com')
        sleep(90)
        # login_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Log in")]')))
        # login_button.click()
        # sleep(5)
        # self.facebook_login()
        # sleep(6)
        # try:
        #     allow_location_button = self.driver.find_element('xpath', '//*[@id="t-1917074667"]/main/div/div/div/div[3]/button[1]')
        #     allow_location_button.click()
        # except:
        #     print('no location popup')
        #
        # try:
        #     notifications_button = self.driver.find_element('xpath', '/html/body/div[2]/main/div/div/div/div[3]/button[2]')
        #     notifications_button.click()
        # except:
        #     print('no notification popup')
    
    def facebook_login(self):
        # find and click FB login button
        login_with_facebook = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Log in with Facebook")]')))
        login_with_facebook.click()

        # save references to main and FB windows
        sleep(8)
        base_window = self.driver.window_handles[0]
        fb_popup_window = self.driver.window_handles[1]
        # switch to FB window
        self.driver.switch_to.window(fb_popup_window)

        try:
            cookies_accept_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Accept Cookies")]')))
            cookies_accept_button.click()
        except:
            print('no cookies')
        sleep(10)
        email_field = self.driver.find_element(By.NAME, 'email')
        pw_field = self.driver.find_element(By.NAME, 'pass')
        login_button = self.driver.find_element(By.NAME, 'login')
        email_field.send_keys(email)
        pw_field.send_keys(password)
        login_button.click()
        self.driver.switch_to.window(base_window)
        try:
            allow_location_button_again = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Allow")]')))
            allow_location_button_again.click()
        except:
            print('no location popup')
        try:
            enable_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Enable")]')))
            enable_button.click()
        except:
            print('no location enable')

    def right_swipe(self):
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.ARROW_RIGHT)
    def left_swipe(self):
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.ARROW_LEFT)

    def auto_swipe(self):
        while True:
            sleep(2)
            try:
                self.right_swipe()
            except:
                self.close_match()

    def close_match(self):
        match_popup = self.driver.find_element('xpath', '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        match_popup.click()
    
    def get_matches(self):
        match_profiles = self.driver.find_elements('class name', 'matchListItem')
        print(str(match_profiles))
        message_links = []
        for profile in match_profiles:
            if profile.get_attribute('href') == 'https://tinder.com/app/my-likes' or profile.get_attribute('href') == 'https://tinder.com/app/likes-you':
                continue
            match_name = profile.find_element(By.CLASS_NAME, 'Ell')
            name = match_name.text
            print("got matches")
            print(name)
            message_links.append((name, profile.get_attribute('href')))
        return message_links

    def send_messages_to_matches(self):
        links = self.get_matches()
        for name, link in links:
            self.send_message(name, link)

    def send_message(self, name, link):
        self.driver.get(link)
        sleep(5)
        text_area = self.driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/form/textarea')
        print("sending message")
        message = generate_intro(generate_tinder_message(), name)
        text_area.send_keys(message)
        sleep(10)
        # text_area.send_keys(Keys.ENTER)

bot = TinderBot()
bot.open_tinder()
sleep(10)
# bot.auto_swipe()
# bot.send_messages_to_matches()