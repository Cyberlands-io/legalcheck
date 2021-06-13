from git import License, Repository
import os
import argparse
from filemanager import File_Manager


class License_Checker(File_Manager):

    def __init__(self, path_to_lib, is_local_search):
        self.is_local_search = is_local_search
        File_Manager.__init__(File_Manager, path_to_lib)

    def main(self):
        if self.is_local_search:
            print("Find Local licenses")
            for lic_path in self.find_license_files():
                repository = Repository(License.analize_license(lic_path), name=lic_path.split('/')[-2])
                Repository.print_repository_data(repository)

        else:
            print("Get Remote licenses")
            self.get_repos_info()
            for repository in self.repositories:
                Repository.print_repository_data(repository)


if __name__ == '__main__':

    # Get args
    parser = argparse.ArgumentParser(prog='legal_check', usage='%(prog)s [options] libs separated by spaces')
    parser.add_argument('lib', help='Path to libraries folder')
    parser.add_argument('-l', action='store_true', help='Get a local license file')
    args = parser.parse_args()
    
    if os.path.isdir(args.lib):
        checker = License_Checker(args.lib, args.l)
        checker.main()
