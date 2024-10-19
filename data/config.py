import os

from decouple import config

BOT_TOKEN = config('BOT_TOKEN')
# id admin
ADMIN_ID = config("ADMINS_ID").split(',')
# IP = config("IP_ADDRESS")
DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")
DB_NAME = config("DB_NAME")
DB_HOST = config("DB_HOST")
DB_PORT = config("PORT")
WB_EMPLOYEE_ID = config("WB_EMPLOYEE_ID")
WB_PASSWORD = config("WB_PASSWORD")

SECRET_KEY = config("SECRET_KEY")
PASSPORT_URL = config("PASSPORT_URL")
