import os
import sys
import string
import random
import hashlib
import sys
from getpass import getpass

from utils.dbconfig import dbconfig

from rich import print as printc
from rich.console import Console

console = Console()

#creates secret value
def generateSecretValue():
	length = 10
	#combines random uppercase letters and numbers to make a secret value with length k
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))

#creates config file
def makeConfig():

	printc("[green] Creating a new config [/green] ")

	# Create database
	db = dbconfig()
	cursor = db.cursor()
	try:
		cursor.execute("CREATE DATABASE password_manager")
	except Exception as e:
		printc("[red] Something went wrong!")
		console.print_exception(show_locals=True)
		sys.exit(0)

	printc("[green][+][/green] A database called 'password_manager' was created")

	# Create tables
	query = "CREATE TABLE password_manager.secrets (master_password_hash TEXT NOT NULL, secret_value TEXT NOT NULL)"
	res = cursor.execute(query)
	printc("[green][+][/green] Table 'secrets' created ")

	query = "CREATE TABLE password_manager.entries (site_name TEXT NOT NULL, site_url TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
	res = cursor.execute(query)
	printc("[green][+][/green] Table 'entries' created ")


	mp = ""
	printc("[yellow][+] You will now create a master password, this will give you access to all your other passwords [/yellow]\n")

	while 1:
		mp = getpass("Choose a MASTER PASSWORD: ")
		if mp == getpass("Re-type: ") and mp!="":
			break
		printc("[yellow][-] Please try again.[/yellow]")

	# Hash the MASTER PASSWORD
	hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
	printc("[green][+][/green] Generated hash of MASTER PASSWORD")


	# Generate a device secret
	ds = generateSecretValue()
	printc("[green][+][/green] Device Secret generated")

	# Add them to db
	query = "INSERT INTO password_manager.secrets (master_password_hash, secret_value) values (%s, %s)"
	val = (hashed_mp, ds)
	cursor.execute(query, val)
	db.commit()

	printc("[green][+][/green] Added to the database")

	printc("[green][+] Configuration done![/green]")

	db.close()

if __name__ == "__main__":

	makeConfig()
