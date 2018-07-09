from datetime import datetime
from random import choice
from termcolor import colored
from pip._vendor.distlib.compat import raw_input

import details
from details import secret
from details import chatmessage, secret, s
from steganography.steganography import Steganography
import csv

print("welcome to Secret chat")
print("lets get started")
#=======================================================================================================================
def load_friends():
    #global secret
    with open('friends.csv','rU') as friends_data:              #opening file
        reader = list(csv.reader(friends_data, dialect='excel'))                    #reading data
        for row in reader[1:]:
            if row:
                m=row[0]
                name = (row[1])
                age = (row[2])
            #online = row[3]
                s = secret(m, name, age)
                friends.append(s)


#===========================================================================================================================


def chatload_friends():
    with open('chats.csv','rU') as chats_data:
        reader = list(csv.reader(chats_data, dialect='excel'))
        for row in reader[1:]:
            if row:
                sender=row[0]
                messege_sent_to=row[1]
                text=row[3]
                time=row[4]
                sent_by_me=row[4]
                chatlist=[sender,messege_sent_to,text,time,sent_by_me]


#================================================================================================================================

STATUS_MESSAGES = ["Busy", "Sleeping", "in the gym", "Available"]
friends = []                        #creating list

load_friends()                  #calling function
chatload_friends()              #calling function


#=============================================================================================================================================


def add_status(current_status_message):
    if current_status_message != None:
        print("your current status is" + " " + current_status_message)
    else:
        print("you dont have any status")
    status = raw_input("do you want to select from old status? y or n")
    if len(status) >= 1:
        if status.upper() == 'Y':
                serial = 1
                for old_status in STATUS_MESSAGES:
                    print(str(serial) + ". " + old_status)
                    serial = serial + 1
                user_selection = input("which one do you want to select :")
                new_status = None
                if len(STATUS_MESSAGES) >= user_selection:
                    new_status = STATUS_MESSAGES[user_selection - 1]
                else:
                    print("invalid selection")
                return new_status

        elif status.upper() == 'N':
                new_status = raw_input("enter your new status")
                if len(new_status) > 1:
                    STATUS_MESSAGES.append(new_status)
                else:
                    print("please enter something")
                return new_status
        else:
                print("invalid entry")
    else:
        set_status="no status"
        return set_status



#=============================================================================================================================================


def add_friend():               #function used for adding friends
    new_friend = {
        'm': '',
        'name': '',
        'age': 0,
        'is_online':True,
        'chats' : []
    }
    valid_name=True
    valid_salutation=True
    while valid_name:
        new_friend['name'] = raw_input("whats your friend name")
        if len(new_friend['name'])>=3:
            while valid_salutation:
                new_friend['salutation'] = raw_input("what should we call your friend mr. or ms.")
                if len(new_friend['salutation'])>=2:
                    new_friend['name'] = new_friend['salutation'] + " " + new_friend['name']
                    valid_name=False
                    valid_salutation=False
                else:
                    print("invalid saliutation")
        else:
                print("please enter valid name")
        valid_age=True
    while valid_age:
        new_friend['age'] = raw_input("whats age of your friend")
        if len(new_friend['age'])>0:
            valid_age=False
        else:
            print("invalid age")
        new_friend['is_online'] = True
        if len(new_friend['name'])>=3 and 80>=new_friend['age']>=10:
            friends.append(new_friend)
            with open('friends.csv','a') as friends_data:
                writer = csv.writer(friends_data)
                writer.writerow([new_friend['name'],new_friend['age'],new_friend['is_online']])
        else:
            print("friend can not be added")
    return len(friends)



#===============================================================================================================================================


def select_a_friend():                  #function to choose/select a friend
    serial_no = 1
    for frnd in friends:
        print str(serial_no) + " " + frnd.m
        serial_no = serial_no + 1
    user_selected_friend = input("select your friend")
    user_index = user_selected_friend - 1
    return user_index




#==============================================================================================================================================


def send_message():             #function for sending message
    user_frnd_index = select_a_friend()
    original_img = raw_input("what is the name of your image")
    text = raw_input("what is your message to encode")
    output_path = 'output.jpg'
    Steganography.encode(original_img, output_path, text)           #encoding messege
    new_chat = {
        "sender" : s.name,
        "message_sent_to":friends[user_frnd_index].name,
        "message" : text,
        "time" : datetime.now(),
        "sent_by_me" : True
    }
    friends[user_frnd_index].chats.append(new_chat)
    with open('chats.csv','a') as chats_data:                                       #writing to file
        writer = csv.writer(chats_data)
        writer.writerow([new_chat['sender'],new_chat['message_sent_to'],new_chat['message'],new_chat['time'],new_chat['sent_by_me']])
    print colored("your messege is sent","red")


#===========================================================================================================================================


def read_message():
    sender = select_a_friend()
    output_path = raw_input("what is output path")
    secret_text = Steganography.decode(output_path)                 #decoding the messege
    #friends[sender]['chats'].append(new_chat)
    print colored("your secret message is"+ " " + secret_text,"red")


#===========================================================================================================================================


def readchatload_friends(choice):
    name_friend=friends[choice].name
    with open('chats.csv','rU') as chats_data:
        reader = list(csv.reader(chats_data,dialect='excel'))
        check=False
        for row in reader[1:]:
            if row:
                if(row[1]==name_friend):
                    check = True
                    print colored(row[2],"red")
                    print colored(row[3], "blue")


#======================================================================================================================================


def start(m, name, age):     #main function
    current_status_message = None
    show_menu = True
    while show_menu:
        menu_choice = input("what do you want to do? \n 0.Exit \n 1.status update \n 2.Add a friend \n 3.Send a message \n 4.Read message \n 5.show chat message history")
        if menu_choice == 1:
            current_status_message = add_status(current_status_message)
            #if len(current_status_message) >= 1:
            if current_status_message == None:
                print("you didn't select the status correctly")
            else:
                print colored("you status is updated to" + " " +current_status_message,"blue")
            #else:
             #    print("you didn't select the status correctly ")

        elif menu_choice == 2:
            no_of_friends = add_friend()
            print("no. of friends you have " + " " + str(no_of_friends))

        elif menu_choice == 3:
            send_message()

        elif menu_choice == 4:
            read_message()

        elif menu_choice == 5:
            print("select a friend whose chat u want to see")
            choice = select_a_friend()
            readchatload_friends(choice)

        elif menu_choice == 0:
            print("logging you out")
            show_menu = False
            exit()

        else:
            print("wrong choice")


on=True
while on:
        user = raw_input("are you an existing user:: Y or N")
        if user.upper() == 'Y':
            print colored("\n we have your detail","yellow")
            start(s.m, s.name, s.age)
        elif user.upper() == 'N':

            valid_name=True
            valid_sal=True
            valid_age=True
            while valid_name:
                s.name= raw_input("whats your name")
                if len(s.name) >= 3:
                        print colored("hello" + " " + s.name,"red")
                        while valid_sal:
                            s.m = raw_input("how would you like to recognise mr. or ms.")
                            if len(s.m) >= 2:
                                print colored("well ok" + " " +s.m + " " + s.name,"red")
                                valid_name=False
                                valid_sal=False
                            else:
                                print("\n")
                                print("inputted wrong entry")
                else:
                    print("enter atleast 3 charecters")
            while valid_age:
                s.age = raw_input("enter your age(only numbers) :")
                if len(s.age)>0:
                    print colored("\n we are done","red")
                    valid_age = False
                    start(s.m,s.name,s.age)
                else:
                    print("incorrect age")
            on=False
        else:
            print("\n wrong choice")
