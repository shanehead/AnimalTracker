from app import app

@app.route('/')
def index():
	return 'Animal Tracker'

@app.route('/login')
def login():
	return 'Login'
