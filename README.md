# LSPT-Link-Analysis
LSPT 2024 - Team V Link Analysis

This project uses python's virtual enviornment to manage dependencies. Make sure to create the venv in the root of the project, and 
use the ```requirements.txt``` file to install the necessary packages. for more information on python's venv, go [here](https://docs.python.org/3/library/venv.html).


### Creating the virtual enviornment

To create a virtual eviornment called venv, run:

```
python -m venv venv
```

### Activating the virtual enviornment

In order to use the virtual enviornment, you must activate it first. On windows:

```
.\venv\Scripts\activate
```

On POSIX;

```
.\venv\bin\activate
```

### Installing and adding dependencies

Once the venv is atcivated, you can install python packages into the enviornment, and it will be isolated from your system's enviornment. To install the necessary packages, run

```
pip install -r requirements.txt
```

if you need to add new dependencies to the project, make sure to add them to the ```requirements.txt``` file, so created enviornments will have all the needed dependencies. 