import os
from time import sleep
from zipfile import ZipFile

import requests


class Update():
    def __init__(self):
        self.version = '1.5.5'
        self.github = 'https://google.com'
        self.zipfile = 'https://google.com'
        self.update_checker()

    def update_checker(self):
        code = requests.get(self.github).text
        if "self.version = '1.5.5'" in code:
            print('This version is up to date!')
            print('Exiting...')
            sleep(2)
            exit()
        else:
            print('''
                    ███╗   ██╗███████╗██╗    ██╗    ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗██╗
                    ████╗  ██║██╔════╝██║    ██║    ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║
                    ██╔██╗ ██║█████╗  ██║ █╗ ██║    ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  ██║
                    ██║╚██╗██║██╔══╝  ██║███╗██║    ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  ╚═╝
                    ██║ ╚████║███████╗╚███╔███╔╝    ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗██╗
                    ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝      ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝
                                      Invalid Github''')
            choice = input('\nThe Github link is no longer available? (y/n): ')
            if choice.lower() == 'y':
                print('Exiting...')
                sleep(2)
                exit()
            if choice.lower() == 'n':
                print('Exiting...')
                sleep(2)
                exit()


if __name__ == '__main__':
    Update()
