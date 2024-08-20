import re
import os
import time
import random
import requests
import telebot
import sys
from telebot.types import ReactionTypeEmoji
from g4f.client import Client
from g4f.cookies import set_cookies
from g4f.Provider import BingCreateImages, OpenaiChat, Gemini
from telethon import TelegramClient
from langdetect import detect


file_path = os.path.dirname(os.path.realpath(__file__))

with open(file_path + '/settings', 'r') as f:
    data = []
    for line in f:
        s = line.strip()
        string = re.search(r' = (.*?) #', s).group(1)
        data.append(string)
f.close()

API_ID = data[0]
API_HASH = data[1]
token = data[2]
botname = data[3]
chat_id = data[4]
language = data[5]
rate_messages = float(data[6])
rate_emojis = float(data[7])
emojis = data[8].split(', ')
Name = data[9]
print("Name:", Name)
print("Botname:", botname[1:])

client0 = TelegramClient('my-client', API_ID, API_HASH)
client = Client()
bot = telebot.TeleBot(token)

if chat_id == 'default':
    url = 'https://api.telegram.org/bot'+token+'/getUpdates'
    status = 0
    while status == 0:
        try:
            resp = requests.get(url).json()
            status = 1
        except Exception as e:
            print('telegram api timeout..')
            sys.exit(0)
            time.sleep(15)
    
    print('resp: ', resp['result'])
    if len(resp['result']) > 0:
        print('Update: ', resp['result'][0])
        if 'message' in resp['result'][0]:
            chat_id = resp['result'][0]['message']['chat']['id']
            #print('Group: ', resp['result'][0]['message']['chat']['title'])
        else:
            print(resp['result'][0])
            if 'edited_message' in resp['result'][0]:
                chat_id = resp['result'][0]['edited_message']['chat']['id']
            else:
                chat_id = resp['result'][0]['my_chat_member']['chat']['id']
            print(chat_id)

async def last_bot_id():
    url = f'https://api.telegram.org/bot{token}/getUpdates?offset=-1'
    status = 0
    while status == 0:
        try:
            resp = requests.get(url).json()
            status = 1
            print(resp)
        except Exception as e:
            print('telegram api timeout..')
            sys.exit(0)
            time.sleep(15)
    if len(resp['result']) > 0:
        if 'message' in resp['result'][0]:
            print(resp['result'][0]['message']['from'])
            if 'username' in resp['result'][0]['message']['from']:
                user = resp['result'][0]['message']['from']['username']
            else:
                user = ''
            last_bot_id = resp['result'][0]['message']['message_id']
            if 'text' in resp['result'][0]['message']:
                text = resp['result'][0]['message']['text']
            else:
                text = ''
        else:
            print(resp['result'][0])
            if 'edited_message' in resp['result'][0]:
                user = resp['result'][0]['edited_message']['from']['username']
                last_bot_id = resp['result'][0]['edited_message']['message_id']  	
                text = resp['result'][0]['edited_message']['text']	
            else:		 
                print(resp['result'][0])
                if 'message' in resp['result'][0]:
                    if 'username' in resp['result'][0]['message']['from']:
                        user = resp['result'][0]['my_chat_member']['from']['username']
                    else:
                        user = ''
                else:
                    user = ''
                last_bot_id = ''
                text = ''

        print(last_bot_id)
    else:
        last_bot_id =''
        user = ''
        text = ''
        print('If you just created a new bot:')
        print('1. Be shure privacy mode of your bot is disabled.')
        print('2. Add your bot to the group.')
        print('3. Contact him in the group via @yourbotname <any text>.')
        print('4. restart the script.')
        await client0.disconnect()  
        await client.disconnect()    
    return last_bot_id, user, text

