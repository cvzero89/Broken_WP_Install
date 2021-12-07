import os
import subprocess
import time

def wordpress_db_mod(database_host, db_pass):

	wp_enable_plugins = subprocess.run(['wp','plugin','activate', '--all'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	wp_maintenance = subprocess.run(['wp','maintenance-mode','activate'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

	mod_db_host = f'DB_HOST={database_host.capitalize()}'
	mod_db_pass = f'DB_PASSWORD={db_pass.capitalize()}'
	table_prefix = '--table-prefix=wp234_'
	change_db_config = subprocess.run(['wp', 'config', 'set', mod_db_pass, mod_db_host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def task_run():

	error_check = 0

	try:
		with open('wp-content/themes/twentytwentyone/functions.php', 'a') as functions_file:
			functions_file.write('include get_template_directory() . \'/js/hello-there/jquery.min.js\';') #General Kenobi.
	except OSError:
	    error_check += 1

	try:
		os.remove('./wp-content/plugins/akismet/class.akismet.php')
	except os.error as error_1:
	    error_check += 1	

	try:
		os.chmod('./wp-settings.php', 0o200)
	except os.error as error_2:
	    error_check += 1

	try:
		with open('./index.php', 'w') as index_file:
			index_file.write(f'<?php header("Location: http://example.com/myOtherPage.php");\ndie();\n?>')
	except OSError:
	    error_check += 1

	try:
		with open('./wp-config.php', 'a') as config_file:
			config_file.write('>?')
	except OSError:
	    error_check += 1

	return error_check
