sudo apt install python3-pip
pip install -r requirements.txt


sudo apt-get update
sudo apt-get install mariadb-server

Login to mysql as root
sudo mysql -u root

Create User
CREATE USER 'pm'@localhost IDENTIFIED BY 'password';

Grant privileges

GRANT ALL PRIVILEGES ON *.* TO 'pm'@localhost IDENTIFIED BY 'password';
