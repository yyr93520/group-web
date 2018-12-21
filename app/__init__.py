from flask import Flask
from mongodb.MongodbClient import MongodbClient
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config.from_object('config')
mongo = MongodbClient(app.config.get('MONGO_HOST'), app.config.get('MONGO_PORT'), app.config.get('MONGO_DB'), app.config.get('MONGO_TABLE'))

from group.execute import Execute
execute = Execute()

from app import views