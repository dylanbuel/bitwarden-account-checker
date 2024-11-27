#!/usr/bin/env python

import json
import hashlib
import requests
import argparse
from concurrent.futures import ThreadPoolExecutor

def checkaccount(item):
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
                    return (breachedaccount)
def checkaccounts(threadcount, items) -> list:
    breachedaccounts = list()
    with ThreadPoolExecutor(max_workers=threadcount) as executor:
        futures = []
        for item in items:
            future = executor.submit(checkaccount, item)
            futures.append(future)
        for future in futures:
            result = future.result()
            if result != None:
                breachedaccounts.append(result)
    return breachedaccounts
if __name__ =="__main__":
    threadcount = 25
    
    # get args
    parser = argparse.ArgumentParser("bitwarden account check")
    parser.add_argument("filename", help="bitwarden json export", type=str)
    parser.add_argument("--showpasswords", help="when printing breached accounts include passwords in print", action="store_true")
    args = parser.parse_args()
    file = open(args.filename, "r")
    bitwardendata = json.load(file)
    file.close()
    breachedaccounts = checkaccounts(threadcount, bitwardendata["items"])
    #print account info
    print("Breached accounts")
    for account in breachedaccounts:
        printstring = "Breached: " + account["name"] + " user: " + account["username"]
        if (args.showpasswords):
            printstring = printstring + " Password: " + account["password"]
        print(printstring)