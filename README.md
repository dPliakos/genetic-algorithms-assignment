# Genetic algorithms experiment


Required tools:
 
 - python3
 - make
 - virualenv
 
Optional:
 - gnu-parallel (for parallel execution)


Preperation:
 - `virtualenv -p python3 ./.venv`
 - `source ./.venv/bin/activate`
 - `pip3 install -r ./requirements.txt`

Execution:
 - normal execution: `make`
 - show trace /debug : `make trace`
 - show graph: `make graph`
 - run multiple instances (e.g. for 100 executions): `N=100 make par`
