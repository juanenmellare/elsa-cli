# Elsa Client

A simple client to commit messages with a Jira proyect key as prefix...

## Requeriments
- Python 2.7

## Install

Grant permits, move "elsa.py" file in /usr/local/bin and rename it as "elsa" without the ".py" extension.
```bash
cd elsa-cli
chmod a+x elsa.py
mv elsa.py /usr/local/bin/elsa
```

## Startup

Type `elsa` and set the Jira proyect key (set in the current terminal, if you open another you'll have to set it up again).


## Commits Examples

```bash
elsa -c 777                     # git commit -m "ICDMNG-777"

elsa -c 777 -m "add tests"      # git commit -m "ICDMNG-777: add test"

elsa -c 777 -m "add tests" -p   # git commit -m "ICDMNG-777: add test" & git push origin ${current_branch}
```

## Help?

```bash
elsa --help
```

