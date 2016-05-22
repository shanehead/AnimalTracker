from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from config import DevConfig
from app import app, db
app.config.from_object(DevConfig)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # init - First initialization
    # migrate - Get latest model updates
    # upgrade - Perform the upgrade
    manager.run()
