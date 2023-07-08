# chr0m3x
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
# Desc      :   Client script for Chrome Data Exfiltration on Windows unlocked machines.
#               This script will both work locally on the target machine or send the chrome db and the userprofile key to a server machine with all the .NET utility installed.
#               Check the server side script at http://github.com/0xb4dbyt3/<ADD NEW URL> if you will use the WORK_ONLINE attack type.
#
# Thanks    :   Thanks to thepythoncode.com for the article that saves me a lot of time (https://www.thepythoncode.com/article/extract-chrome-passwords-python)
#
# Params    :   
#   WORK_ONLINE     -> Set this variable at False to save db and key on the Bash Bunny. Set it to True to exfiltrate through SCP
#   HOST            -> This should be the IP of the FTP server
#   PORT            -> This should be the PORT of the FTP server (for testing you can use python-ftp-server)
#   FTP_USERNAME    -> This should be the username to login into the ftp server
#   FTP_PASSWORD    -> This should be the password to login into the ftp server
Chrome Data exfiltration tool - Standalone plus Bashbunny payload
