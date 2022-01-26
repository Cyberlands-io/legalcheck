# [Сyberlands](https://cyberlands.io) Legal Check
Cyberlands open-source license validation tool which allows to check licensing for used packages, as result tool generates a xls file with information about repositories in the target forder and their liceses.

This tool is developed in collaboration with [DigiLaw](https://digilaw.pro/) company

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

## Supported languages
* actionscript3
* applescript
* asp
* c
* clojure
* coffee-script, coffeescript, coffee
* cpp - C++
* cs
* csharp
* css
* bash
* elixir
* go
* haml
* http
* java
* javascript
* markdown
* objectivec
* pascal
* PHP
* Perl
* python
* rust
* shell, sh, zsh, bash - Shell scripting
* sql
* swift
* rb, jruby, ruby - Ruby
* smalltalk
* volt
* vue
* yaml