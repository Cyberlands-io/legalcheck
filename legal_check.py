from git import License, Repository
import os
import argparse
from filemanager import File_Manager
from progress.bar import IncrementalBar
import time
from command_line import process, read_strategy, Level
import sys

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


def parse_args(args):

    if '--lib' in args and '--req' not in args and '--help' not in args:
        if not args[args.index('--lib') + 1].startswith('-'):
            lib = args[args.index('--lib') + 1]
            local = False
            console_output = False
            if '-l' in args:
                local = True
            if '-oC' in args:
                console_output = True
            if os.path.isdir(lib):
                    checker = License_Checker(lib, local)
                    checker.main()
                    if console_output:
                        for repository in checker.repositories:
                            Repository.print_repository_data(repository)
        else:
            print('Enter path to lib')
    elif '--req' in args and '--lib' not in args and '--help' not in args:
        strategy_ini_file = './liccheck.ini'
        requirement_txt_file = './requirements.txt'
        reporting_txt_file = None
        no_deps = False
        level = Level.STANDARD
        if '-s' in args and not args[args.index('-s') + 1].startswith('-'):
            strategy_ini_file = args[args.index('-s') + 1]
        if '-lv' in args and not args[args.index('-lv') + 1].startswith('-'):
            level = args[args.index('-lv') + 1]
        if '-r' in args and not args[args.index('-r') + 1].startswith('-'):
            requirement_txt_file = args[args.index('-r') + 1]
        if '-R' in args and not args[args.index('-R') + 1].startswith('-'):
            reporting_txt_file = args[args.index('-R') + 1]
        if '--no-deps' in args and '--no-deps' in args:
            no_deps = True
        strategy = read_strategy(strategy_ini_file)
        process(requirement_txt_file, strategy, level, reporting_txt_file, no_deps)

    elif '--help' in args and '--req' not in args and '--lib' not in args:
        print('''usage:  legal_check.py [ -h --help ]

                    For license check :

                        required arguments:
                            --lib              Path to libraries folder

                        optional arguments:
                            -l                 Get a local license file
                            -oC                Output result to console


                    python legal_check.py --lib path_to_cloned_libs [ -l | -oC ]

                    For requirements check :

                        required arguments:
                            --req              Check requirements

                        optional arguments:
                            -s                 Strategy ini file
                            -lv                Level for testing compliance of packages, where:
                                                   Standard - At least one authorized license (default);
                                                   Cautious - Per standard but no unauthorized licenses;
                                                   Paranoid - All licenses must by authorized.
                            -r                 path/to/requirement.txt file
                            -R                 path/to/reporting.txt file
                            --no-deps          Don't check dependencies

                    python legal_check.py --req [ -s | -r | -R | --no-deps ]

 ''')
    else:
        print('Use python legal_check.py --help ')
        exit()

def main():
    parse_args(sys.argv)

if __name__ == '__main__':
    main()