#!/usr/bin/env python

import argparse
from getpass import getpass
import hashlib
import pyperclip

from rich import print as printc

import utils.add
import utils.retrieve
from utils.dbconfig import dbconfig

parser = argparse.ArgumentParser(description='Description')

parser.add_argument('option', nargs='?', help='You can either add or extract passwords')
parser.add_argument("-n", "--name", help="Site name")
parser.add_argument("-u", "--url", help="Site URL")
parser.add_argument("-e", "--email", help="Email")
parser.add_argument("-l", "--login", help="Username")
parser.add_argument("-c", "--copy", action='store_true', help='Copy password to clipboard')


args = parser.parse_args()


def inputAndValidateMasterPassword():
	mp = getpass("MASTER PASSWORD: ")
	hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

	db = dbconfig()
	cursor = db.cursor()
	query = "SELECT * FROM password_manager.secrets"
	cursor.execute(query)
	result = cursor.fetchall()[0]
	
	#compares hashed master password to the one in the database
	if hashed_mp != result[0]:
		printc("[red][!] WRONG! [/red]")
		return None

	return [mp, result[1]]


def main():

	if args.option is None:
		printc("[red][!] Missings arguments --- You can choose to either add or extract information [/red] ")
        
	if args.option in ["add"]:
		if args.name == None or args.url == None or args.login == None:
			printc("[red][!][/red] Missing arguments")
			return

		if args.email == None:
			args.email = ""

		#validates master password
		res = inputAndValidateMasterPassword()

		#if password is successfully validated
		if res is not None:
			#res[0] is master password res[1] secret value
			utils.add.addEntry(res[0], res[1], args.name, args.url, args.email, args.login)

	if args.option in ["extract"]:
	
		res = inputAndValidateMasterPassword()

		search = {}
		if args.name is not None:
			search["site_name"] = args.name
		if args.url is not None:
			search["site_url"] = args.url

		#if inputed password is same as master password user can view the account information
		if res is not None:
			#passes master password and device secret
			utils.retrieve.retrieveEntries(res[0], res[1], search, decryptPassword = args.copy)

main()