from utils.dbconfig import dbconfig
import utils.aesutil
from getpass import getpass

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import base64

from rich import print as printc
from rich.console import Console

def computeMasterKey(mp, sv):

	#encodes master password and secret value
	password = mp.encode()
	salt = sv.encode()

	#creates master key using pbkdf2 function
	key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
	return key


def checkEntry(site_name, site_url, email, username):
	db = dbconfig()
	cursor = db.cursor()
	query = f"SELECT * FROM password_manager.entries WHERE site_name = '{site_name}' AND site_url = '{site_url}' AND email = '{email}' AND username = '{username}'"
	cursor.execute(query)
	results = cursor.fetchall()

	if len(results) != 0:
		return True
	return False


def addEntry(mp, sv , site_name, site_url, email, username):
	# checks to see if the given entry is already in the database
	if checkEntry(site_name, site_url, email, username):
		printc("[yellow][-][/yellow] Entry with these details already exists")
		return

	# gets password from user for the account they are adding
	password = getpass("What is the password for the account you are adding?: ")

	# compute master key
	mk = computeMasterKey(mp, sv)

	# encrypt password with mk
	encrypted = utils.aesutil.encrypt(key=mk, source=password, keyType="bytes")

	# adds given entries into password manager
	db = dbconfig()
	cursor = db.cursor()
	query = "INSERT INTO password_manager.entries (site_name, site_url, email, username, password) values (%s, %s, %s, %s, %s)"
	val = (site_name, site_url, email, username, encrypted)
	cursor.execute(query, val)
	db.commit()

	printc("[green][+][/green] Added entry ")
