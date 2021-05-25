from git import License, Repository
import os
import argparse
from file_manager import File_Manager

class License_Checker(File_Manager):

    def __init__(self, path_to_lib) -> None:
        File_Manager.__init__(File_Manager, path_to_lib)

    def main(self, local):
        if local:
            print("Find Local licenses")
            for lic_path in checker.find_license_files():
                rep = Repository(License.compare_license(lic_path), name=lic_path.split('/')[-2])
                rep.print_license_data(rep)
        else:
            print("Get Remote licenses")
            self.get_repos_info()
            for repos in self.repositories:
                repos.rep_license = repos.get_repository_license(repos.owner,repos.name)
                repos.print_license_data(repos)


if __name__ == '__main__':

    # Get args
    parser = argparse.ArgumentParser(prog='legal_check',usage='%(prog)s [options] libs separated by spaces')
    parser.add_argument('lib', help='Path to libraries folder')
    parser.add_argument('-l', action='store_true', help='Get a local license file')
    args = parser.parse_args(['/Users/klaus/Downloads/test/legal_check/', '-l'])
    
    if os.path.isdir(args.lib):
        checker = License_Checker(args.lib)
        checker.main(args.l)

        