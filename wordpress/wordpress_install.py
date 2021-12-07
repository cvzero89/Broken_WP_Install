import subprocess
import getpass
import time
#WordPress Install Module
def get_info():

	site_name = input('Enter the site name:')
	database_name = input('Enter the database name:')
	user_name = input('Enter the user name:')
	database_host = input('Enter the database hostname:')
	db_pass = getpass.getpass('Enter the database password')
	return site_name, database_name, user_name, database_host, db_pass


def wp_setup(site_name, database_name, user_name, database_host, db_pass):

	#Installing WordPress:
	print('Downloading latest WordPress')
	download_wp = subprocess.Popen(['wp', 'core', 'download', '--force'], stdout=None)
	time.sleep(5)

	#Set up config:
	database_name_config = f'--dbname={database_name}'
	user_name_config = f'--dbuser={user_name}'
	db_host_config = f'--dbhost={database_host}'
	db_pass_config = f'--dbpass={db_pass}'
	config_wp = subprocess.Popen(['wp', 'config', 'create', database_name_config, user_name_config, db_host_config, db_pass_config], stdout=None)
	time.sleep(7)

	set_url = f'--url={site_name}'
	install_wp = subprocess.Popen(['wp', 'core', 'install', set_url, '--title=WPS Broken Site', '--admin_user=cvzero89', '--admin_email=cvjoe89@gmail.com'], stdout=None)
	time.sleep(7)
