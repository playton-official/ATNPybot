#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, time, sqlite3, telepot, threading
from telepot.namedtuple import *
from bs4 import *


#powered by @playtonprojects, created by playton.
#put the token (replace TOKEN with bot's token.), install modules and start the bot.  


def get_groups(update):

    try:
        conn = sqlite3.connect("altenen.db")
        cursor = conn.cursor()
        conn.execute("create table if not exists chats(cid varchar(200))")
    except Exception as error:
        print("There is an error: "+str(error))

    query = "select * from chats where cid like "+str(update['chat']['id'])
    if(update['chat']['type'] != "private"):

        try:
            if(update['new_chat_participant'] and cursor.execute(query).fetchone() is None):
                    inline = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Powered by @playtonprojects",url="https://t.me/playtonprojects")]])
                    telepot.Bot("").sendMessage(update['chat']['id'],"🔆<b>Grazie per avermi aggiunto!</b>\nMi sono configurato e sintonizzato\ncon il tuo gruppo, d'ora in poi...\nriceverai cc da altenen automaticamente.",
                                                                                             parse_mode="HTML",
                                                                                             reply_markup=inline)
                    cursor.execute("insert into chats(cid) values ('"+str(update['chat']['id'])+"')")
                    conn.commit()
                    print("<-> Supergroup added: "+str(update['chat']['id']))
        except:
                pass
    else:
        if(update['text']=="/start"):
            inline = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Add me to a group!",url="https://telegram.me/altenenofficialbot?startgroup=foo")]])
            telepot.Bot("TOKEN").sendMessage(update["chat"]["id"],"❤<b>Grazie per avermi avviato!</b>🔆\nAggiungimi ad un gruppo, per\nricevere le cc in tempo reale!\n\n💡Powered by @playtonprojects!",
                                                                                     parse_mode="HTML",
                                                                                     reply_markup=inline)



def main():


    #function 1 - get cookie_bpc
    response_altenen = requests.get("http://www.altenen.com/").text
    print("<-> Starting to parsing cookies...")
    varc = response_altenen.split("\");document.")[0].split("c=toNumbers(\"")[1]
    response_cryptomathic = requests.get("http://extranet.cryptomathic.com/aescalc/index?key=deadbeefdeadbeefdeadbeefdeadbeef&iv=00000000000000000000000000000000&input=deadbeefdeadbeefdeadbeefdeadbeef"+str(varc)+"&mode=cbc&action=Decrypt&output=").text
    soup_parser = BeautifulSoup(response_cryptomathic,"html.parser")
    bpc_token = soup_parser.find('textarea',{'id':'output'}).text.lower()[32:]
    print("<-> Cookie BPC resolved: "+str(bpc_token))
    COOKIES = dict(bbpassword="9158824a73ec1f0cbd571ab0175ebbbf; ",bblastactivity="0; ",bblastvisit="1496414647; ",bbsessionhash="550275967d810ed0c20b08db8b163d0c; ",bbuserid="777101; ",_ddg_="70095 ",bpc=bpc_token)


    #function 2 - get last_thread
    response_altenen = requests.get("http://altenen.com/forumdisplay.php?f=41",cookies=COOKIES).text
    print("<-> Starting to parsing thread...")
    soup_parser = BeautifulSoup(response_altenen,"html.parser")
    LAST_THREAD = int(soup_parser.find('td', {'class': 'unread'}).get('id').replace('td_threadtitle_', ''))
    print("<-> Thread taken: "+str(LAST_THREAD))

    try:
        conn = sqlite3.connect("altenen.db")
        cursor = conn.cursor()
        conn.execute("create table if not exists chats(cid varchar(200))")
    except Exception as error:
        print("There is an error: "+str(error))

    import time
    #importants variables
    thread = LAST_THREAD
    bot = telepot.Bot("TOKEN")   #put the token

    #function 3 - get credit_cards     
    while(1):

			
			time = time.time()
            response_altenen=requests.get("http://altenen.com/showthread.php?t="+str(thread),cookies=COOKIES).text
            soup_parser=BeautifulSoup(response_altenen,"html.parser")
            #control posts
            
            if "No Thread specified." in response_altenen:
                print("<"+str(time)+"|"+str(thread)+"> Here, there isn't cc.")
                pass
            elif ", you do not have permission to access this page." in response_altenen:
                thread += 1
                print("<"+str(time)+"|"+str(thread)+"> Here, there isn't cc.")
                pass
            elif "Invalid Thread specified." in response_altenen:
                thread += 1
                pass
            elif "<font color=\"#FFFFFF\">ATN Police</font>" in response_altenen:
                thread += 1
                print("<"+str(time)+"|"+str(thread)+"> Here, there isn't cc.")
                pass
            elif "<strong>Infraction" in response_altenen:
                thread += 1
                print("<"+str(time)+"|"+str(thread)+"> Here, there isn't cc.")
                pass
            else:

                #parsing
                print("<"+str(time)+"|"+str(thread)+"> I used this thread.")
                title = soup_parser.find('title').text.encode('utf-8')
                cc = soup_parser.find('div', {'class': 'vb_postbit'}).text.replace("\r\n\r\n","").encode('utf-8')
                username = soup_parser.find('a', {'class': 'bigusername'}).font.text.encode('utf-8')
                message = "🔆New <b>post</b> from <a href='http://altenen.com'>altenen</a>.\n\n👤Username: <i>"+str(username)+"</i>\n✏Title: <i>"+str(title)+"</i>\n📝Post:\n"+str(cc)+"\n\n💡Powered by @playtonprojects"
                query = "select * from chats"
                inline = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Add me to a group!",url="https://telegram.me/altenenofficialbot?startgroup=foo")]])

        

                for x in cursor.execute(query).fetchall():
                    try:
                        bot.sendMessage(x[0],message,parse_mode="HTML",reply_markup=inline)
                    except Exception as error:
                        print("<!> Exception:  "+str(error))
                        cursor.execute("delete from chats where cid like "+str(x[0]))
                        conn.commit()
                        pass
                thread += 1
    





if __name__=='__main__':
    telepot.Bot("TOKEN").message_loop({'chat':get_groups})
    try:
		threading.Thread(target=main()).start()
		while(True):
			pass
    except:
		pass



		
