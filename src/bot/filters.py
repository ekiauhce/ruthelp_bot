from telegram.ext import Filters

import database

author = Filters.user(377064896)
admins = Filters.user(database.get_admins())
