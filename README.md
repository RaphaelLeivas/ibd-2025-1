# ibd-2025-1
Repo para a disciplina de Introdução a Banco de Dados, 2025/1 Engenharia de Sistemas UFMG

# Setting Up Development Environment (Python)

- install python 3.12.4 https://www.python.org/downloads/release/python-3124/
    - make sure the python.exe is placed in the PATH during the installation wizard

- check that the installation was successful: open CMD and run `python -V`. It must show the version installed.
- clone / pull the repository
- go to folder containing project
- connect FUG and PUMP to computer. Make sure they show up in the Operating System's device manager.
- make sure the `setup.json` file has all the configurations used.

Now we need to do the following:
 * Create Pyhton virtual environment
 * Activate the virtual env
 * Install the packages in this virtual environment
 * Run the Jupyer Notebook inside this virtual environment
 
To do all those things, do the following:
- `python -m venv myEnv`
- cd to myEnv/Scripts (cd myEnv/Scripts/)
- `.\activate`
- cd back to project root folder (cd ../../)
- check that the package ipykernel==6.29.5 is in the requirements.txt file (for Jupyter notebook)
- `pip install -r requirements.txt`
- check that all modules were installed: `pip freeze`
- choose the newly created virtual environment in the VS Code lower right corner
    - or press F1: pyhton select interpreter and the env on the local myEnv folder
- run the program: `python main.py`
- to exit the virtual environment afterwards: `deactivate`