async def last_message_id():
    emo_ids = 0
    index = 0
    reply = 0
    first = 10

    try:
        with open(file_path + '/.last_answer_id', 'r') as f:
            data = []
            for line in f:
                s = line.strip()
                data.append(s)
            if str(data[1]) == str(chat_id):
                last_answer_id = int(data[0]) 
            else:
                last_answer_id = 0
        f.close() 
    except:
        with open(file_path + '/.last_answer_id', 'w') as f:
            f.write('0')  
            f.write('\n')
            f.write('0')
            last_answer_id = 0
        f.close() 

    if last_answer_id == '':
        last_answer_id = 0

    print('Last_answer_id: ', last_answer_id)
    id2, user, text = await last_bot_id()
    print(chat_id)
    last_id = ''
    last_message = ''
    async for message in client0.iter_messages(chat_id, limit=10):
        if text == message.text:
            last_id = message.id
            last_message = message.text

        sender = await message.get_sender()
        print(sender.username)

        #print('Text: ', text)
        #print(message)
        print('Last_answer_id: ', last_answer_id)
        print('message:', message.post)
        print('action:', message.action)
        if message.pinned == True:
            print('pinned:', message.pinned)
        if (message.action is None)&(message.pinned == False):
            if (message.id > last_answer_id)&(botname in message.text):
                reply = 1
                first = message.id
            if (str(user) != str(botname[1:])):
                emo_ids = 1

        print('message_id: ', message.id)
        print('first: ', first)
        
        index += 1
        print(message)

    return last_id, last_message, emo_ids, reply, first, last_answer_id, id2

async def chat_gpt_text(prompt, prompt_messages):
    prompt_messages.append({ 'role': 'user', 'content': prompt })
    print(prompt_messages)
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=prompt_messages
    )

    return response

async def messages(first, last_answer_id, language, prompt_messages):
    if language == 'ru':
        pr = Name + ', представь, что ты человек, прочитавший следующие сообщения из чата. Сгенеририруй короткий оригинальный комментарий на русском языке на эти сообщения, который должен начинаться с символов *!* и заканчиваться на *!*. Сообщения из этого чата: '
    
    if language == 'en':
        pr = Name + ', imagine that you are a person reading the following chat messages. Generate a short original comment in English for these messages, which should begin with the characters *!* and end with *!*. Messages from this chat:'
    ind = 1
    id2, user, text = await last_bot_id()
    message_id = ''
    last_id = ''
    async for message in client0.iter_messages(chat_id, limit=10):
        if text == message.text:
            message_id = message.id
            last_id = message_id
    add = 0
    delta = 0
    id_s = []
    async for message in client0.iter_messages(chat_id, limit=10):
        if text == message.text:
    	    add = 1
        sender = await message.get_sender()
        if (add == 1)&(message.id not in id_s):
    	    delta += 1
    	    id_s.append(message.id)
        if (message.pinned == False)&(message.action is None)&(str(sender.username) != str(botname[1:])):
            if (botname in message.text)&(message.id > last_answer_id)&(message.id == first):
                print('Promt: ', message.text)
                s = message.text
                sub = s.replace(botname, '')
                if language == 'ru':
                    pr = Name + ', сгенеририруй ответ на русском языке. ' + sub 
                if language == 'en':
            	    pr = Name + ', generate an answer in English. ' + sub
                message_id = message.id
                break
            print('sender:', sender.username)
            if str(sender.username) != str(botname[1:]):
                string = message.text.rstrip()
                pr = pr + str(ind)+'. ' + string + ' '
        ind+=1
    # response to chat gpt
    resp = await chat_gpt_text(pr, prompt_messages)
    print(resp.choices[0].message.content)

    return resp.choices[0].message.content, message_id, id2, last_id, delta


