from bs4 import BeautifulSoup
import requests, json, os, collections
def login():
    data = {'lgn':"",'pwd':""}
    s = requests.session()
    while True:
        '''
        data['lgn'] = input("username: ")
        data['pwd'] = input("password: ")
        '''
        data['lgn'] = 'b08901058'
        data['pwd'] = 'Mason8912180203'
        resp = s.post('http://140.112.17.207/login',data)
        if resp.text.find("帳號或密碼錯誤") == -1:
            print("Login Succesfully!")
            break
        else:
            print("帳號或密碼錯誤")
    return s, data['lgn']

def download_source(*,session,sid,r,status='all'):
    print('sid')
    s = session
    data = json.loads(requests.get('http://140.112.17.207/api/result?sid='+str(sid)).text)[0]
    res, ttl, scr, uid = int(data['res']), str(data['ttl']), str(data['scr']), str(data['uid'])
    restext = ['', 'CE', 'OLE', 'MLE', 'RE', 'TLE', 'WA', 'AC', 'Uploading...', 'PE']
    if restext[res]!= status and status !='all':
        return 'not' + status
    try: 
        name = '_'.join(ttl.split(' '))
    except:
        name = ttl
    try:
        os.mkdir('./'+uid+"/"+name)
    except:
        pass
        #print(str(sid)+".txt"+"existed")
    filename = "./"+uid+"/"+ name +"/"+str(sid)+".txt"
    if str(sid)+".txt" in os.listdir('./'+uid+"/"+name) and not r:
        return str(sid)+"Existed!"
    
    resp = s.get('http://140.112.17.207/source/highlight/'+str(sid))
    source = s.get('http://140.112.17.207/source/'+str(sid))
    soup = BeautifulSoup(resp.text,'html.parser')
    if soup.find('h3').string != 'Result':
        return str(sid)+"Error message!"
    raw = soup.find('table',{'class':'pure-table'})
    task_raw = raw.find_all('td')
    alltask, allstatus, = [], []
    for td in task_raw:
        if td.string!=None:
            alltask.append(td.string)    
    status_raw = raw.find_all('span')
    for ele in status_raw:
        allstatus.append(ele.string)
    pre_raw = raw.find_all('pre')
    allmessage = ['\n']*len(alltask)
    for i in range(len(pre_raw)):
        try :
            temp = pre_raw[i]
            allmessage[i] = temp.string.strip('\n')
        except:
            pass
    with open(filename,'w') as f:
        f.write(ttl+": "+scr+'pt'+'\n'*3)
        for i in range(len(allstatus)):
            f.write(alltask[i]+": "+allstatus[i]+"\n")
            f.write(allmessage[i])
        f.write('\n')
        f.write('source.py'+'\n')
        f.write(source.text)
    return str(sid)+": Sucessful!" 

def update_usr_dic():
    response = requests.get("http://140.112.17.207/ranklist?page=2")
    soup = BeautifulSoup(response.text,'html.parser')
    pagelink = soup.find_all('a',{"class":"page-number"})
    usr = dict()
    for link in pagelink:
        response = requests.get("http://140.112.17.207"+ link.get('href'))
        soup = BeautifulSoup(response.text,'html.parser')
        a = soup.find_all('a',{"class":"nav_a"})
        for i in a:
            usernumber = i.get('href').split("/")[1].lower()
            username = i.string
            usr[username] = usernumber
    with open('user.json','w') as f:
        f.write(json.dumps(usr))
    return usr

def update_problemset():
    response = requests.get("http://140.112.17.207/problems/domain/0#1")
    soup = BeautifulSoup(response.text,'html.parser')
    problemlinks = soup.find_all('a',{"class":"pure-menu-link","style":"text-overflow: ellipsis;"})
    problemset = dict()
    problempage = []
    payloads = {'did':'0','uid':'101','lid':'1'}
    for link in problemlinks:
        if link.get("href") == None:
            continue
        problempage.append(link.get("href").strip("#"))
    for tag in problempage:
        payloads['lid'] = tag
        response = requests.get("http://140.112.17.207/api/problems",payloads)
        data = json.loads(response.text)['plist']
        subs = json.loads(response.text)['subs']
        for i in range(len(data)):
            problem = data[i]
            sub = subs[i]
            problemset[problem['pid']] = (problem['ttl'], str(sub['ac']))
    problemset =  collections.OrderedDict(sorted(problemset.items()))
    with open('problemset.json','w') as j:
        j.write(json.dumps(problemset))
    with open('problemset.txt','w') as t:
        for key in problemset:
            t.write(str(key)+": "+str(problemset[key][0])+'\n'*2)

def getuid(lgn=''):
    update_usr_dic()
    with open('user.json','r') as f:
        usrdict = json.loads(f.read())
    if lgn =='':
        while(True):
            username = input("username: ")
            if username in usrdict:
                return usrdict[username]
            else:
                print('Error: username not found')
    else:
        username = lgn
        if username in usrdict:
            return usrdict[username]
        else:
            print('Error: username not found')

def latestproblem():
    update_problemset()
    with open('problemset.json') as f:
        probdict = json.loads(f.read())
    count = 0
    while True:
        print("1. latest problems")
        print('2. all problems')
        print('b: back')
        selection = input('Please choose a mode\n')
        if selection == 'q':
            return
        else:
            if selection in ['1','2']:
                mode = selection
                break
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Error: Invalid Input!")
    if mode == '1':
        for key in probdict:
            if int(probdict[key][1]) <40:
                print(key,probdict[key][0])
                count += 1
        if count == 0:
            temp = 0
            for key in probdict:
                temp+=1
                if temp>len(probdict)-5:
                    print(key,probdict[key][0])   
    if mode == '2':
        for key in probdict:
            print(key,probdict[key])
    print('-------------')
    input("Press enter to move on")
            