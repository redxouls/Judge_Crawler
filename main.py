from bs4 import BeautifulSoup
import requests, json, os
import tools, usr
def api(level):
    valid1 = ['1','2','3','4','q']
    valid2 = ['1','2','3','logout','q']
    clear()
    while level == 1:
        print('1. Login for more features')
        print('2. Problems')
        print('3. Check my latest submission status')
        print('4: submissions(live)')
        print('q: exit')
        selection = input('Please input something to move on\n')
        if selection in valid1:
            clear()
            return selection
        else:
            print('Invalid input')
    while level ==2:
        print('1. Download all of my code')
        print('2. Download all my ac code')
        print('3. Check Certain code with sid')
        print('logout : logout my account')
        print('q: exit')
        selection = input('Please input something to move on\n')
        if selection in valid2:
            clear()
            return selection
        else:
            print('Invalid input')
    
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()
restext = ['', 'CE', 'OLE', 'MLE', 'RE', 'TLE', 'WA', 'AC', 'Uploading...', 'PE']
session = None

while True:
    clear()
    selecton = api(1)
    if selecton == '1':
        if session == None:
            session, lgn = tools.login()
        uid = str(tools.getuid(lgn=lgn))
        me = usr.user(uid)
        selection = api(2)
        if selection == '1':
            me.fetch_all(session=session,r=False, status ='all')
            print('-------------')
            input('Press enter to move on')
        if selection == '2':
            me.fetch_all(session=session,r=False,status ='AC')
            print('-------------')
            input('Press enter to move on')
        if selection == '3':
            while True:
                sid = input("sid: ")
                try:
                    tools.download_source(session=session,sid=sid,r=True,status='all',solo=True)
                    filename = "./temp/"+ str(sid)+ ".txt"
                    with open(filename,'r') as f:
                        clear()
                        print(f.read())
                        print('---------------------')
                        input('Press any key to continue')
                    break
                except:
                    print("Failed to acquire the source file!!!")
        if selection == 'logout':
            session = None
    if selecton == '2':
        tools.latestproblem()
    if selecton == '3':
        while True:
            try:
                uid = str(tools.getuid())
                print(uid)
                n = input("How many?\n")
                me = usr.user(uid) 
                me.latest_submissions(int(n))
                print("------------------------")
                input("Press enter to move on")
                break
            except:
                print('Error: Please try again')
    if selecton == '4':
        response = requests.get("http://140.112.17.207/api/submission")
        subs = json.loads(response.text)
        for sub in subs:
            print('{0}: {1} {2} {3} {4}'.format(sub['ttl'],restext[int(sub['res'])],sub['scr'],sub['sid'],tools.getuid(uid =str(sub['uid']))))
        print('---------------------------')
        input('Press any key to continue')
    if selecton == 'q':
        break
