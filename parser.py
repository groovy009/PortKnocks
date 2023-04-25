import re
import builtins
from datetime import datetime
import urllib.request
import json
import ast



class Log:

        def __init__(self, ip, date, requestMethod=None, requestResource=None, requestProtocol=None, rCode=None, rBytes=None, referrer=None, userAgent=None):
                self.ip = ip
                self.date = date 
                self.requestMethod = requestMethod
                self.requestResource = requestResource
                self.requestProtocol = requestProtocol
                self.rCode = rCode
                self.rBytes = rBytes
                self.referrer = referrer
                self.userAgent = userAgent

        def __repr__(self):
                return self.ip +' '+ str(datetime.fromtimestamp(self.date)) +' '+ str(self.requestMethod) + ' '+ str(self.requestResource) + ' '+ str(self.requestProtocol) + ' '+ str(self.rCode)+ ' ' +str(self.rBytes)+ ' '+ str(self.referrer) + ' '+ str(self.userAgent) 

        def lookUpIp(self):
                try:
                        addy = "https://geolocation-db.com/jsonp/" + str(self.ip)
                        with urllib.request.urlopen(addy) as url:
                                data = url.read().decode()
                                data = data.split("(")[1].strip(")")
                                dataDict = json.loads(data)
                                #print(dataDict)
                                name = dataDict["country_name"]
                                #print(name)

                                if name == "Not found":
                                        return {}
                                else:
                                        return dataDict

                except:
                        return {}





def parseDate(dateObj: str):
        
        
        d = datetime.strptime(dateObj, "%d/%b/%Y:%H:%M:%S %z")
        return d.timestamp()





def main():
        
        
        #TODO: eventaully ensure all variables are the proper data types (int, string, etc.)
       
        #scp parser.py opc@129.158.33.10:/home/opc/parser.py
        
        

        #fLine = '209.141.53.74 - - [02/Jan/2022:06:43:12 +0000] "GET /config/getuser?index=0 HTTP/1.1" 404 196 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0"'
        #https://regex101.com/r/RWo4Zb/1 
        parsing = re.compile('^(\S+).+\[(\S+ \S+)] "([^"]+)" ([^"]+) "(.+)" "([^"]+)"')
        LogList = []
       
        
        f = open("logs.txt", "r")
        for fLine in f:
                matched= parsing.match(fLine)
                if(matched == None):
                        print("Line does not match RegX")
                        print(fLine)
                else:
                        rCode = None
                        rBytes = None
                        referrer = None
                        userAgent = None
                        requestResource = None
                        requestMethod = None
                        requestProtocol=None

                        ip = matched.group(1)
                        date = parseDate(matched.group(2))
                        


                        request =matched.group(3)
                        if (request != '-'):

                                splitRequest =request.split(' ')
                                if (len(splitRequest) == 3):
                                        requestMethod = splitRequest[0]
                                        requestProtocol= splitRequest[1]
                                        requestResource= splitRequest[2]
                                else: 
                                        requestMethod = request

                        

                        codes = matched.group(4)
                        codes =codes.split(' ')


                        if (codes[0]!= '-'):
                                
                                rCode = int(codes[0])

                        if(codes[1]!='-'):
                                
                                rBytes = int(codes[1])




                        if (matched.group(5)!= '-'):
                                referrer = matched.group(5)

                        if(matched.group(6)!= '-'):
                                userAgent= matched.group(6)

                        newLog= Log(ip,date, requestMethod, requestResource, requestProtocol, rCode, rBytes, referrer, userAgent)
                        LogList.append(newLog)

        
        countries = {}
        for log in LogList:
                countryData = log.lookUpIp()

                if not countryData: break
                    
                name = countryData["country_name"] 
                code = countryData["country_code"]  
                #TODO: get country emoji and set up twitter API 
                if name in countries:
                        countries[name]+=1
                else:
                        countries[name]=1;


        print(countries)
        print(len(LogList))



if __name__=="__main__":
        main()

