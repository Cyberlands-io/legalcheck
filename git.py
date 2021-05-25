import requests
from abc import ABC, abstractmethod
from colorama import Fore, Style

class License():

    def __init__(self, name, permissions, conditions, limitations) -> None:
        self.name = name
        self.permissions = permissions
        self.conditions = conditions
        self.limitations = limitations
        self.get_max_len()
    
    licenses = { 
                 "apache-2.0" : "Apache",
                 "bsd-2-clause" : "BSD 2-Clause",
                 "bsd-3-clause" : "BSD 3-Clause",
                 "bsl-1.0" : "Boost Software",
                 "cc0-1.0" : "Creative Commons Legal Code",
                 "epl-2.0" : "Eclipse Public",
                 "gpl-3.0" : "GNU GENERAL PUBLIC",
                 "agpl-3.0" : "GNU AFFERO GENERAL",
                 "lgpl-2.1" : "GNU LESSER GENERAL PUBLIC",
                 "mit" : "MIT",
                 "mpl-2.0" : "Mozilla Public",
                 "unlicense" : "free and unencumbered software released"
                 }

    @staticmethod
    def compare_license(path_to_license_file):
        with open(path_to_license_file) as f:
            datafile = f.read()
            for key, value in License.licenses.items():
                if value.lower() in datafile.lower():
                    return GitHub.get_license_by_key(key)

    def print_license_data(self):
        print('\n{}{: >40}\n'.format(Style.BRIGHT + Fore.YELLOW,self.name))
        print('{}{: >20} {}{: >20} {}{: >20}\n'.format(Style.BRIGHT + Fore.GREEN,'Pemissions',Style.BRIGHT + Fore.BLUE,'Conditions',Style.BRIGHT + Fore.RED,'Limitations'))
        for index, _ in enumerate(getattr(self, self.max_len)):
            print("{}{: >20} {}{: >20} {}{: >20}".format(Style.BRIGHT + Fore.GREEN,self.index_is_exists(self.permissions,index),Style.BRIGHT + Fore.BLUE,self.index_is_exists(self.conditions,index),Style.BRIGHT + Fore.RED,self.index_is_exists(self.limitations,index)))

    def get_max_len(self):
        self.max_len = max({'permissions':self.permissions,'conditions':self.conditions,'limitations':self.limitations}.items(), key = len)[0]
   
    def index_is_exists(self, data, index):
        return data[index] if 0 <= index < len(data) else " "
    
    

class Repository(License):
    

    def __init__(self, rep_license=None, name='', owner='', url='') -> None:
        self.name = name
        self.owner = owner
        self.url = url
        self.rep_license = rep_license

    def print_license_data(self, rep):
        print('\n{}{}'.format(Style.BRIGHT + Fore.MAGENTA,self.url if self.url else self.name))
        if rep.rep_license:
            rep.rep_license.print_license_data()
        else:
            print('\n{}{}'.format(Style.BRIGHT + Fore.YELLOW,'Private or None License!'))

class Git(ABC):
 
    @abstractmethod
    def get_repository_license(self, repository_owner, repository_name):
        raise NotImplementedError


class GitHub(Git, Repository):

    def get_repository_license(self, repository_owner, repository_name):
        response = requests.get(f'https://api.github.com/repos/{repository_owner}/{repository_name}/license', headers={"Authorization" : "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"})
        if response.status_code == 200:
            license_resp = requests.get(response.json()['license']['url']).json() if response.json()['license']['url'] else None
            return License(license_resp['name'], license_resp['permissions'],license_resp['conditions'],license_resp['limitations']) if license_resp else None
        elif response.status_code == 404:
            return None
        else:
            print('{}{}'.format(Style.BRIGHT + Fore.RED,'API rate limit!'))
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

    def get_repository_license(self, repository_owner, repository_name):
        response = requests.get(f'https://gitlab.com/api/v4/projects/{repository_owner}%2F{repository_name}', params={'license' : True})
        if response.status_code == 200:
            license_resp = requests.get(f'https://gitlab.com/api/v4/licenses/{response.json()["license"]["key"]}').json() if response.json()['license'] else None
            return License(license_resp['name'], license_resp['permissions'],license_resp['conditions'],license_resp['limitations']) if license_resp else None
        elif response.status_code == 404:
            return None
        else:
            print('{}{}'.format(Style.BRIGHT + Fore.RED,'API rate limit!'))
            exit()
