# manage.py

from flask_script import Manager

from app.server.instance import server

manager = Manager(server.get_app())

@manager.command
def reset():
    
    from app.models import reset

    reset()

if __name__ == "__main__":
    manager.run()