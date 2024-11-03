#!/usr/bin/env python

import json
import hashlib
import requests
import argparse


parser = argparse.ArgumentParser("bitwarden account check")
parser.add_argument("filename", help="bitwarden json export", type=str)
args = parser.parse_args()

file = open(args.filename, "r")
bitwardendata = json.load(file)
file.close()


breachedaccounts = []
for item in bitwardendata["items"]:
    if (("login" in item ) and not (item["login"]["password"] == None)):
        if "username" in item["login"]:
            username = item["login"]["username"]
        else:
            username = " "
        #edge case where the user name field is there but there is no value in it.
        if username == None: username = " "
        if "name" in item:
            name = item["name"]
        else:
            name = " "

        password = item["login"]["password"]


        passwordhash = hashlib.sha1(str(password).encode("utf-8")).hexdigest()
        #API returns in all caps. 
        passwordhash = passwordhash.upper()
        # needs first 5 https://haveibeenpwned.com/API/v3#PwnedPasswords
        first5ofhash = passwordhash[:5]
        potentialpasswordmatchs = requests.get("https://api.pwnedpasswords.com/range/" + first5ofhash)
        potentialpasswordmatchs = potentialpasswordmatchs.content.decode("utf-8")

        for potentialpasswordmatch in potentialpasswordmatchs.splitlines():

            potentialpasswordmatch = potentialpasswordmatch.split(":")[0]
            #API only returns suffix reading prefix
            potentialpasswordmatch = first5ofhash + potentialpasswordmatch
            if passwordhash == potentialpasswordmatch:
                breachedaccount = dict()
                breachedaccount["password"] = password
                breachedaccount["username"] = username
                breachedaccount["name"] = name


                breachedaccounts.append(breachedaccount)
                
        print(name + ": " + username + " checked")
        

print("Breached accounts")
for account in breachedaccounts:

    print("Breached: " + account["name"] + " user: " + account["username"] + " Password: " + account["password"])
