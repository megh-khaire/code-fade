# code-fade

> Measuring the half life of code on Github

<!-- MAIN BODY -->
## Installation

Before you start the installation process make sure you have python installed.

1 Clone this repositor on your local machine:

```bash
git clone git@github.com:code-fade/code-fade.git
```

2 Move inside the main project directory:

```bash
cd code-fade
```

3 Setup and activate your virtual environment (optional):

```bash
# To create a virtual env:
python -m venv .venv
# Note: use python3 if you're on MacOS

# For activation use one of the following commands based on your OS:
source .venv/bin/activate   # On Mac / Linux
.venv\Scripts\activate.bat  # In Windows CMD
.venv\Scripts\Activate.ps1  # In Windows Powershel
```

4 Install the required packages from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Create `.env` file

1. Duplicate the provided `example.env` file.
2. Rename the duplicated file to `.env`.
3. Open the `.env` file and insert the secrets and configurations required for the application to function properly.
