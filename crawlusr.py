from bs4 import BeautifulSoup
import requests, json, os
import tools

class submission:
    def __init__(self,raw):
        self.sid = raw['sid']
        self.uid = raw['uid']
        self.pid = raw['pid']
        self.res = raw['res']
        self.scr = raw['res']
        self.scr = raw['scr']
        self.ttl = raw['ttl']

class user:
    def __init__(self,uid):
        try:
            os.mkdir(str(uid))
        except:
            pass
            #print("Existed")
        self.uid = uid
        self.subcount = 0
        self.sublist = []
        self.para  = {'limit': '25', 'uid': str(self.uid),'page':'1'}    
        self.restext = ['', 'CE', 'OLE', 'MLE', 'RE', 'TLE', 'WA', 'AC', 'Uploading...', 'PE']
        print("Create user successfully")
    def update_submissions(self):
        filename = "./"+str(self.uid)+"/"+"submissions.json"
        with open(filename,'w') as f:
            f.write('[')
            for pagenum in range(100):
                self.para['page'] = pagenum
                response = requests.get("http://140.112.17.207/api/submission",self.para)
                if len(response.text) == 2:
                    break
                else:
                    a = response.text.strip('[')
                    a = a.strip(']')
                    if pagenum != 0:
                        a = ',' +a
                f.write(a)
                data = json.loads(response.text)
                for raw in data:
                    self.sublist.append(submission(raw))
            f.write(']')
        self.subcount = len(self.sublist)
    def fetch_all(self,*,session,r=False,status='all'):
        self.update_submissions()
        for i in range(len(self.sublist)):
            sub = self.sublist[i]
            print(i,": "+tools.download_source(sid = sub.sid,r=r,session=session,status=status))
    def latest_submissions(self,n):
        self.update_submissions()
        filename = "./"+str(self.uid)+"/"+"submissions.json"
        with open(filename) as f:
            sublist = json.loads(f.read())
            for i in range(n):
                sub = sublist[i] 
                ttl = sub['ttl']
                res = self.restext[int(sub['res'])]
                sid = sub['sid']
                scr = sub['scr']                
                print('{0} : {1} {2} {3}'.format(sid,ttl,res,scr))
    