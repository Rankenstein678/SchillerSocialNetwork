import jsonpickle
import json
import requests
import time
import random as rn
from post import ClientPost
import hashlib
import os
from main import MyServer

ip = "http://192.168.6.179:8080"


print("""
****************************************************************************************************
***********************************************/***(/****/******************************************
//*********************************(&&&&&&&&%((//**///*/(#%&&&&%/***********************************
//***/*///******************/%&&&(//*****************************(&&&&%*****************************
////***/****************%&&%******************************************/(&&&%/***********************
///////*/***/*******#&&(***/&/*********************************************(&&&&/*******************
//////*/*///*****%&&//*/%%(&%/%&/*********************************************/&&&&&/***************
///////**///**/&&(***/####&&&&////***********************************************/&&&&**************
/////*//*/***%&%********(%&&&&#%##**************************************************(&&%************
//////////*&&%********(&&*%&%%&(******************************************************(&&(**********
//////////&&(**************%%***********************************************************#&(*********
/////////#&///*/*************************************************************************(&(********
/////////&#//*****************(/**********************************************************&&/*******
////////&%*//**/*************/&%***********************************/&&********************&&#*******
///////#&///////*//********(&&&&&%/*******************************#%&&&&/*****************%&&*******
///////&&*///*****************&&*********************************(#%%%/*******************/&&*******
///////&(**/*/*****************************************************#%/*********************&%*******
///////&(/*/****************************%(*************************************************&&*******
//////(&(/***/****/**********************/&&(**********/&&*********************************%%*******
////*/(&#///////*/*/****/***********************(((%##(************************************%&/******
//////%@/*//**//***************************************************************************&&*******
//////&&/*/*///***********************#&&&@@@@@@@&&&&&&(/*********************************#&%*******
//////@&(/*///****/***************/&&&%((/*************//%&&&(****************************/&#*******
/////@@&//**/**/*****************&&&/***********************/&&&(*************************%&(*******
/////@@&/*//*/****************(&&/*****************************&&&&/*********************%&&/*******
/////%@&////////****/*******#@&***********************************#&&(*******************%&&********
//////@@(////////**********&%/**************************************%&&/******************&%********
//////%@(///////*/*******/&(/****************************************/&&/****************/&/********
//////%@#///////////****/&(*******************************************(&&****************#&*********
/////(#@#/////////**//*/@(/********************************************#&#**************&&&*********
////(/(@#//////////*//*(&/**********************************************&&**************&&#*********
//((///@@//////////////&&***********************************************%&/*************&&%*********
//////(@@(////////*//*/&#*/*********************************************(&/*************&#**********
((/////&@%///////////*/@&//*////****************************************%&/************/&#**********
(//////#@@/////////////@@/**********************************************&&*************(&***********
/((////%@@#%########%%#%&%&&(((((//*//////**//(##%%#////////(//(((####%#&&%((((((##((((%&%**********
(((///@@@(/////////*(@@###/&&*************/&&*****#&#***************(&&***%&&#**********/&&#********
////#@@@(//////////@@%/////&%//**/*/******/&&*****(&(***************&&(*****%&&(**********#&&/******
//(%@@@//////////%@@///////&#*//*////*****(&%*****/&(**************/&&*******/&&&***********%&&/****
/(&@@&/////////#@@&////////&%/***////**/**/&(*****/&#**************&&#**********&&/***********&&%***
///@@@@@@@@@@@@@(//////////#@@@@@@@@@@@&@&#(******/&&&&&&@&&&@@@&&@@&************(&&&&&&&&&&&&&&(***\n
""")
s="Wilkommen bei Oktopost"
for i in s:
    print(i, end="")
    time.sleep(0.1)
print("\n")


# function to create users with unique usernames and a password
def createUser():
    # --------------------------------------------------
    # take user input for verification and turn it into a JSON String with @jsonpickle
    username =input("Gebe einen Benuternamen an:\n")
    password =input("Passwort: ")

    # hash the password with random 32 bit long salt and 200.000 iterations of sha256
    clum =os.urandom(32)
    key =hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), clum, 200000)

    # combine salt and key and use them as login credentials together with username
    LOGIN_CREDENTIALS =(username, clum+key)
    data = jsonpickle.encode(ClientPost(LOGIN_CREDENTIALS[0], LOGIN_CREDENTIALS[1], "", 1))
    # --------------------------------------------------
    # try to make post request to web page using previously made JSON String data with @requests
    try:
        response =requests.post(ip, data=data)
    except requests.ConnectionError as err:
        print("Server Error:\n" + str(err))
    # --------------------------------------------------
    # create user if everything is allright or restart function if userName already exists
    if response.status_code == 200:
        print(response.text)
        return(LOGIN_CREDENTIALS)
    elif response.status_code == 500:
        print(response.text)
        LOGIN_CREDENTIALS= createUser()
        return(LOGIN_CREDENTIALS)
    # --------------------------------------------------

# --------------------------------------------------
# choose between creating user or interacting with the program as a user
action = int(input("Gebe Aktion ein     \"0\" für Posts     \"1\" um User zu erstellen: \n"))
if action== 0:
    username = input("Gebe deinen Benuternamen an:\n")
    password = input("Passwort: ")

    salt =ip/salts/username
    salt =json.loads(salt)

    clum =salt["salt"]
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), clum, 200000)



elif action== 1:
    LOGIN_CREDENTIALS= createUser()
# --------------------------------------------------
# staying in loop for user to interact with posts by reading or creating them
while True:
    user_in = input("r - Gibt neuesten Post aus; p - sendet einen Post\n")
    match user_in:
        case "r":
            response = None
            # --------------------------------------------------
            # request connection to the web page (200 == positive response) using @requests
            try:
                response = requests.get(ip)
            except requests.ConnectionError as err:
                print("Server Error:\n" + str(err))
                continue
            # --------------------------------------------------
            # if connection is working the last post in the sql database from table "posts" is printed
            # calling own class from "post.py" and reading out one constructors information
            if response.status_code == 200:
                post = jsonpickle.decode(response.text)[0]
                print(f"User: {post.userID}\nTitle: {post.title}\nText: {post.text}\nLikes: {post.likes}")
            else:
                print("ErrorStatusCode = ", response.status_code)
            # --------------------------------------------------

        # --------------------------------------------------
        # user creates post by typing in the title and text of the post,
        # which are turned into a JSON String together with the User information and Likes
        case "p":
            title = input("Titel: \n")
            text = input("Inhalt:\n")
            response = None
            data = jsonpickle.encode(ClientPost(LOGIN_CREDENTIALS[0], LOGIN_CREDENTIALS[1], title, text, 0))
        # --------------------------------------------------
            # try to connect with web page as before with the same results for different response codes
            try:
                response = requests.post(ip, data=data)
            except requests.ConnectionError as err:
                print("Server Error:\n" + str(err))
                continue

            if response.status_code== 200:
                print(response.text)
            elif response.status_code== 400:
                print(response.text)
            else:
                print("ErrorStatusCode = ", response.status_code)
        # --------------------------------------------------