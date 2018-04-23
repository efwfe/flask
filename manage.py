# _*_coding:utf-8_*_

from flask_migrate import Migrate,MigrateCommand,Manager
from app import create_app,db
from app.models import User, Role

app = create_app('develop')



manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(db=db,User=User,Role=Role)

if __name__ == '__main__':
    print(app.url_map)
    manager.run()