# -*- coding: utf-8 -*-

import telebot
import cv2 
import numpy as np 
import urllib.request 
 
def auto_canny(image, sigma=0.4):
  v = np.median(image)
  lower = int(max(0, (1.0 - sigma) * v))
  upper = int(min(255, (1.0 + sigma) * v))
  edged = cv2.Canny(image, upper, lower, 3)
  return edged

def contours(photo):
    image = cv2.imread(photo)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    auto = auto_canny(blurred)
    contours, hierarchy = cv2.findContours(auto,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    img = np.full((image.shape[0], image.shape[1], 3), 255, dtype=np.uint8) # create white image
    cv2.drawContours(img, contours, -1, (0, 0, 0), 3) 
    cv2.imwrite('image.jpg', img) 

    return open('image.jpg','rb')

token = "789374632:AAGxi99fQZaOrYdFbD8JZyisGLQcbbn7CL0"
bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def welcome_start(message):
    bot.send_message(message.chat.id, 'Привет. Отправь мне фотографию автомобиля и я обработаю ее.\nДля ознакомления напиши /help')

@bot.message_handler(commands=['help'])
def welcome_help(message):
    bot.send_message(message.chat.id, '1.Загрузи и отправь фотографию автомобиля. \n2.Получи раскраску на основе отправленной фотографии.')

@bot.message_handler(content_types=["text"])
def content_text(message):
    bot.send_message(message.chat.id, 'Я работаю только с фото.')
 
@bot.message_handler(content_types=["photo"])
def handle_docs_photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("test.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_photo(message.chat.id, contours('test.jpg'))

bot.polling()