import os
import argparse
from filemanager import FileManager


class LicenseChecker(FileManager):

    def __init__(self, path_to_lib) -> None:
        FileManager.__init__(FileManager, path_to_lib)

    def main(self):
        self.get_repos_info()
        for repos in self.repositories:
            repos.rep_license = repos.get_repository_license(repos.owner, repos.name)
            repos.print_license_data(repos)


if __name__ == '__main__':

    # Get args
    parser = argparse.ArgumentParser(prog='legal_check', usage='%(prog)s [options] libs separated by spaces')
    parser.add_argument('lib', help='Path to libraries folder')
    parser.add_argument('-l', action='store_true', help='Get a local license file')
    args = parser.parse_args()

    if os.path.isdir(args.lib):
        checker = LicenseChecker(args.lib)
        if args.l:
            checker.find_license_and_readme_files()

        checker.main()
