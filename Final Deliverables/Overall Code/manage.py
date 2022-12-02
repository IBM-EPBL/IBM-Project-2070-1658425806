from app import create_app,db
from models import User

def deploy():
	app = create_app()
	app.app_context().push()
	db.create_all()
	
deploy()

