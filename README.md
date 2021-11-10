# [Сyberlands](https://cyberlands.io) Legal Check
Cyberlands open-source license validation tool which allows to check licensing for used packages, as result tool generates a xls file with information about repositories in the target forder and their liceses.

## Install:
  ```
  git clone https://github.com/Cyberlands-io/legal-check.git
  pip install -r requirements.txt
  ```

## Usage:
  ```
  python3 legal_check.py --lib <path_to_cloned_libs>
  open res.xls
  ```
    
**Arguments:**  
    ```--lib``` - Path to libraries folder

**Optional arguments:**  
  ```-h, --help``` - Show this help message and exit  
  ```-l``` - Get a local license file