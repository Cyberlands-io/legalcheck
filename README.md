# [Сyberlands.io](https://cyberlands.io) LegalCheck
Cyberlands open source license validation tool which allows to check licensing for used packages, as result tool generates a xls file with information about repositories in the target forder and their liceses.

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

## Supported licenses
* agpl 3.0
* apache 2.0
* bsd 2-clause
* bsd 3-clause
* bsl 1.0
* creative commons 1.0
* epl 2.0
* gpl 2.0
* gpl 3.0
* lgpl 2.1
* mit
* mpl 2.0

## Sample output
```bash
python legal_check.py --lib /tmp/legal-check-test -oC
Get Remote licenses

https://github.com/sansyrox/robyn

       BSD 2-Clause "Simplified" License

          Pemissions           Conditions          Limitations

      commercial-use    include-copyright            liability
       modifications                                  warranty
        distribution
         private-use

https://github.com/dorey/JavaScript-Equality-Table

Creative Commons Attribution Share Alike 4.0 International

          Pemissions           Conditions          Limitations

      commercial-use    include-copyright            liability
       modifications     document-changes        trademark-use
        distribution         same-license           patent-use
         private-use                                  warranty

https://github.com/ximerus/Empire

 BSD 3-Clause "New" or "Revised" License

          Pemissions           Conditions          Limitations

      commercial-use    include-copyright            liability
       modifications                                  warranty
        distribution
         private-use

https://github.com/poise/python

                      Apache License 2.0

          Pemissions           Conditions          Limitations

      commercial-use    include-copyright        trademark-use
       modifications     document-changes            liability
        distribution                                  warranty
          patent-use
         private-use

https://github.com/yrutschle/sslh

         GNU General Public License v2.0

          Pemissions           Conditions          Limitations

      commercial-use    include-copyright            liability
       modifications     document-changes             warranty
        distribution      disclose-source
         private-use         same-license

https://github.com/pion/webrtc

                             MIT License

          Pemissions           Conditions          Limitations

      commercial-use    include-copyright            liability
       modifications                                  warranty
        distribution
         private-use

https://github.com/nabla-c0d3/sslyze

  GNU Affero General Public License v3.0

          Pemissions           Conditions          Limitations

      commercial-use    include-copyright            liability
       modifications     document-changes             warranty
        distribution      disclose-source
          patent-use network-use-disclose
         private-use         same-license
```
