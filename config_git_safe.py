from . app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config["MYSQL_DATABASE_USER"] = 'NAME_USER'
app.config["MYSQL_DATABASE_PASSWORD"] = 'PASSWORD_USER'
app.config["MYSQL_DATABASE_DB"] = 'NAME_DATABASE'
app.config["MYSQL_DATABASE_HOST"] = 'NAME_HOST'
mysql.init_app(app)


