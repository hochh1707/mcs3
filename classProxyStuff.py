import requests
import random
import os
import time
from classLogStuff import classLogStuff

class classProxyStuff:
    cl = classLogStuff()
    usProxies = []
    currentProxyIndex = 0

    def getProxy(self):
        proxy = self.getNextProxy()
        if not proxy:
            msg = "zzz30 failed to get a proxy from file"
            self.cl.log(msg)
            exit(msg)
        return proxy

    def getNextProxy(self):
        if (len(self.usProxies)-1 < self.currentProxyIndex): return False
        thisProxy = self.usProxies[self.currentProxyIndex]
        self.currentProxyIndex += 1
        return thisProxy

    def getListOfUSproxies(self):
        #if proxy file already exists, and file is less than 60min old, load them
        if self._checkFileProxyList():
            self._loadProxyList()
            return True
        #if proxy file does not exist or is more than 60min old, request proxies
        proxyList = self._requestProxies()
        #put proxies into file and load them
        if proxyList:
            f1 = open("./proxy_list.txt","w")
            for j in proxyList:
                print(j,file=f1)
            f1.seek(0)
            f1.close
            self._loadProxyList()
            return True
        else:
            return False

    def _loadProxyList(self):
        f2 = open("./proxy_list.txt","r")
        for j in f2:
            j = j[0:len(j)-1]
            self.usProxies.append(j)
        f2.seek(0)
        f2.close
        if len(self.usProxies)>1:
            return True
        else:
            return False

    def _checkFileProxyList(self):
        try:
            uuu = os.path.getmtime("./proxy_list.txt")
        except:
            return False
        if (time.time() - uuu) > 60*60:
            return False
        return True

    # def loadFileProxyList(self):

    def _requestProxies(self):
        aSession = requests.session()
        headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"en-US,en;q=0.9",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Content-Type":"application/x-www-form-urlencoded",
            "DNT":"1",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
        }
        aSession.headers.update(headers)
        url = "http://list.didsoft.com/get?email=31west@gmail.com&pass=rs8ftj&pid=http2000&showcountry=yes&https=yes"
        try:
            proxies = aSession.get(url,timeout=20)
        except requests.Timeout as err:
            msg = "Requested proxies. Timed out."
            self.cl.log(msg)
            exit(msg)
        except requests.RequestException as err:
            msg = "Requested proxies. Request failed."
            self.cl.log(msg)
            exit(msg)
        else:
            usProxies = []
            for j in proxies.content.decode("utf-8").split("\n",maxsplit=-1):
                if j[len(j)-3:len(j)] == "#US": usProxies.append(j[0:len(j)-3])
            if len(usProxies) >= 1:
                msg = "Requested proxies. Received " + str(len(usProxies)) + "."
                print(msg)
                self.cl.log(msg)
                return usProxies
            else:
                msg = "Requested proxies. Received none."
                self.cl.log(msg)
                exit(msg)
