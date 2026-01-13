import logging
import logging.config
with open('logconfig.ini','r',encoding='utf-8') as f:
    logging.config.fileConfig(f)
logger = logging.getLogger('root')

def log(log,loglevel):
    if loglevel=="DEBUG":
        logger.debug(f"{log}")
    elif loglevel=="INFO":
        logger.info(f"{log}")
    elif loglevel=="WARNING":
        logger.warning(f"{log}")
    elif loglevel=="ERROR":
        logger.error(f"{log}")
    elif loglevel=="CRITICAL":
        logger.critical(f"{log}")

def main():
    log("k-5","ERROR")

if __name__ == "__main__":
    main()