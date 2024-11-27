# Bitwarden-account-checker

This tool is meant to quickly check a bitwarden vault passwords against the Have I Been Pwned password database.


## How to use
1) Export your vault as an unencrypted json this can be done using there clients or via the online vault https://vault.bitwarden.com/#/tools/export
2) Run the python script with the arg of your json file. 

## Optional augments
  -h, --help            show this help message and exit
  --showpasswords       when printing breached accounts include passwords in print
  --threadcount THREADCOUNT
                        Number of workers (default: 25)