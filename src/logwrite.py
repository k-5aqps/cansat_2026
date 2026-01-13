import logging
import logging.config

class MyLogging():
    def __init__(self):
        with open('logconfig.ini','r',encoding='utf-8') as f:
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

def main():
    log=MyLogging()
    log.write("k-5","ERROR")

if __name__ == "__main__":
    main()