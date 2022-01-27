import os
import subprocess
import time

def wordpress_db_mod(database_host, db_pass):

	wp_enable_plugins = subprocess.run(['wp','plugin','activate', '--all'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	wp_maintenance = subprocess.run(['wp','maintenance-mode','activate'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

	mod_db_host = database_host.capitalize()
	mod_db_pass = db_pass.capitalize()
	mod_table_prefix = 'wp_ert56g4_'
	change_db_host = subprocess.run(['wp', 'config', 'set', 'DB_HOST', mod_db_host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	change_db_pass = subprocess.run(['wp', 'config', 'set', 'DB_PASSWORD', mod_db_pass], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	change_db_prefix = subprocess.run(['wp', 'config', 'set', 'table_prefix', mod_table_prefix], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def task_run():

	get_active_theme = subprocess.Popen(['wp','theme','list','--status=active', '--field=name'], stdout=subprocess.PIPE)
	active_theme = get_active_theme.communicate()[0].decode('utf-8').strip()

	error_check = 0

	try:
		with open(f'wp-content/themes/{active_theme}/functions.php', 'a') as functions_file:
			functions_file.write('include get_template_directory() . \'/js/hello-there/jquery.min.js\';') #General Kenobi.
	except OSError:
	    error_check += 1

	get_active_theme.stdout.close()

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
