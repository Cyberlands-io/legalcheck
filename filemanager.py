import os
from re import search as rsearch
from git import GitHub, GitLab

class File_Manager():

    LICENSE_FILE = 'LICENSE'
    DIR_NAME = '.git'
    CONFIG_FILE = '/config'
    repositories = set()
    repos_info_pattern = r'(?s)^.*(?<=(gitlab.com|github.com))(.*$)'
    url_pattern = r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'

    def __init__(self, path_to_lib) -> None:
        self.path = path_to_lib
    
    # For local search

    def find_license_files(self):
        licenses = set()
        for root, _, filenames in os.walk(self.path):
            for file in filenames:
                if file.endswith(self.LICENSE_FILE):
                    licenses.add(os.path.join(root, file))
        return licenses

    # For remote search
    
    def get_repos_info(self):
        for root, directories, _ in os.walk(self.path):
            for direct in directories:
                if direct.endswith(self.DIR_NAME):
                    self.repositories.add(self.read_config(os.path.join(root, direct)))

    @staticmethod
    def parse_data(pattern, string, group_index):
        try:
            return rsearch(pattern,string).group(group_index)
        except Exception as ex:
            print(ex)

    @staticmethod
    def line_that_contain(string, fp):
        return [line for line in fp if string in line][0].strip()

    def read_config(self, path_to_git_dir):

        with open(path_to_git_dir + self.CONFIG_FILE) as file:
            url = File_Manager.parse_data(self.url_pattern, File_Manager.line_that_contain('url', file), 0)
            _, repository_owner, repository_name = File_Manager.parse_data(self.repos_info_pattern,url , 2).split('/')
            
            return GitHub(name = repository_name, owner = repository_owner, url=url) \
                   if 'github' in File_Manager.parse_data(self.repos_info_pattern, url, 1) \
                   else GitLab( name = repository_name, owner = repository_owner,url=url)