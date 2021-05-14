from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
import os

from project import app, db
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.add_command('runserver', Server(host='0.0.0.0', port=8001 ,   threaded=True))
    manager.run()
