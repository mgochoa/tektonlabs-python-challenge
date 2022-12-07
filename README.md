# Tekton Challenge

---

## How to run it

### Create virtual environment

    python -m venv

### Activate virtual environment

#### Windows:

    PS C:\> <venv>\Scripts\Activate.ps1

#### Linux:

    source <venv>/bin/activate

### Install dependencies

    pip install -r requirements.txt

### In production

    uvicorn tekton_challenge.main:app --reload --log-config ./tekton_challenge/log.ini

### In development

    python ./tekton_challenge/main.py

### Open docs

    http://localhost:8000/docs

## How to test it

### Running tests with

    pytest
