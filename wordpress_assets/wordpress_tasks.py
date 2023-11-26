import os
import random
import string
import shutil
from zipfile import ZipFile 

def generate_random_sequence(length=6, interpolate=''):
    """
    Generates a random sequence of letters and numbers, optionally interpolating it with a provided string.

    :param length: Length of the random sequence to be generated, default is 6.
    :param interpolate: A string to be interleaved with the random sequence.
    :return: A string containing the interleaved sequence.
    """
    random_sequence = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    if interpolate:
        # Interleave the random sequence with the provided string
        combined_sequence = ''.join(r + i for r, i in zip(random_sequence, interpolate))
        # Add any remaining characters from the longer string
        combined_sequence += random_sequence[len(interpolate):] if len(random_sequence) > len(interpolate) else interpolate[len(random_sequence):]
        return combined_sequence
    else:
        return random_sequence


def random_post(site):
	get_random_list = site.run_command([
		'wp', 'post', 'list', 
		'--post_type=page', 
		'--format=ids'])
	if get_random_list:
		page_ids = [id_str for id_str in get_random_list.split() if id_str != site.page_id]
	if page_ids:
		random_page_id = random.choice(page_ids)
		site.run_command(['wp', 'option', 'update', 'page_on_front', random_page_id])

def wordpress_db_mod(site):

	mod_db_host = 'mysql' + generate_random_sequence(3) + '.' + site.site_name
	mod_db_pass = generate_random_sequence(3, site.db_pass)
	mod_table_prefix = 'wp_' + generate_random_sequence(6)
	site.run_command(['wp', 'config', 'set', 'DB_HOST', mod_db_host])
	site.run_command(['wp', 'config', 'set', 'DB_PASSWORD', mod_db_pass])
	site.run_command(['wp', 'config', 'set', 'table_prefix', mod_table_prefix])


def task_run(site, start_path):

	site.run_command(['wp', 'plugin', 'activate', '--all'])
	site.run_command(['wp', 'maintenance-mode', 'activate'])

	get_active_theme = ['wp','theme','list','--status=active', '--field=name']
	active_theme = site.run_command(get_active_theme)
	random_post(site)
	error_check = 0

	try:
		random_name = generate_random_sequence(4, site.site_name)
		site.run_command(['wp', 'option', 'set', 'siteurl', random_name])
		site.run_command(['wp', 'option', 'set', 'home', random_name])
		site.run_command(['wp', 'search-replace', f'https://{site.site_name}', f'https://{random_name}'])
	except:
		print('Error at search-replace.')
		error_check += 1

	try:
		wordpress_db_mod(site)
	except:
		print('Error at WP_DB_MOD')
		error_check += 1

	try:
		theme_path = f'./wp-content/themes/{active_theme}'
		with open(f'{theme_path}/functions.php', 'a') as functions_file:
			functions_file.write('include get_template_directory() . \'/js/hello-there/jquery.min.js\';\n') #General Kenobi.
			functions_file.write('add_action( "init", "my_custom_function" );')
	except OSError:
		print('Error at theme.')
		error_check += 1
	
	try:
		if os.path.exists(f'{theme_path}/theme.json'):
			shutil.copy(f'{start_path}/wordpress_assets/wp.json', f'{theme_path}/')
			os.rename(f'{theme_path}/theme.json', f'{theme_path}/cvzero89.json')
			os.rename(f'{theme_path}/wp.json', f'{theme_path}/theme.json')
		elif os.path.exists(f'{theme_path}/style.css'):
			shutil.copy(f'{start_path}/wordpress_assets/wp.css', f'{theme_path}/')
			os.rename(f'{theme_path}/style.css', f'{theme_path}/cvzero89.css')
			os.rename(f'{theme_path}/wp.css', f'{theme_path}/style.css')			
	except Exception as e:
		print(e)
		
	try:
		os.remove('./wp-content/plugins/akismet/class.akismet.php')
	except os.error as error_1:
		print('Error at akismet.')
		error_check += 1	

	try:
		os.chmod('./wp-settings.php', 0o200)
	except os.error as error_2:
		print('Error at wp-settings')
		error_check += 1

	try:
		with open('./index.php', 'w') as index_file:
			index_file.write(f'<?php header("Location: http://example.com/myOtherPage.php");\ndie();\n?>')
	except OSError:
		print('Error at index.')
		error_check += 1

	try:
		with open('./wp-config.php', 'a') as config_file:
			config_file.write('>?')
	except OSError:
		print('Error at wp-config.')
		error_check += 1

	return error_check

## - Moving a dummy WP-CLI to be used on the exercise. If --reset is used then it will remove it and delete the alias from .bashrc.
def move_payload(start_path, mode):
	home_dir = os.path.expanduser('~')
	user = home_dir.split('/')[2]
	fake_wp_cli_path = f'{home_dir}/.wp-dummy/wp-dummy'
	alias = f'alias wp="{fake_wp_cli_path}"'
	bash_path = f'{home_dir}/.bashrc'
	if user == 'root':
		exit()
	if mode == 'installer':
		try:
			os.mkdir(f'{home_dir}/.wp-dummy/')
		except OSError as error:
			...
		assets_path = f'{start_path}/wordpress_assets'
		with ZipFile(f'{assets_path}/wp-dummy.zip', 'r') as zObject:
			zObject.extractall(f'{assets_path}/')
		if not os.path.exists(fake_wp_cli_path):
			shutil.copy(f'{assets_path}/wp-dummy', f'{home_dir}/.wp-dummy/')
		os.chmod(f'{home_dir}/.wp-dummy/wp-dummy', 0o740)
		
		## - True if alias is already on the file.
		def check_file(alias, bash_path):
			with open(bash_path, 'r') as read_file:
				for line in read_file:
					if alias in line:
						return True
			return False
		## - Only modifying the file if it is needed.
		if check_file(alias, bash_path) == False:
			with open(bash_path, 'a') as bash_file:
				bash_file.write(f'{alias}\n')
	elif mode == 'reset':
		print('Resetting changes to files...')
		# Read the file and store lines
		with open(bash_path, 'r') as file:
			lines = file.readlines()

		# Remove the line with the specified content
		lines = [line for line in lines if alias not in line]

		# Write the modified lines back to the file
		with open(bash_path, 'w') as file:
			file.writelines(lines)
			
		try:
			shutil.rmtree(f'{home_dir}/.wp-dummy/')
		except Exception as e:
			print(e)
		print('Done.')
