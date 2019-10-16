import os
import subprocess

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from app import create_app, db

app = create_app(os.getenv('NARWHAL_ENV') or 'dev')
manager = Manager(app)
migrate = Migrate(app, db)
server = Server(host="0.0.0.0", port=65502)


manager.add_command('runserver', server)

manager.add_command('db', MigrateCommand)


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def format():
    """Runs the yapf and isort formatters over the project."""
    isort = 'isort -rc *.py app/'
    yapf = 'yapf -r -i *.py app/'

    print('Running {}'.format(isort))
    subprocess.call(isort, shell=True)

    print('Running {}'.format(yapf))
    subprocess.call(yapf, shell=True)


if __name__ == '__main__':
    manager.run()
