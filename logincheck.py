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
        data['lgn'] = 'b0900158'
        data['pwd'] = 'Mason8912180203'
        resp = s.post('http://140.112.17.207/login',data)
        if resp.text.find("帳號或密碼錯誤") == -1:
            print("Login Succesfully!")
            break
        else:
            print(resp.text.find("帳號或密碼錯誤"))
    return s

login()