import requests
import random
import time
from classLogStuff import classLogStuff
from classProxyStuff import classProxyStuff

class classScraper:
    cl = classLogStuff()

    def scraperMain(self,mode):
        """
        1) Cron job hits python app
        2) Get proxy list
        3) Parse proxy list for US only
        4) Pick a random number from 1-5 and only continue if the number is 2
        5) Pick a random number between 1-5 and plan to send that many requests
        6) For each request:
            6a) Pick a random number between 1-5 for each request, and wait that many seconds before sending the request
            6b) Pick a random proxy from the list of US proxies
            6d) Pick random 6 digit number from 100000 to 399999 and that will be the property ID
            6e) Send request, check for property not found page, or error page
            6f) Record property ID in log of good or bad property IDs
            6g) For successful requests, save HTML in a text file to parse later. Named property id_date.txt
        """
        cp = classProxyStuff()
        cs = classScraper()
        cl = classLogStuff()
        cp.getListOfUSproxies()

        if(mode == "d"):
            print("Dev mode")
            howManyRequests = 1
        if(mode == "p"):
            print("Production mode")
            randomNum = random.randint(1,5)
            if randomNum == 2: 
                print("Random number is 2, contiue with program.")
                howManyRequests = random.randint(1,5)
                print("How many requests: " + str(howManyRequests))
            else:
                exit("Random number generated between 1 and 5 is " + str(randomNum) + ". Do not continue because number is not 2")

        cl.dashboard(mode)
        cl.aggregate(mode)

        ## Loop one time for each request we are supposed to do
        for i in range(0,howManyRequests):
            time.sleep(random.randint(1,10))
            propertyID = cs.getPropertyID()
            propertyResult = False
            ## Cycle through proxies until one of them works
            while propertyResult == False:
                time.sleep(random.randint(1,5))
                proxy = cp.getProxy()
                propertyResult = cs.scrape(proxy,propertyID)
            validPropertyID = cs.checkResult(propertyID,propertyResult)
            if validPropertyID:
                f1=open("./properties/" + time.strftime("%Y%m%d") + "_" + str(propertyID) + ".txt","w")
                print(propertyResult.content.decode("utf-8"),file=f1)
                f1.close
        return "aaa61"

    def scrape(self,proxy,propertyID):
        msg = time.strftime("%Y%m%d") + "_" + str(propertyID)
        self.cl.log(msg,"log_attempted_scrapes")
        aSession = requests.session()
        propertyUrl = "https://propaccess.trueautomation.com/clientdb/Property.aspx?cid=20&prop_id=" + str(propertyID)
        headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"en-US,en;q=0.9",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Content-Type":"application/x-www-form-urlencoded",
            "DNT":"1",
            "Host":"propaccess.trueautomation.com",
            "Origin": "https://propaccess.trueautomation.com",
            "Referer":"https://propaccess.trueautomation.com/ClientDB/PropertySearch.aspx?cid=20",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
        }
        aSession.headers.update(headers)
        try:
            propertyResult = aSession.get(propertyUrl,proxies={"http":proxy},timeout=20)
        except requests.Timeout as err:
            return False
        except requests.RequestException as err:
            return False
        else:
            return(propertyResult)

    def checkResult(self,propertyID,propertyResult):
        if "Sorry for the inconvenience" in propertyResult.content.decode("utf-8"):
            msg = time.strftime("%Y%m%d") + "_" + str(propertyID)
            self.cl.log(msg,"log_property_failed")
            print("zzz42 invalid property " + str(propertyID))
            return False
        elif "Property not found" in propertyResult.content.decode("utf-8"):
            msg = time.strftime("%Y%m%d") + "_" + str(propertyID)
            self.cl.log(msg,"log_property_failed")
            print("zzz42 invalid property " + str(propertyID))
            return False
        else:
            msg = time.strftime("%Y%m%d") + "_" + str(propertyID)
            self.cl.log(msg,"log_property_scraped")
            print("zzz58 good property " + str(propertyID))
            return True

    def getPropertyID(self):
        propertyID = False
        ## Generate a random property ID and check to make sure it has not already
        ## been tried and found to be invalid
        while propertyID == False:
            propertyID = random.randint(100000,399999)
            if self.checkForInvalidPropID(propertyID):
                propertyID = False
                continue
            if self.checkForAlreadyScrapedPropID(propertyID):
                propertyID = False
                continue
        return propertyID

    def checkForInvalidPropID(self,propertyID):
        try:
            f1=open('./logs/log_property_failed.txt', 'r')
        except:
            # If file does not exist, return False, AKA property ID is not invalid
            return False
        else:
            for p in f1:
                if p[9:15] == str(propertyID):
                    msg = time.strftime("%Y%m%d") + "_"
                    msg = msg + str(propertyID) + "_skipped_failed"
                    self.cl.log(msg,"log_property_skipped")
                    f1.seek(0)
                    f1.close
                    return True
            # If we did not find the property ID in the file, then it is not invalid
            return False

    def checkForAlreadyScrapedPropID(self,propertyID):
        try:
            f1=open('./logs/log_property_scraped.txt', 'r')
        except:
            # If file does not exist, return False, AKA property ID is not invalid
            return False
        else:
            for p in f1:
                if p[9:15] == str(propertyID):
                    msg = time.strftime("%Y%m%d") + "_"
                    msg = msg + str(propertyID) + "_skipped_scraped"
                    self.cl.log(msg,"log_property_skipped")
                    f1.seek(0)
                    f1.close
                    return True
            # If we did not find the property ID in the file, then it is not invalid
            return False
