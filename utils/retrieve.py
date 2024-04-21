from utils.dbconfig import dbconfig
import utils.aesutil
import pyperclip

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import base64

from rich import print as printc
from rich.console import Console
from rich.table import Table

def computeMasterKey(mp, sv):
	password = mp.encode() 
	salt = sv.encode()
	key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
	return key

def retrieveEntries(mp, sv, search, decryptPassword = False):
	db = dbconfig()
	cursor = db.cursor()

	query = ""
	if len(search) == 0:
		query = "SELECT * FROM password_manager.entries"
	else:
		query = "SELECT * FROM password_manager.entries WHERE "
		
		#loops through search terms given by user and adds it to query
		for i in search:
			query += f"{i} = '{search[i]}' AND "

		#gets rid of the additinoal ' AND ' at end of query
		query = query[:-5]

	cursor.execute(query)

	#gets results of search query in a list
	results = cursor.fetchall()

	if len(results) == 0:
		printc("[yellow][-][/yellow] No results for the search")
		return

	# if user wants to view password but query gives multiple results we will not copy password to clipboard
	if (decryptPassword and len(results) > 1) or (not decryptPassword):
		
		#creates table schema
		table = Table(title="Results")
		table.add_column("Site Name")
		table.add_column("URL",)
		table.add_column("Email")
		table.add_column("Username")
		table.add_column("Password")

		#contructs table entry
		for i in results:
			table.add_row(i[0], i[1], i[2], i[3], "{hidden}")

		console = Console()
		console.print(table)
		return 

	if decryptPassword and len(results) == 1:
		# Compute master key
		mk = computeMasterKey(mp, sv)

		# decrypt password
		decrypted = utils.aesutil.decrypt(key=mk, source=results[0][4], keyType="bytes")

		printc("[green][+][/green] Password copied to clipboard")
		pyperclip.copy(decrypted.decode())

	db.close()