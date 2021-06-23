from git import License, Repository
import os
import argparse
from filemanager import File_Manager
from progress.bar import IncrementalBar
import time


class License_Checker(File_Manager):

    def __init__(self, path_to_lib, is_local_search):
        self.is_local_search = is_local_search
        File_Manager.__init__(File_Manager, path_to_lib)

    def main(self):
        try:
            if self.is_local_search:
                print("Find Local licenses")
                self.find_license_files()
            else:
                print("Get Remote licenses")
                self.get_repos_info()
                
            for i, repository in enumerate(self.repositories):
                self.write_repository_data_to_file(Index = i,Name = repository.name, Repository_License = repository.rep_license)
        finally:
            self.workbook.close()


if __name__ == '__main__':

    # Get args
    parser = argparse.ArgumentParser(prog='legal_check', usage='%(prog)s [options] libs separated by spaces')
    parser.add_argument('lib', help='Path to libraries folder')
    parser.add_argument('-l', action='store_true', help='Get a local license file')
    parser.add_argument('-oC', action='store_true', help='Output result to console')
    args = parser.parse_args()

    if os.path.isdir(args.lib):
        checker = License_Checker(args.lib, args.l)
        checker.main()
        if args.oC:
            for repository in checker.repositories:
                Repository.print_repository_data(repository)