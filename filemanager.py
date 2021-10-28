import os
import xlsxwriter
from re import search as rsearch
from git import GitHub, GitLab, License, Repository

class File_Manager():

    LICENSE_FILE = r'LICENSE*'
    DIR_NAME = '.git'
    CONFIG_FILE = '/config'
    FILE_RESULT = 'res.xlsx'
    repositories = set()
    repos_info_pattern = r'(?s)^.*(?<=(gitlab.com|github.com))(.*$)'
    url_pattern = r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'

    sheet_titles = ['Repository name', 'License name', 'Permissions', 'Conditions', 'Limitations']

    def __init__(self, path_to_lib) -> None:
        self.path = path_to_lib
        self.workbook = xlsxwriter.Workbook(self.FILE_RESULT)
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.write_row(0, 0, self.sheet_titles, self.workbook.add_format({'bg_color': '#AAAAAA', 'bold': True, 'border': True, 'font_size' : '14'}))
        self.worksheet.set_column(0, len(self.sheet_titles), 25)
        

    def write_repository_data_to_file(self, **kwargs):
        cell_format = self.workbook.add_format({'border': True})
        if kwargs.get('Repository_License'):
            self.worksheet.write_row(kwargs.get('Index') + 1, 0, [kwargs.get('Name'), kwargs.get('Repository_License').name, '\n'.join(kwargs.get('Repository_License').permissions), '\n'.join(kwargs.get('Repository_License').conditions), '\n'.join(kwargs.get('Repository_License').limitations)],cell_format)
        else:
            self.worksheet.write(kwargs.get('Index') + 1, 0, kwargs.get('Name'),cell_format)

    
    # For local search

    def find_license_files(self):

        for root, _, filenames in os.walk(self.path):
            for file in filenames:
                if rsearch(self.LICENSE_FILE,file.rsplit(None, 1)[-1]):
                    self.repositories.add(Repository(License.analize_license(os.path.join(root, file)), name=os.path.join(root, file).split('/')[-2]))

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
