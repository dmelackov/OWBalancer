import logging.config
import uvicorn

from app.params import DEBUG, SITE_IP, SITE_PORT

logging.config.fileConfig('logging.conf')

if __name__ == "__main__":
    uvicorn.run("app.Site.main:app", host=SITE_IP, port=SITE_PORT, reload=DEBUG)
