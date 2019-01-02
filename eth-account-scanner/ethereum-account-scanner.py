import json
import time
from multiprocessing import Process, Queue
import multiprocessing

import requests
from eth_account import Account



def doRequest():

    # Put your API key in here. To get one register on https://etherscan.io/
    key = ''

    # Static part of API
    link = 'https://api.etherscan.io/api?module=account&action=balancemulti&address='
    linkEnd = '&tag=latest&apikey=' + key
    
    # Etherscan API allows requests with max 20 addresses. This is the list which will contain them.
    addressList = []
    # Counter to keep track of public/private keys pairs.
    counter = 0

    # Counter to keep track of stats  
    fail = 0
    win = 0


    # Check loop begins here
    while True:

        # First the list is filled with 20 private keys and the corresponding public addresses.
        for x in range(20):
            if x != 19:
                # First 19 addresses are concatenated with a ',' to build the final API link. Parameter string is extra entropy.
                acct = Account.create('sadkjhjwk dhkdasdlkm')
                addressList.append([acct.address + ',', acct.privateKey.hex()])
            else:
                acct = Account.create('dwqdcwejnc bcbrewrijsdn')
                addressList.append([acct.address, acct.privateKey.hex()])
        
        # Concatenate link with addresses
        for add in addressList:
            link = link + add[0]

        # Concatenate link with API key
        link = link + linkEnd

        # Send request and get JSON response
        data = requests.get(link, timeout = 10)
        jdata = json.loads(data.text)

        # Loop checks if there is a > 0 balance
        for res in jdata['result']:
            
            # If there is a account with a balance > 0 then the privat key is stored in a textfile named foundKeys.txt
            if  int(res['balance']) > 0:
                f= open("foundKeys.txt","a+")
                f.write(addressList[counter][1] + "\r\n")
                win = win + 1
                
            else:
                fail = fail + 1
            
            counter = counter + 1

        
        # Refresh link, list and counter
        link = 'https://api.etherscan.io/api?module=account&action=balancemulti&address='
        addressList = []
        counter = 0
        
        # Print stats
        print(multiprocessing.current_process().name + '  win: ' + str(win) + '   fail: ' + str(fail))


# Create Threads
def createThread(Threads):
    for n in range(Threads):
        p = Process(name='p' + str(n+1),target=doRequest, args=())
        p.start()

# Main
if __name__ == '__main__':
    
    # Number of Threads. 
    Threads = 4
    createThread(Threads)
  