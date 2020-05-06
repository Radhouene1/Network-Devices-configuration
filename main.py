#
# © Copyright Radhouene BELHADJ ALAYA
# Contact:
# LinkedIn : https://www.linkedin.com/in/radhouene-belhadj-alaya-b61abb109/
# Mail : bha.radhouene@gmail.com
#
#
#

import time
from netmiko import ConnectHandler

class UserPass:
    def __init__(self,username,password):
        self.username = username
        self.password = password

    def set_username(self,username):
        self.username=username

    def set_password(self,password):
        self.password = password

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password


class Scripting():

    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.device = None

    def close(self):
        self.device.disconnect()

    def open(self):
            self.device = ConnectHandler(device_type ='cisco_ios',
                                     host = self.hostname,
                                     username = self.username,
                                     password = self.password,)
            self.device.enable()

    def send_config_command(self,command):
        return self.device.send_config_set(command, delay_factor=2)


def GetIPListFromFile(path):
    IPList=[]

    with open(path) as fp:
        for line in fp:
            IPList.append(line.replace("\n", ""))
    return IPList

def GetUsersList(path):
    UsersList=[]
    with open(path) as fp:
        for line in fp:
            username = line[0:line.find(';')].replace(" ","")
            password = line[line.find(';')+1:].replace(" ","").replace("\n","")
            UsersList.append(UserPass(username,password))

    return UsersList

if __name__ == "__main__":

    configfile = open('Config.txt')
    configset = configfile.read()
    configfile.close()

    out = ""
    for IP_item in GetIPListFromFile("IP_address.txt"):

        for user in GetUsersList("Usernames.txt"):
            out= out + "\n"
            print(IP_item, "Try to connect with  username =", user.get_username(), " and password =",user.get_password())
            scr = Scripting(IP_item, user.get_username(), user.get_password())
            stop = False
            try:
                scr.open()
                stop = True
                out = out + IP_item +"; Username = "+user.get_username() + "; password ="+ user.get_password()+'\n \n \n'
                out= out +scr.send_config_command(configset) +'\n'
                time.sleep(0.5)
                scr.close()
            except:
                print("It's not the right User")
            if (stop):
                break

    with open("Output.txt", "w+") as f:
        f.write(out)