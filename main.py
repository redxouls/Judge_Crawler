from bs4 import BeautifulSoup
import requests, json, os
import tools, crawlusr
def api(level):
    valid1 = ['1','2','3','c','q']
    valid2 = ['1','2','3','c','q']
    while level == 1:
        print('1. Login for more features')
        print('2. Problems')
        print('3. Check my latest submission status')
        print('c: clear screen')
        print('q: exit')
        selection = input('Please input a number to move on\n')
        if selection in valid1:
            clear()
            return selection
        else:
            print('Invalid input')
    while level ==2:
        print('1. Download all of my code')
        print('2. Download all my ac code')
        print('3. Check Certain code with sid')
        '''
        print('c: clear screen')
        '''
        print('q: exit')
        selection = input('Please input a number to move on\n')
        if selection in valid2:
            clear()
            return selection
        else:
            print('Invalid input')
    
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
clear()
while True:
    clear()
    selecton = api(1)
    if selecton == '1':
        session, lgn = tools.login()
        uid = str(tools.getuid(lgn))
        me = crawlusr.user(uid)
        print(me)
        selection = api(2)
        if selection == '1':
            print(selection)
            me.fetch_all(session=session,r=False, status ='all')
            print('-------------')
            input('Press enter to move on')
        if selection == '2':
            print(selection)
            me.fetch_all(session=session,r=False,status ='AC')
            print('-------------')
            input('Press enter to move on')
    if selecton == '2':
        tools.latestproblem()
    if selecton == '3':
        while True:
            try:
                uid = str(tools.getuid())
                n = input("How many?\n")
                me = crawlusr.user(uid) 
                me.latest_submissions(int(n))
                print("------------------------")
                input("Press enter to move on")
                break
            except:
                print('Error: Please try again')
    if selecton == 'c':
        os.system('cls' if os.name == 'nt' else 'clear')
    if selecton == 'q':
        break
