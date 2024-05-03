# Simple password manager


**Must have python3 installed**
## Installation Commands

```
sudo apt install python3-pip
pip install -r requirements.txt
```

## To install mariadb
```
sudo apt-get update
sudo apt-get install mariadb-server
```

## Once DB is installed must log into DB to create user

### 1. Login to mysql as root

```
sudo mysql -u root
```
### 2. Create USer

```
CREATE USER 'pm'@localhost IDENTIFIED BY 'password';
```
### 3. Grant privileges
```
GRANT ALL PRIVILEGES ON *.* TO 'pm'@localhost IDENTIFIED BY 'password';
```


## Control flow of program

1. User will run the config.py to create a master pasword and create a secret value that will be used as a salt
2. User will then use the pm.py to add or retrive passwords from the database

## Runtime commands

## Configure database (password_manager database must not exist)
# If database exists can use "drop database password_manager;" to reset it

```
python3 config.py
```

## Available arguments
```
-n -> Site name
-u -> Site URL
-e -> Email Address
-l -> login user name
-c -> Copy password
```
## Add entry
# Adds Bob's google account to the database 
Will then prompt to enter the master password and password for the account they would like to add to the database
```
python3 pm.py add -n Google -u www.google.com -e example@gmail.com -l Bob
```

## Retrieve entry

### To retrieve all added accounts

```
python3 pm.py extract
```

### To retrieve a specifc accont can use -n "Name"

```
python3 pm.py extract -n Google
```

### To copy the password of a specific account to the clipboard use -n "Name" and -c

```
python3 pm.py extract -n Google -c
```
