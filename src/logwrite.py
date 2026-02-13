import logging
import logging.config
import csv
import datetime


class MyLogging():
    def __init__(self):
        with open('../config/logconfig.ini','r',encoding='utf-8') as f:
            logging.config.fileConfig(f)
        self.logger = logging.getLogger('root')

    def write(self,log,loglevel):
        if loglevel=="DEBUG":
            self.logger.debug(f"{log}")
        elif loglevel=="INFO":
            self.logger.info(f"{log}")
        elif loglevel=="WARNING":
            self.logger.warning(f"{log}")
        elif loglevel=="ERROR":
            self.logger.error(f"{log}")
        elif loglevel=="CRITICAL":
            self.logger.critical(f"{log}")

    def init():
        with open("../log/gpslog.csv","w") as f:
            pass
        with open("../log/degree.csv","w") as f:
            pass

    def forCSV(self,lat,lon):
        with open("../log/gpslog.csv","a") as f:
            wrt = csv.writer(f)
            wrt.writerow([datetime.datetime.now(),lat,lon])
    def forLATLON(self,temp1,temp2):
        with open("../log/degree.csv","a") as f:
            wrt = csv.writer(f)
            wrt.writerow([datetime.datetime.now(),temp1,temp2])

def main():
    log=MyLogging()
    log.write("k-5","ERROR")

if __name__ == "__main__":
    main()