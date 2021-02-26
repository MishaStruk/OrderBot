import json
import urllib

import requests
import time
import  datetime

import Responses
import DatabaseMoudle
import Classes

NON_VALID_PASSWORDS = ("/start", "/help", "/order", "/password", "/myorders")
users_in_reg=[]
orders_in_progress = []


TOKEN = "<Enter BOT API KEY"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    """Function to send a text to a user by user id"""
    """param: text : string :The text to be sent"""
    """param: chat_id : int :The id of the user in telegram"""
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_last_update_id(updates):
    """Function to get the last unreasoned update id"""
    """param: updates : list of updates"""
    """:return: update : item :the json of the latest update"""
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_json_from_url(url):
    """Function to get json of a site"""
    """param: url : string :The site url"""
    """param: js : string :the json string"""
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    """Function to get the latest updates"""
    """param: offset : int :the offset of the desired updates"""
    """:return: js : json list :list of json as requested by offset"""
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    """Function to get the text and id of the user"""
    """param: updates : json lost:the list of updates"""
    """:return: text, chat_id : str,int :text and id of the user"""
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def get_user_id(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    user_id = updates["result"][last_update]["message"]["chat"]["id"]
    return user_id


def send_message(text, chat_id):
    """Function to send a text to a user by user id"""
    """param: text : string :The text to be sent"""
    """param: chat_id : int :The id of the user in telegram"""
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def start_chat(chat_id):
    """TODO: Make an start function documantaion"""
    """Start function when user start the bot by /start"""
    """param: chat_id : int :The user id in telegram"""
    DATABASE = DatabaseMoudle.userDatabase()
    str_id = str(chat_id)
    if(DATABASE.CheckIfUserIdExist(str_id)):
        send_message("You are registered,\nUse /order command to order\nYou can choose Pizza,"
                     "Falafel or a toast\nOr /help for more commands", chat_id)
    else:
        send_message("Please Register, Write your password twice", chat_id)
        new_user = Classes.user_in_registration(chat_id)
        users_in_reg.append(new_user)




def start_order(chat_id):
    """TODO: Make an strat order function documantaion"""
    """Start order for a user by /order"""
    """param: chat_id : int :The user id in telegram"""
    DATABASE = DatabaseMoudle.userDatabase()
    time = datetime.datetime.now()
    time_str = time.strftime(("%d/%m/%y")) # String of the date
    if(not DATABASE.CheckIfUserIdExist(str(chat_id))):
        print(f"User id {chat_id} does not exist")
        send_message("You have to register in order to order. User /start",chat_id)
        return
    print("User "+ str(chat_id) + "Exists")
    print("Cheking if he orders today " + time_str)
    if (DATABASE.checkIfOrderExist(str(chat_id),time_str)):
        send_message("You have already ordered today, Sorry!"
                     "\nCome back tomorrow", chat_id)
        return
    print("User "+ str(chat_id) + " Hasn't orders on "+ time_str)
    if chat_id in orders_in_progress:
        send_message("You have already opened an order"
                     "\nWrite what you want pizza,toast or falafel", chat_id)
    orders_in_progress.append(chat_id)
    send_message("We are ready to take your order"
                 "\nWrite what you want pizza,toast or falafel", chat_id)

def place_order(chat_id,food_type):
    """Places an order after given valid information"""
    """param: chat_id : int :The user id in telegram"""
    """param: food_type : string :The food type"""
    DATABASE = DatabaseMoudle.userDatabase()
    time = datetime.datetime.now()
    time_str = time.strftime(("%d/%m/%y"))  # String of the date
    print(f"Placing order to {chat_id}, of {food_type} in {time_str}")
    DATABASE.addOrder(str(chat_id), food_type, time_str)
    send_message(f"Ordered {food_type} in {time_str}",chat_id)
    orders_in_progress.remove(chat_id)




def register(user,password):
    """Registers a user by a given password"""
    """param: user : Class user_in_registration object"""
    """param: password : string :The password given"""
    DATABASE = DatabaseMoudle.userDatabase()
    print(f"in register {int(user.id)}")
    if(user.pass1 is None):
        user.pass1 = password
        return
    if (user.pass2 is None):
        user.pass2 = password
        if(user.pass1 == user.pass2 and not DATABASE.CheckIfUserIdExist(str(user.id)) and not user.pass2 in NON_VALID_PASSWORDS):
            print(f"Adding User {user.id}  with pass {user.pass2}")
            DATABASE.addUser(str(user.id), user.pass2)
            print(f"User {user.id} has succesfully registred with pass {user.pass2}")
            send_message(f"You have been successfully registered id: {user.id} password: {user.pass2}\n Use /order to order food", user.id)
            users_in_reg.remove(user)
            return
        else:
            send_message("Passwords does not match or its a non-valid for use please use /start again!", user.id)
            users_in_reg.remove(user)
            return



def help(chat_id,firstname):
    """Function that send the help message to a user by request"""
    """param: chat_id : int:  user id"""
    """param: firstname : string :The name of the user"""
    text = Responses.help_text(firstname)
    send_message(text, chat_id)

def myorders(chat_id):
    """Function that send the user order list"""
    """param: chat_id : int:  user id"""
    DATABASE = DatabaseMoudle.userDatabase()
    if not DATABASE.CheckIfUserIdExist(str(chat_id)):
        send_message("You are not registered use /start", chat_id)
        return
    text = "Your orders:\nDate       | Food\n"
    order_list = DATABASE.fetchOrders(str(chat_id))
    for item in order_list:
        text += f"{item[2]} |{DatabaseMoudle.FOODTYPE[item[1]]}\n"

    send_message(text,chat_id)

def passwordshow(chat_id):
    """Function that send the user id and password by request"""
    """param: chat_id : int:  user id"""
    DATABASE = DatabaseMoudle.userDatabase()
    if(not DATABASE.CheckIfUserIdExist(str(chat_id))):
        send_message("You are not registered use /start",chat_id)
        return
    user_data = DATABASE.fetchUserInfo(str(chat_id))
    print(user_data)
    send_message(f"ID:{user_data[0][0]}\nPassword:{user_data[0][1]}",chat_id)

def echo_all(updates):
    """Function that passes on all the sent messages in updates and deals with them"""
    """param: updates : list of json strings given at getUpdate for the last messages"""
    for update in updates["result"]:
        try:
            know_cmd_flag=0 #cmd flag

            text = update["message"]["text"] #text sent
            chat_id = update["message"]["chat"]["id"] #user id
            first_name = update["message"]["chat"]["first_name"] #first name
            for user in users_in_reg: #Check if the user in registration
                if(chat_id == user.get_id()):
                    print("Message: Found user in registration!!")
                    print(users_in_reg)
                    know_cmd_flag = 1
                    print("Message: Entering register")
                    register(user, text)


            if(chat_id in orders_in_progress): #Check if user is in mid order
                text = text.lower()
                if text not in DatabaseMoudle.FOODTYPE:
                    send_message(f"{text} is not a valid food type, Please use pizza,toast of falafel.\nTo order "
                                 f"again use /order", chat_id)
                    orders_in_progress.remove(chat_id)
                else:
                    place_order(chat_id,text)
                continue

            if(text == '/start'): # /start function
                if(not know_cmd_flag):
                    know_cmd_flag = 1
                    start_chat(chat_id)
                    continue
            if(text == '/order'): # /order function
                if (not know_cmd_flag):
                    know_cmd_flag = 1
                    print("Order from user "+ str(chat_id))
                    start_order(chat_id)
                    continue
            if (text == '/help'): # /help function
                if (not know_cmd_flag):
                    know_cmd_flag = 1
                    print(f"Help function for user {chat_id}")
                    help(chat_id,first_name)
                    continue
            if (text == '/myorders'):# /myorder function
                if (not know_cmd_flag):
                    know_cmd_flag = 1
                    print(f"/myorder function for user {chat_id}")
                    myorders(chat_id)
                    continue
            if (text == '/password'):# /password fucntion
                if (not know_cmd_flag):
                    know_cmd_flag = 1
                    print(f"/password function for user {chat_id}")
                    passwordshow(chat_id)
                    continue

            if(not know_cmd_flag):
                send_message("Unknown cmd, use /help if needed", chat_id)
        except Exception as e:
            print(e)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        print(updates)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
