# <img align="center" src="https://user-images.githubusercontent.com/18221356/131405849-aa3e6b78-df8c-4417-a8bf-91b97338ba68.gif" alt="Elsa" width="75"/> Elsa Client

A simple client to commit messages with a Jira proyect key as prefix...

## Setup

- Download "elsa.py" from this repository
- Move "elsa.py" file in `/usr/local/bin`
- Grant permit 

## Examples

```bash
elsa -c 777 -m                  # git commit -m "ICDMNG-777"

elsa -c 777 -m "add tests"      # git commit -m "ICDMNG-777: add test"

elsa -c 777 -m "add tests" -p   # git commit -m "ICDMNG-777: add test" & git push origin ${current_branch}
```


## Help?

```bash
elsa --help
```

