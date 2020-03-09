#client.py

import http.client
import sys
import urllib.parse
import json

ipaddress = "192.168.208.254"
client = http.client.HTTPConnection(ipaddress , 5555)
headers = {'Content-type': 'application/json'}

def makeLogin():
    client = http.client.HTTPConnection(ipaddress , 5555)
    arrayOfStrings = []
    print("Login: Enter username")
    line = sys.stdin.readline().strip()
    arrayOfStrings.append(line)
    print("Login: Enter location")
    location = sys.stdin.readline().strip()
    arrayOfStrings.append(location)
    print("Login: Enter Type: passenger or driver")
    type_ = sys.stdin.readline().strip()
    arrayOfStrings.append(type_)
    params = {"uname": arrayOfStrings[0], "location": arrayOfStrings[1], "type": arrayOfStrings[2]}
    params = json.dumps(params)
    client.request("POST" , "/login", params,headers)
    response = client.getresponse() 
    response = response.status

    return [response, type_,location,line]

def makeLocate(city):
    client = http.client.HTTPConnection(ipaddress , 5555)

    print("Locating Drivers nearby:")
    client.request("GET", "/locate?city=" + city)
    res = client.getresponse()
    data = res.read().decode('utf-8')
    return json.loads(data)

def makeBooking(driver,origin,destination):
    client = http.client.HTTPConnection(ipaddress , 5555)

    params = {"driver": driver, "origin": origin, "dest": destination}
    params = json.dumps(params)
    client.request("POST" , "/book", params,headers)

def booking_menu(location):
    while True:
        list_of_drivers = makeLocate(location)
        while len(list_of_drivers) < 1:
            print("Enter for locating drivers within your city")
            line = sys.stdin.readline()
            list_of_drivers = makeLocate(location)
            if not list_of_drivers:
                print('No drivers found. Retrying')

        print("Select from available drivers:")
        for i in range(len(list_of_drivers)):
            print(str(i + 1) + ": " + str(list_of_drivers[i]))
        selection = sys.stdin.readline()
        # assume number selected is correct
        print("Enter origin location:")
        origin = sys.stdin.readline().strip()
        print("Enter destination location:")
        destination = sys.stdin.readline().strip()
        makeBooking(list_of_drivers[int(selection)-1], origin, destination)

def awaitNotif(driver):
    print("Waiting for a notification:")
    client.request("GET", "/notif?driver=" + driver)
    res = client.getresponse().read().decode('utf-8')
    res = json.loads(res)
    if res:
        print("you have got notification" , res)
    import time
    time.sleep(2)
    awaitNotif(driver)


if __name__ == '__main__':

    while True:
        result = makeLogin()
        while result[0] == 500:
            print("Username taken.Please try again")
            result = makeLogin()

        if result[1] == "driver":
            awaitNotif(result[3])

        elif result[1] == "passenger":
            booking_menu(result[2])
        else:
            print("invalid type")
            pass
















