import os
from re import search as rsearch
from git import GitHub, GitLab

class File_Manager():

    FILE_NAMES = ('LICENSE','README.md')
    DIR_NAMES = ('.git')
    matches = set()
    repositories = set()
    repos_info_pattern = r'(?s)^.*(?<=(gitlab.com|github.com))(.*$)'
    url_pattern = r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'

    def __init__(self, path_to_lib) -> None:
        self.path = path_to_lib

    def find_license_and_readme_files(self):
        for root, _, filenames in os.walk(self.path):
            for file in filenames:
                if file.endswith(self.FILE_NAMES):
                    print(os.path.join(root, file))

    def get_repos_info(self):
        for root, directories, _ in os.walk(self.path):
            for direct in directories:
                if direct.endswith(self.DIR_NAMES):
                    self.repositories.add(self.read_config(os.path.join(root, direct),'/config'))

    def lines_that_contain(self, string, fp):
        return [line for line in fp if string in line]

    def read_config(self, path_to_git_dir, file):
        with open(path_to_git_dir + file) as file:
            url = rsearch(self.url_pattern,self.lines_that_contain('url', file)[0].strip()).group(0)
            result = rsearch(self.repos_info_pattern,url).group(2).split('/')
            return GitHub(result[2],result[1],url=url) if 'github' in rsearch(self.repos_info_pattern,url).group(1) else GitLab(result[2],result[1],url=url)