import os
import sys
import subprocess
import time
from wordpress.wordpress_install import get_info, wp_setup
from wordpress.wordpress_tasks import wordpress_db_mod, task_run
import requests

checking_version = f'{sys.version_info.major}.{sys.version_info.minor}'

if checking_version == '3.6' or checking_version > '3.5.9' :
    print(f'Running Python version is {checking_version}')
else:
    print(f'This script will not work on Python {checking_version}, please update before running')
    exit()

print('============================================\nWordPress Install Script\n============================================')

site_name, database_name, user_name, database_host, db_pass = get_info()

## Needs MySQL module:
#try:

#    cnx = mysql.connector.connect(user=user_name, password=db_pass, host=database_host, database=database_name)

#except mysql.connector.Error as err:
#  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#    print("Something is wrong with your user name or password")
#  elif err.errno == errorcode.ER_BAD_DB_ERROR:
#    print("Database does not exist")
#  else:
#    print(err)
#else:
#  cnx.close()

print(f'Installing latest WordPress on {site_name}, the database is {database_name}, user {user_name} with the password provided above')
checks = False
while checks == False:
    input_check = input("Is the information correct?: [Y/N]")
    if input_check.upper() == "N":
        print("Let's try this again")
        get_info()
    elif input_check.upper() == "Y":
        print("All good!")
        checks = True
    elif input_check.upper != "Y" and input_check.upper != "N":
        print("Bad input. I can only accept Y or N. To cancel the script use Ctrl + C")
        get_info()


if os.path.isfile('./wp-config-sample.php') == False:
	wp_setup(site_name, database_name, user_name, database_host, db_pass)
else:
	print('Skipping setup')

#Is WordPress Working?
try:
	ping_to_wordpress = requests.get(f'http://{site_name}', timeout = 30)
	ping_to_wordpress.raise_for_status()
	print(f'The site reports a {ping_to_wordpress.status_code} HTTP code')
except:
	print(f'HTTP Error/Timeout, {site_name} might not be working OK. Do we need to re-run setup?')
checks = False
while checks == False:
    input_check = input(f'Go to http://{site_name}, can you see the site?: [Y/N]')
    if input_check.upper() == "N":
        print("Let's try this again\n Running setup:")
        wp_setup(site_name, database_name, user_name, database_host, db_pass)
    elif input_check.upper() == "Y":
        print("Okay, time to break it! The goal is to get it to load as before.")
        checks = True
        time.sleep(5)
    elif input_check.upper != "Y" and input_check.upper != "N":
        print("Bad input. I can only accept Y or N. To cancel the script use Ctrl + C")
        wp_setup(site_name, database_name, user_name, database_host, db_pass)

wordpress_db_mod(database_host, db_pass)

error_check_1 = task_run()

if error_check_1 >= 1:
	print('There were some errors during the setup. DM @carlosv over Slack ')
else:
	print('Done. Start working. Any questions DM @carlosv over Slack ')
