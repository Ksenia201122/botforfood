import telebot
import json
token="7765062409:AAFHxtXKFjVAP_4AJMiQaMLU62aO9EAxRrk"
bot=telebot.TeleBot(token)

menu_items = [
        {"name": "Грибной суп", "price": "450 руб.", "photo": "mushroom_soup.png"},
        {"name": "Салат Цезарь", "price": "550 руб.", "photo": "caesar.png"},
        {"name": "Утка с апельсинами", "price": "700 руб.", "photo": "duck_orange.png"},
        {"name": "Бефстроганов", "price": "650 руб.", "photo": "stroganoff.png"},
        {"name": "Ризотто", "price": "500 руб.", "photo": "risotto.png"},
        {"name": "Тирамису", "price": "400 руб.", "photo": "tiramisu.png"},
        {"name": "Блины", "price": "300 руб.", "photo": "pancakes.png"},
        {"name": "Паста Карбонара", "price": "550 руб.", "photo": "carbonara.png"},
        {"name": "Гаспачо", "price": "350 руб.", "photo": "gazpacho.png"},
        {"name": "Фалафель", "price": "400 руб.", "photo": "falafel.png"}

]


@bot.message_handler(["start"])
def handle_start(message):
    cnopc=cnopci()
    bot.send_message(message.chat.id,"привет",reply_markup=cnopc)


def cnopci():
    naborcnopoc=telebot.types.ReplyKeyboardMarkup()
    cnopcamenu=telebot.types.KeyboardButton("меню")
    cnopcacorz=telebot.types.KeyboardButton("корзина")
    cnopcaoformzacaz=telebot.types.KeyboardButton("оформить заказ")
    naborcnopoc.add(cnopcamenu)
    naborcnopoc.add(cnopcacorz)
    naborcnopoc.add(cnopcaoformzacaz)
    return naborcnopoc


def funcia(message):
    return True

def cena(nazvanie):
    for eda in menu_items:
        if eda["name"]==nazvanie:
            return eda["price"]

def dlajson(id,nazvanie,cena,colvo):
    fayl=open("file.json","r",encoding="UTF-8")
    slovar=json.load(fayl)
    if id not in slovar:
        slovar[id]={"номер":"","имя":"","адрес":"","корзина":{nazvanie:[cena,colvo]}}
    else:
        slovarnfo=slovar[id]
        corzina=slovarnfo["корзина"]
        if nazvanie in corzina:
            spisoc=corzina[nazvanie]
            spisoc[1]=spisoc[1]+colvo
        else:
            corzina[nazvanie]=[cena,colvo]
    fayl.close()
    fayl=open("file.json","w",encoding="UTF-8")
    json.dump(slovar,fayl,ensure_ascii=False,indent=4)
    fayl.close()
    
def corzina(id):
    fayl=open("file.json","r",encoding="UTF-8")
    slovar=json.load(fayl)
    slovarpols=slovar[id]
    slovcorzina=slovarpols["корзина"]
    nabor=telebot.types.InlineKeyboardMarkup()
    for bludo in slovcorzina:
        spisoc=slovcorzina[bludo]
        cnopcaedi=telebot.types.InlineKeyboardButton(bludo+" "+str(spisoc[1]),callback_data="bludocorz")
        cnopcaplus=telebot.types.InlineKeyboardButton("+",callback_data="plus*"+bludo)
        cnopcaminus=telebot.types.InlineKeyboardButton("-",callback_data="minus*"+bludo)
        nabor.add(cnopcaminus,cnopcaedi,cnopcaplus)
    fayl.close()
    return nabor
@bot.callback_query_handler(func=funcia)
def handle_obrabotcacnop(clic):
    spisocrazdel=clic.data.split("*")
    if spisocrazdel[0]=="eda":
        dlajson(str(clic.message.chat.id),spisocrazdel[1],cena(spisocrazdel[1]),1)
    if spisocrazdel[0]=="vpravo":
        stranica=int(spisocrazdel[1])
        generator=geneeeratorcnop(stranica+1)
        bot.send_message(clic.message.chat.id,"меню",reply_markup=generator)
    elif spisocrazdel[0]=="vlevo":
        nomerstr=int(spisocrazdel[1])
        generator=geneeeratorcnop(nomerstr-1)
        bot.send_message(clic.message.chat.id,"меню",reply_markup=generator)
    if spisocrazdel[0]=="plus":
        dlajson(str(clic.message.chat.id),spisocrazdel[1],0,1)
        cnopca=corzina(str(clic.message.chat.id))
        bot.edit_message_text("корзина",clic.message.chat.id,clic.message.message_id,reply_markup=cnopca)
    if spisocrazdel[0]=="minus":
        dlajson(str(clic.message.chat.id),spisocrazdel[1],0,-1)
        cnopca=corzina(str(clic.message.chat.id))
        bot.edit_message_text("корзина",clic.message.chat.id,clic.message.message_id,reply_markup=cnopca)
    if spisocrazdel[0]=="otmenit":
        bot.send_message(clic.message.chat.id,"корзина:",reply_markup=corzina(str(clic.message.chat.id)))
    if spisocrazdel[0]=="podtverdit":
        bot.send_message(clic.message.chat.id,"Введите Ваше имя")
        bot.register_next_step_handler_by_chat_id(clic.message.chat.id,ima)

