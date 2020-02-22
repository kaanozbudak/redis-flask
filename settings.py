# ###################################
#       PROJECT CONFIGURATIONS      #
# ###################################
import os

# APPLICATION

APP_HOST = "0.0.0.0"
APP_PORT = 5000
DEBUG = True

# REDIS
# This condition can be removed when using environment variables
if os.getenv("MODE") == "DOCKER":
    REDIS_HOST = "redis"
else:
    REDIS_HOST = '0.0.0.0'

REDIS_PORT = 6379
REDIS_DB = 0
