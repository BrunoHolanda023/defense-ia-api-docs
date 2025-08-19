# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import defenselib

if __name__ == '__main__':
    serverIP = '10.200.19.75'
    username = 'system'
    password = 'admin123'
    [token, tempSig, signature] = defenselib.Login(serverIP, username, password)



    r = defenselib.list_department(serverIP,token,tempSig)
    print('Department list: '+r.text+'\n')

    r = defenselib.get_device_tree(serverIP,token,tempSig)
    print('Device Tree: ' + r.text + '\n')

    [r, mqttPassword,mqttMqtt,mqttOpenWireAddr,mqttUserName] = defenselib.get_MQ_address(serverIP, token, signature)
    print('MQ Config: ' + r.text + '\n')

    #Personnel Managment to Access Control on Defense client

    r = defenselib.add_person(serverIP,token)   #the payload is described inside the function

    r = defenselib.get_person(serverIP, token, '2048')

    #update_person(serverIP, token, '2048')     #the payload is described inside the function

    #delete_person(serverIP, token, '53738,222')


    # Access Control
    defenselib.get_door_globalcontrol_status(serverIP, token)

    defenselib.open_door(serverIP, token, '1000000$7$0$0')  # This ID can be gotten in the device list, notice that the channel $7$0 is related to doors

    defenselib.close_door(serverIP, token, '1000000$7$0$0')



