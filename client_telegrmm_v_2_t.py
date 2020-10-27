
print ('[+] Старт программы телеграмм клиент')
print ('[+] Версия V 2.1')
import iz_func
import telebot

api_id       = XXXXXXXXXX
api_hash     = 'XXXXXXXXXXX'
phone_number = 'XXXXXXXXXXX'                      #Телефон клиента
print ('    [+] Пользователь:',phone_number) 
namebot     = "@ask_314_bot"                      #Бот который выдает информацию       

def send_message_bot (message_out,markup,catalog):
    import telebot  
    namebot = "@ask_314_bot" 
    token,about = iz_func.get_token (namebot)
    bot   = telebot.TeleBot(token)    
    bot.send_message(catalog,message_out,reply_markup = markup, parse_mode='HTML', disable_web_page_preview = True)   ##Отправляем сообщения из бота

def send_new_message (message,catalog,chat_title,chat_username,chat_id,find_w,sender_username):
    print ('[1]')
    message_out = ''
    message_out = message_out + '🤵 <b>Новое сообщение</b> от @' +str(sender_username) +'\n'
    message_out = message_out + '⭐ <i>'+str(find_w)+'</i>' + '\n'    
    message_out = message_out + '' + '\n'
    message_out = message_out + message + '\n'
    message_out = message_out + '' + '\n'
    message_out = message_out + 'Сообщение: https://t.me/'+chat_username +'/'+str(chat_id)+ '\n'
    message_out = message_out + 'Описание : ' +chat_title   + '\n'
    bot.send_message(catalog,message_out,parse_mode='HTML',disable_web_page_preview = True)   ## Информируем о новом

def load_key (namebot,user_id):
    list_key = []
    db,cursor = iz_func.connect (namebot)
    sql = "select id,key_name from tel_key where namebot = '{}' and user_id = '{}'".format(namebot,user_id);
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,key_name = row
        list_key.append(key_name)
    return list_key           ### Читаем ключевые слова для поиска. Хранятся в базе данных
  
def find_key (mess,list_key):
    find = ''
    label = 'не найден'
    for line in list_key:
        if mess.upper().find(line.upper()) != -1:
            label = 'найден'
            find = find + " " +line
            print ('        [+]',line)
    return label,find          ### Поиск в тексте ключевых слов 

def select_word (mess,word):
    mess = mess.replace(str(word),'<b>'+str(word)+'</b>')
    mess = '==>'+mess 
    return mess      ### Выделение жирным ключевого слова    
 
def list_send_grup (user_id):
    db,cursor = iz_func.connect (namebot)
    sql = "SELECT id,receiver_id,sender_id FROM tel_resend where user_id = "+str(user_id)+""    
    cursor.execute(sql)
    data = cursor.fetchall()
    list_grup = []
    for rec in data: 
        id,receiver_id,sender_id = rec
        list_grup.append([receiver_id,sender_id])
    return list_grup     ### Список групп которые читаем   

def get_user_send ():
    import time
    db,cursor   = iz_func.connect (namebot)
    timestamp = int(time.time())
    sql = "select DISTINCT user_id from secret_key where  user_id <> '' and begin_t  < "+str(timestamp)+" and end_t > "+str(timestamp)+" ORDER BY begin_t DESC "
    cursor.execute(sql)
    data = cursor.fetchall()
    list = []
    for rec in data: 
        user_id = rec[0]
        list.append(user_id)
    return list               ###  Список клиентов которые читают группу 

from telethon import TelegramClient, events
session = 'session_{}.load_catalog_№10'.format(phone_number)
client = TelegramClient(session,api_id=192804,api_hash=api_hash)
@client.on(events.NewMessage)
async def my_event_handler(event):
    message = event.message
    print ('[+]',message)              
    path = await client.download_media(message=message)
    print('File saved to', path)                                  # Скачиваем картинку если она есть.

    print ('[+] Сообщение:',event.id)    
    try:
        sender_id_user    = ''
        sender       = await event.get_sender()
        sender_id_user    = sender.id
    except Exception as e:    
        print ('    [+] error send message',e)   
        pass     
    try:
        sender_username = ''
        sender_username = sender.username                         #  Получаем информацию об отправители
    except Exception as e:    
        print ('    [+] error send message',e)     
        pass   
    try:
        sender_phone = ''   
        sender_phone = sender.phone 
    except Exception as e:    
        print ('    [+] error send message',e)        
        pass
    print ('    [+] sender id:',sender_id_user,', phone:',sender_phone,',username',sender_username)
    try:
        raw_text     = ''                                        # Тескст сообшения при необходимости
        raw_text     = event.raw_text
    except Exception as e:    
        print ('    [+] error send message',e)
        pass
    print ('    [+] text:',raw_text[0:120].replace('\n',''))
    try:
        chat         = ''                                        # Информация о чате если сообщение от туда
        chat_id      = ''
        chat_title   = ''
        chat_username = ''
        chat         = await event.get_chat ()
        chat_id      = event.chat_id
        chat_title   = chat.title
        chat_username = chat.username        
    except Exception as e:    
        print ('    [+] error send message',e)
        pass
    print ('    [+] chat   id:',chat_id,  ', title:',chat_title)

    message_out = ""                                                              ###  Формируем информацию о новом сообшении для бота
    message_out = message_out + '🙋 <b>Информация</b>'+'\n'
    message_out = message_out + '<b>Текст</b>'+'\n'
    message_out = message_out + str(raw_text)+'\n'    
    message_out = message_out + ''+'\n'
    message_out = message_out + '<b>Получатель</b>:'+'\n'
    message_out = message_out + '    https://t.me/Oksana121901'+'\n'
    message_out = message_out + '    Телефон: '+str(phone_number)+'\n'
    message_out = message_out + '    Имя: Оксана Борвинская'+'\n'    
    message_out = message_out + '<b>Отправитель</b>:'+'\n'
    message_out = message_out + '    ID:      '+str(sender_id_user)+''+'\n'
    message_out = message_out + '    Телефон: '+str(sender_phone)+''+'\n'
    message_out = message_out + '    Логин:   '+str(sender_username)+''+'\n'

    lastid = 0                                                                     ##  Записываем это сообшение в базу данных
    try:
        db,cursor = iz_func.connect (namebot)
        sql = "INSERT INTO get_message_ask (`sender_text`,`in_name`,`sender_name`,`sender_id`) VALUES ('{}','{}','{}','{}')".format ('',str(phone_number),str(sender_username),str(sender_id_user))
        cursor.execute(sql)
        db.commit() 
        lastid = cursor.lastrowid
    except Exception as e:    
        print ('    [+] error send message',e)

    try:                                                                           ##  Отправляем телеграмм боту
        from telebot import types 
        markup = types.InlineKeyboardMarkup(row_width=4)
        tx1    = 'Ответить'
        cl1    = 'Ответить_'+str(lastid)
        mn1    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)
        tx1    = 'Блокировать'
        cl1    = 'Блокировать_'+str(lastid)
        mn2    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)    
        markup.add(mn1,mn2) 
    except Exception as e:    
        print ('    [+] error send message',e)

    try:
        sql  = "select id,telefon,user_id from get_user_telefon where telefon = '"+str(phone_number)+"';"
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data:
            id,telefon,user_id = rec
            print ('    [+]',telefon,user_id)
            send_message_bot (message_out,markup,user_id)                          ## Отправляем это сообшение всем кто на него подпиан

    except Exception as e:    
        print ('    [+] error send message',e)



client.start()
client.run_until_disconnected()
