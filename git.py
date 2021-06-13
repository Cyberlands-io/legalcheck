import requests
from abc import ABC, abstractmethod
from colorama import Fore, Style
from parse import compile
import os
import re


class License():

    TEMPLATES_PATH = './templates'

    def __init__(self, name, permissions, conditions, limitations) -> None:
        self.name = name
        self.permissions = permissions
        self.conditions = conditions
        self.limitations = limitations
        self.get_max_len()

    @staticmethod
    def analize_license(path_to_license_file):
        
        pattern = r"[\n\t\s]*"
        for f in os.listdir(License.TEMPLATES_PATH):
            with open(f'{License.TEMPLATES_PATH}/{f}','r') as template:
                p = compile(re.sub(pattern, "",template.read()))
                with open(path_to_license_file,'r') as license_file:
                    l = re.sub(pattern, "", license_file.read())              
                    res = p.parse(l)
                    if res:
                        return GitHub.get_license_by_key(f[:-4])

            

    def print_license_data(self):
        print('\n{}{: >40}\n'.format(Style.BRIGHT + Fore.YELLOW, self.name))
        print(
            '{}{: >20} {}{: >20} {}{: >20}\n'.format(Style.BRIGHT + Fore.GREEN, 'Pemissions', Style.BRIGHT + Fore.BLUE,
                                                     'Conditions', Style.BRIGHT + Fore.RED, 'Limitations'))
        for index, _ in enumerate(getattr(self, self.max_len)):
            print("{}{: >20} {}{: >20} {}{: >20}".format(Style.BRIGHT + Fore.GREEN,
                                                         self.index_is_exists(self.permissions, index),
                                                         Style.BRIGHT + Fore.BLUE,
                                                         self.index_is_exists(self.conditions, index),
                                                         Style.BRIGHT + Fore.RED,
                                                         self.index_is_exists(self.limitations, index)))

    def get_max_len(self):
        self.max_len = max({'permissions': self.permissions, 'conditions': self.conditions,'limitations': self.limitations}.items(), key=len)[0]

    def index_is_exists(self, data, index):
        return data[index] if 0 <= index < len(data) else " "


class Repository(License):
    
    def __init__(self, rep_license=None, name='', owner='', url=''):
        self.name = name
        self.owner = owner
        self.url = url
        self.rep_license = rep_license

    @staticmethod
    def print_repository_data(repository):
        print('\n{}{}'.format(Style.BRIGHT + Fore.MAGENTA,repository.url if repository.url else repository.name))
        if repository.rep_license:
            repository.rep_license.print_license_data()
        else:
            print('\n{}{}'.format(Style.BRIGHT + Fore.YELLOW,'Private or None License!'))


# Gits

class Git(ABC):

    @abstractmethod
    def get_repository_license(self, repository_owner, repository_name):
        raise NotImplementedError


class GitHub(Git, Repository):

    def __init__(self, name, owner, url):
        repository_license = self.get_repository_license(owner, name)
        super().__init__(repository_license, name, owner, url)

    def get_repository_license(self, repository_owner, repository_name):

        response = requests.get(f'https://api.github.com/repos/{repository_owner}/{repository_name}/license', headers={"Authorization": "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"})
        if response.status_code == 200:
            license_resp = requests.get(response.json()['license']['url']).json() if response.json()['license']['url'] else None
            return License(license_resp['name'], license_resp['permissions'], license_resp['conditions'],license_resp['limitations']) if license_resp else None
        elif response.status_code == 404:
            return None
        else:
            print('{}{}'.format(Style.BRIGHT + Fore.RED, 'API rate limit!'))
            exit()

    @staticmethod
    def get_license_by_key(license_key):
        response = requests.get(f'https://api.github.com/licenses/{license_key}')
        if response.status_code == 200:
            data = response.json()
            return License(data['name'], data['permissions'], data['conditions'], data['limitations']) if data else None
        elif response.status_code == 404:
            return None
        else:
            print('{}{}'.format(Style.BRIGHT + Fore.RED,'API rate limit!'))
            exit()


class GitLab(Git, Repository):

    def __init__(self, name, owner, url):
        repository_license = self.get_repository_license(owner, name)
        super().__init__(repository_license, name, owner, url)

    def get_repository_license(self, repository_owner, repository_name):

        response = requests.get(f'https://gitlab.com/api/v4/projects/{repository_owner}%2F{repository_name}', params={'license': True})
        if response.status_code == 200:
            license_resp = requests.get(f'https://gitlab.com/api/v4/licenses/{response.json()["license"]["key"]}').json() if response.json()['license'] else None
            return License(license_resp['name'], license_resp['permissions'], license_resp['conditions'], license_resp['limitations']) if license_resp else None
        elif response.status_code == 404:
            return None
        else:
            print('{}{}'.format(Style.BRIGHT + Fore.RED, 'API rate limit!'))
            exit()
