import telebot
import firebase_admin
from firebase_admin import credentials, db
import datetime

cred = credentials.Certificate('birthday-buddy-file(YOUR CREDENTIALS FILE).json')
firebase_admin.initialize_app(cred, {
    'databaseURL': "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx(Get it from firebase)"
})

api = "TELEGRAM BOT API"
bot = telebot.TeleBot(api)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f'''Hello! {message.from_user.first_name} {message.from_user.last_name}, how may I help you?\n\nUse /help command to see list of commands''')

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, f"""" {message.from_user.first_name},You can use any command in described format!\n
    1./start => To start the bot
    2./help => Get help for Commands
    3./setbirthday => To save the birthday 
    4./updatebirthday => To update already existing birthday
    5./deletebirthday => To delete a birthday""")


ref = db.reference('birthdays')
# -----------------------------------setting--------------
@bot.message_handler(commands=['setbirthday'])
def set_birthday(message):
    user = message.from_user.username
    Id = message.chat.id
    # birthday = message.text[len('/setbirthday'):].strip()
    # buddyname=birthday[:birthday.index('-')].rstrip()
    # # Validate the birthday format
    # print(buddyname)
    try:
        birthday = message.text[len('/setbirthday'):].strip()
        buddyname=birthday[:birthday.index('-')]
        
        # Validate the birthday format
        print(buddyname)
        # Convert the birthday to a datetime object
        birthday = birthday[birthday.index('-')+1:]
        
        birthday_dt = datetime.datetime.strptime(birthday, '%d/%m/%Y')
        birthday_dt = str(birthday_dt)[:10]
        # Write the user's birthday to the database
        ref.child(birthday_dt).child(buddyname).set({'User': user,'ID':Id})
        bot.reply_to(message,'Birthday saved successfully!' )
        
    except ValueError:
        print(ValueError)
        bot.reply_to(message,'Invalid birthday format. Please use the format Name-DD/MM/YYYY' )
        bot.send_message(message.chat.id,'Try something like\n"Ikram-03/12/2002"(Name"-"DD/MM/YYYY)' )
    


# ------------------------updation-------------

@bot.message_handler(commands=['updatebirthday'])
def update_birthday(message):
    user_id = message.from_user.username
    Id = message.chat.id
    # birthday = message.text[len('/updatebirthday'):].strip()
    # buddyname=birthday[:birthday.index('-')]
    # # Validate the birthday format
    # print(buddyname)
    try:
        birthday = message.text[len('/updatebirthday'):].strip()
        buddyname=birthday[:birthday.index('-')]
        # Validate the birthday format
        print(buddyname)
        # Convert the birthday to a datetime object
        birthday = birthday[birthday.index('-')+1:]
        birthday_dt = datetime.datetime.strptime(birthday, '%d/%m/%Y')
        birthday_dt = str(birthday_dt)[:10]
        # Write the user's birthday to the database
        ref.child(birthday_dt).child(buddyname).set({'User': user_id,'ID':Id})
        bot.reply_to(message,f'Birthday Updated successfully!\n\n{buddyname} Birthday on {birthday_dt}' )
        
    except ValueError:
        print(ValueError)
        bot.reply_to(message,'Invalid birthday format. Please use the format Name-DD/MM/YYYY' )


# ------------------------deletion-------------

@bot.message_handler(commands=['deletebirthday'])
def update_birthday(message):
    user_id = message.from_user.username
    Id = message.chat.id
    # birthday = message.text[len('/deletebirthday'):].strip()
    # buddyname=birthday[:birthday.index('-')]
    # # Validate the birthday format
    # print(buddyname)
    try:
        birthday = message.text[len('/deletebirthday'):].strip()
        buddyname=birthday[:birthday.index('-')]
        # Validate the birthday format
        print(buddyname)
        # Convert the birthday to a datetime object
        birthday = birthday[birthday.index('-')+1:]
        birthday_dt = datetime.datetime.strptime(birthday, '%d/%m/%Y')
        birthday_dt = str(birthday_dt)[:10]
        # Delete the user's birthday from the database
        # ref.child(user_id).child(buddyname).delete({'birthday': birthday_dt})       
        ref.child(birthday_dt).child(buddyname).delete()
        bot.reply_to(message,f'Birthday Deleted successfully!\n\n{buddyname}-{birthday_dt}' )
        
    except ValueError:
        print(ValueError)
        bot.reply_to(message,'Invalid Date or Name,It Doesnt exists to delete' )





bot.polling()