def ima(message):
    fayl=open("file.json","r",encoding="UTF-8")
    slovar=json.load(fayl)
    slovarpols=slovar[str(message.chat.id)]
    slovarpols["имя"]=message.text
    fayl.close()
    fayl=open("file.json","w",encoding="UTF-8")
    json.dump(slovar,fayl,ensure_ascii=False,indent=4)
    fayl.close()
    bot.send_message(message.chat.id,"Введите Ваш номер телефона")
    bot.register_next_step_handler_by_chat_id(message.chat.id,telephone)

def telephone(message):
    fayl=open("file.json","r",encoding="UTF-8")
    slovar=json.load(fayl)
    slovarpols=slovar[str(message.chat.id)]
    slovarpols["номер"]=message.text
    fayl.close()
    fayl=open("file.json","w",encoding="UTF-8")
    json.dump(slovar,fayl,ensure_ascii=False,indent=4)
    fayl.close()
    bot.send_message(message.chat.id,"Введите Ваш адрес")
    bot.register_next_step_handler_by_chat_id(message.chat.id,adrec)

def adrec(message):
    fayl=open("file.json","r",encoding="UTF-8")
    slovar=json.load(fayl)
    slovarpols=slovar[str(message.chat.id)]
    slovarpols["адрес"]=message.text
    fayl.close()
    fayl=open("file.json","w",encoding="UTF-8")
    json.dump(slovar,fayl,ensure_ascii=False,indent=4)
    fayl.close()
    bot.send_message(message.chat.id,"Заказ успешно оформлен и собирается")






def geneeeratorcnop(nomerstr):
    nabor=telebot.types.InlineKeyboardMarkup()
    start=nomerstr*4
    end=start+4
    for slovar in menu_items[start:end]:
        nazvanie=slovar["name"]
        cnopcaedi=telebot.types.InlineKeyboardButton(nazvanie,callback_data="eda*"+nazvanie)
        nabor.add(cnopcaedi)
    cnopcavlevo=telebot.types.InlineKeyboardButton("влево",callback_data="vlevo*"+str(nomerstr))
    cnopcavpravo=telebot.types.InlineKeyboardButton("вправо",callback_data="vpravo*"+str(nomerstr))
    if nomerstr>0 and nomerstr<len(menu_items)//4:
        nabor.add(cnopcavlevo,cnopcavpravo)
    elif nomerstr==0:
        nabor.add(cnopcavpravo)
    else:
        nabor.add(cnopcavlevo)
    return nabor
def cnopca():
    nabor=telebot.types.InlineKeyboardMarkup()
    cnopcapodtv=telebot.types.InlineKeyboardButton("подтвердить",callback_data="podtverdit")
    cnopcaotmen=telebot.types.InlineKeyboardButton("отменить",callback_data="otmenit")
    nabor.add(cnopcapodtv,cnopcaotmen)
    return nabor
def oformzacaz(message):
    fayl=open("file.json","r",encoding="UTF-8")
    slovar=json.load(fayl)
    slovarpols=slovar[str(message.chat.id)]
    slovcorzina=slovarpols["корзина"]
    a=""
    b=0
    for bludo in slovcorzina:
        spisoc=slovcorzina[bludo]
        spisoccena=spisoc[0].split(" ")
        obchcena=int(spisoccena[0])*spisoc[1]
        b=b+obchcena
        a=a+bludo+" "+str(spisoc[1])+"шт"+"*"+str(spisoc[0])+"="+str(obchcena)+"\n"
    a=a+"\n\nИтого:"+str(b)
    fayl.close()
    return a
@bot.message_handler(func=funcia)
def handlle_all(message):
    if message.text=="меню":
        cnop=geneeeratorcnop(1)
        bot.send_message(message.chat.id,"меню:",reply_markup=cnop)
    if message.text=="корзина":
        cnop=corzina(str(message.chat.id))
        bot.send_message(message.chat.id,"корзина",reply_markup=cnop)
    if message.text=="оформить заказ":
        z=oformzacaz(message)
        bot.send_message(message.chat.id,z,reply_markup=cnopca())



bot.polling()