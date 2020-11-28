from datetime import date
from datetime import datetime
import time

class classLogStuff:

    def log(self,msg,file="log_main"):
        f1=open("./logs/" + file + ".txt", 'a')
        print(msg,file=f1)
        f1.close
        
    def aggregate(self,mode):
        ## only aggregate once an hour
        if(mode == "p" and datetime.now().strftime("%M") != "51"):
            print("Production mode and not minute 51. Did not aggregate.")
            return

        f1 = open("./logs/log_property_skipped.txt","r")
        f2 = open("./logs/log_property_skips_daily.txt","a")
        today = date.today().strftime("%Y%m%d")
        todaySkips = []
        prevLineDay = ""
        countDayFailed = 0
        countDayScraped = 0
        for i in f1:
            j = i.rsplit("_",-1)
            type = j[3].split("\n")[0]
            day = j[0]
            if day == today:
                todaySkips.append(i)
                continue
            if prevLineDay == "": prevLineDay = day
            if prevLineDay != day:
                print(str(prevLineDay) + "_failed_" + str(countDayFailed),file=f2)
                print(str(prevLineDay) + "_scraped_" + str(countDayScraped),file=f2)
                prevLineDay = day
                countDayFailed = 0
                countDayScraped = 0
            if type == "failed": countDayFailed += 1
            if type == "scraped": countDayScraped += 1
        else:
            print(str(prevLineDay) + "_failed_" + str(countDayFailed),file=f2)
            print(str(prevLineDay) + "_scraped_" + str(countDayScraped),file=f2)
            f1.close
            f2.close
            f1 = open("./logs/log_property_skipped.txt","w")
            for i in todaySkips:
                i = i.split("\n")[0]
                print(i,file=f1)
            f1.close



    def dashboard(self,mode):
        ## only run dashboard once an hour
        if(mode == "p" and datetime.now().strftime("%M") != "01"):
            print("Production mode and not minute 01. Did not update dashboard.")
            return

        ## get the numbers of current month, etc.
        currentMonth = date.today().strftime("%m")
        currentYear = date.today().strftime("%Y")
        currentYearMonth = currentYear + currentMonth
        if(currentMonth != 1):
            prevYearMonth = currentYear + str(int(currentMonth) - 1)
        else:
            prevYearMonth = str(int(currentYear)-1) + str(12)

        ## setup dashboard array
        arrDashboard = {
        "scraped_2019": 0,
        "scraped_2020": 0,
        "scraped_2021": 0,
        "scraped_" + currentYearMonth: 0,
        "scraped_" + prevYearMonth: 0,
        "failed_2019": 0,
        "failed_2020": 0,
        "failed_2021": 0,
        "failed_" + currentYearMonth: 0,
        "failed_" + prevYearMonth: 0
        }

        ## scraped properties
        f1 = open("./logs/log_property_scraped.txt")
        latestScrape = 0
        for i in f1:
            if(int(i[0:8]) > latestScrape):
                latestScrape = int(i[0:8])
            if(i[0:4] == "2019"):
                arrDashboard["scraped_2019"] += 1
            if(i[0:4] == "2020"):
                arrDashboard["scraped_2020"] += 1
            if(i[0:4] == "2021"):
                arrDashboard["scraped_2021"] += 1
            if(i[0:6] == currentYearMonth):
                arrDashboard["scraped_" + currentYearMonth] += 1
            if(i[0:6] == prevYearMonth):
                arrDashboard["scraped_" + prevYearMonth] += 1
        f1.close

        ## failed pids
        f1 = open("./logs/log_property_failed.txt")
        latestFail = 0
        for i in f1:
            if(int(i[0:8]) > latestFail):
                latestFail = int(i[0:8])
            if(i[0:4] == "2019"):
                arrDashboard["failed_2019"] += 1
            if(i[0:4] == "2020"):
                arrDashboard["failed_2020"] += 1
            if(i[0:4] == "2021"):
                arrDashboard["failed_2021"] += 1
            if(i[0:6] == currentYearMonth):
                arrDashboard["failed_" + currentYearMonth] += 1
            if(i[0:6] == prevYearMonth):
                arrDashboard["failed_" + prevYearMonth] += 1
        f1.close

        ## print to file
        f1 = open("./logs/dashboard.txt","w")
        for i in arrDashboard:
            print(i + ": " + str(arrDashboard[i]),file=f1)
        f1.close