async def main():
    file_path = os.path.dirname(os.path.realpath(__file__))
    prompt_messages = []
    try:
        with open(file_path + '/.context', 'r') as f:
            data = []
            for line in f:
                s = line.strip()
                if 'user:' in s:
                    text = s.split('user:')
                    #print(text[1])
                    prompt_messages.append({'role': 'user', 'content': text[1]})
                if 'assistant:' in s:
                    text = s.split('assistant:')
                    #print(text[1])
                    prompt_messages.append({'role': 'assistant', 'content': text[1]})
        f.close()
    except:
        with open(file_path + '/.context', 'w') as f:
            f.write('')
        f.close() 
    async with client0:
        last_id, last_message, emo_ids, reply, first, last_answer_id, id2 = await last_message_id()
        current_id = last_id
        rus_lang = 1
        time.sleep(10)
        reply = 0
        while last_id == current_id:
            time.sleep(75)
            current_id, last_message, emo_ids, reply, first, last_answer_id, id2 = await last_message_id()
            if reply == 1:
                break
            if last_id != current_id:
                if random.uniform(0, 1) < rate_emojis:
                    emo = random.choice(emojis)
                    if (emo_ids == 1)&(id2 != ''):
                        message_id = id2
                        print('message_id: ', message_id)
                        status = 0
                        while status == 0:
                            try:
                                bot.set_message_reaction(chat_id, message_id, [ReactionTypeEmoji(emo)], is_big=False)
                                status = 1
                            except Exception as e:
                                print('reaction timeout..')
                                sys.exit(0)
                                time.sleep(15)
                
                if random.uniform(0, 1) > rate_messages:
                    last_id = current_id
            print('current_id:', current_id)
            print('last_id:', last_id)

        words_lang = 0
        other_lang = 1
        lang = ''
        answer = ''
        while (words_lang == 0)|(lang != language)|(answer == '')|(other_lang == 1)|('Извините' in answer)|('извините' in answer)|('Sorry' in answer)|('sorry' in answer):
            for k in range(0, 15):
                bot.send_chat_action(chat_id, 'typing')
                time.sleep(5)
            resp, mes_id, id2, current_id, delta = await messages(first, last_answer_id, language, prompt_messages)
            delete = 0
            if current_id == '':
                delete = 1
                break
            if language == 'ru':
                words_lang = bool(re.search('[а-яА-Я]', resp))
                other_lang = bool(re.search('[\u4e00-\u9fff]', resp))
            if language == 'en':
                words_lang = bool(re.search('[a-zA-Z]', resp))
                other_lang = bool(re.search('[\u4e00-\u9fff]', resp))
            lang = detect(resp)
            print(lang)
            if reply == 0:
                result = resp.strip().split('*!*')
                if len(result) >= 2:
                    answer = result[1].strip()
                else:
                    answer = ''
            else:
                print('resp', resp)
                answer = resp.strip()
        print('reply', reply)
        answer = answer.replace('*!', '')
        answer = answer.replace('!*', '')
        answer = answer.replace('*!*', '')
        answer = answer.replace('*', '')
        answer = answer.replace('#', '')
        print('last answer:', answer)
        strings = answer.split('\n')
        new_strings = [x for x in strings if x != '']
        answer = '\n'.join(new_strings)
        print('new answer: ', answer)
        print('current_id', current_id)
        print('mes id', mes_id)
        print('id2:', id2)
        print(delta)
        
        if delete == 0:
            bot.send_chat_action(chat_id, 'typing')
            if (reply == 1)&(id2 != ''):
                message_id = id2 - delta + 1
                status = 0
                while status == 0:
                    try:
                        url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={answer}&reply_to_message_id={message_id}'
                        print(requests.get(url).json())
                        status = 1
                    except:
                        sys.exit(0)
                with open(file_path + '/.last_answer_id', 'w') as f:
                   f.write(str(mes_id)) 
                   f.write('\n')   
                   f.write(str(chat_id))
                f.close() 

            else:
                status = 0
                while status == 0:
                    try:
                        url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={answer}'
                        print(requests.get(url).json())
                        status = 1
                    except:
                        sys.exit(0)
            answer = answer.replace('\n', ' ')
            prompt_messages.append({ 'role': 'assistant', 'content': answer })
            prompt_messages = prompt_messages[-20:]
            print(prompt_messages)
            with open(file_path + '/.context', 'w') as f:
                for m in prompt_messages:
                    print(m['role'], m['content'])
                    f.write(str(m['role']) + ': ' + str(m['content'])) 
                    f.write('\n')   
            f.close() 
        print('End')

while True:
    client0.loop.run_until_complete(main())
