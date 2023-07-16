
import telebot
import firebase_admin
from firebase_admin import credentials, db, firestore
import datetime
import pytz
import telegram
import requests
from PIL import Image, ImageDraw, ImageFont

cred = credentials.Certificate('birthday-buddy-file(GET IT FROM FIREBASE.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxx GET IT FROM FIREBASE"
})

api = "TELEGRAM BOT API"
bot = telebot.TeleBot(api)
chat_id=-879235 #for logger bot

ref = db.reference('birthdays').get()

# -------------Wisher------------------------------

def send_birthday_wishes(bot, db):

    try:
        # Get the current date in UTC time zone
        current_date = datetime.datetime.now(pytz.utc).strftime('%m-%d')
        current_year = int(datetime.datetime.now(pytz.utc).strftime('%Y')) #Include age in Wish CONGRATS 
        for i in ref.keys():
            i=str(i)
            dob=i[5:]
            doy=int(i[:4])
            if dob==current_date:
                print("HAPPPPPPPY BIIIIIRTHDAYYY!!,It worked")
                print("Name:",list(ref[i].keys())[0],"CHAT ID- ",list(ref[i].values())[0]["ID"])
                message = f"Happy Birthday, {list(ref[i].keys())[0]} you turned {current_year-doy} Years old! 🎉🎂🎈"
                user_chat_id=list(ref[i].values())[0]["ID"]
                # print(user_chat_id)

                #sending Dynamic picture
                image = Image.open('HappyBirthday.png')
                d = ImageDraw.Draw(image)
                font = ImageFont.truetype('Cookie-Regular.ttf', size=60)
                # (x, y) = (390, 525)
                name = list(ref[i].keys())[0]
                # color = 'rgb(0,0,0)' 
                # draw.text((x, y), name, fill=color, font=font)
                W, H = image.size
                w, h = d.textsize(name, font=font)
                print(w, h)
                d.text(((((W-w)/2), ((H - h)/2 +20))),name, fill=(178,34,155), font=font)
                image.save('greeting_card.png')

                # bot.send_photo(user_chat_id, photo='greeting_card.png')
                bot.send_photo(chat_id=user_chat_id,
                               photo=open('greeting_card.png', 'rb'),
                               caption="Here's your Greeting Card!")

                bot.send_message(user_chat_id,message)
            else:
                continue

    except ValueError:
        print("SOMETHING GONE!!")               
        print(ValueError)
        bot.reply_to(message,'Sorry for inconvinence, Something went Wrong at our end!' )



send_birthday_wishes(bot, db)

