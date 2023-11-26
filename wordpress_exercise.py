import os
import time
from wordpress_assets.wordpress_install import WordPress_Site
from wordpress_assets.wordpress_tasks import task_run, move_payload
import requests
import argparse

def install(site):
    start = 'WPS Test #1'
    print(f'{start:~^40}')
    print(f'Installing latest WordPress on {site.site_name}, the database is {site.database_name}, user {site.user_name} with the password provided above')
    checks = False
    while checks == False:
        input_check = input("Is the information correct?: [Y/N] ")
        if input_check.upper() == "N":
            print("Let's try this again")
            site.get_info()
        elif input_check.upper() == "Y":
            print("All good!")
            checks = True
        elif input_check.upper != "Y" and input_check.upper != "N":
            print("Bad input. I can only accept Y or N. To cancel the script use Ctrl + C")
            site.get_info()

    site.wp_install()
    site_title = '\"WPS Custom Page.\"'
    site_post = '\"Hey! Look at me I am a page! Please help me get to this state once I am broken.\"'
    site.create_wp_post(site_title, site_post)

    """
    Checking if the site is reachable. If not the setup will run again in an infinite loop.
    HTTP is used instead of HTTPS in case SSL is not set. If SSL is set the redirect should still work.
    """
    try:
        ping_to_wordpress = requests.get(f'http://{site.site_name}/?nocache=1', timeout = 30)
        ping_to_wordpress.raise_for_status()
        print(f'The site reports a {ping_to_wordpress.status_code} HTTP code')
    except:
        print(f'HTTP Error/Timeout, {site.site_name} might not be working OK. Do we need to re-run setup?')

    checks = False
    while checks == False:
        input_check = input(f'Go to http://{site.site_name}/?nocache=1, can you see the site? (If so, take a screenshot for reference): [Y/N] ')
        if input_check.upper() == "N":
            print("Let's try this again\n Running setup...")
            site.wp_install()
            site.create_wp_post(site_title, site_post)
        elif input_check.upper() == "Y":
            print("Okay, time to break it! The goal is to get it to load as before. Use your screenshot as a guide.")
            checks = True
            time.sleep(5)
        elif input_check.upper != "Y" and input_check.upper != "N":
            print("Bad input. I can only accept Y or N. To cancel the script use Ctrl + C")
            site.wp_install()
            site.create_wp_post(site_title, site_post)
    
    



def main():
    parser =  argparse.ArgumentParser(description='Setting up WP for training exercises.')
    parser.add_argument('--installer', help='Installs and sets up WP.', action='store_true')
    parser.add_argument('--reset', help='Resets the environment.', action='store_true')
    args = parser.parse_args()
    installer = args.installer
    reset = args.reset
    """
    start_path is needed to reference the assets to call the move_payload() function.
    It fixes the problem that may arise if the script is not executed on the root directory.
    """
    start_path = os.getcwd()
    if installer:
        site = WordPress_Site()
        site.folder_check()
        site.get_info()
        install(site)
        error_check = task_run(site, start_path)

        """
        Only move to the final part if there has not been any exception thrown in task_run().
        If error_check is equal or more than 1 means something is not running as supposed to.
        """

        if error_check >= 1:
            print('There were some errors during the setup. DM @carlosv over Slack ')
        else:
            move_payload(start_path, 'installer')
            print('Done. Start working. Any questions DM @carlosv over Slack ')
    elif reset:
        move_payload(start_path, 'reset')
    else:
        print('No argument provided: Use --installer or --reset. For more info use -h.')


if __name__ == "__main__":
    main()
