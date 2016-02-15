#TODO: Automated way to create Postgres databases from scratch
#TODO: Automate running migration on the newly created databases
#TODO: Auto populate static data in the databases
#TODO: Finish implementing animal groups
from app import app
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000)
