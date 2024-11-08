# Contributing to pyscreenrec

👍🎉 First off, thanks for taking the time to contribute! 🎉👍

The following is a set of guidelines for contributing to *pyscreenrec*, which is hosted on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Setup local development environment

This section shows how you can setup your development environment to contribute to *pyscreenrec*.

1. Fork the repository.

2. Clone it using Git (`git clone https://github.com/<YOUR USERNAME>/pyscreenrec.git`).

3. Create a virtual environment.

```
python -m venv venv
```

Activate it using

```
./venv/Scripts/Activate.ps1
```
on Windows

```
source ./venv/bin/activate
```

on unix-based systems (make sure to choose the activation script according to your shell)

4. Install dependencies.

We recommend using [poetry](https://python-poetry.org) for dependency management.

```
poetry install --no-root
```

Otherwise, using pip:

```
pip install .
```

5. Make your changes.

6. Stage and commit (`git add .` and `git commit -m "COMMIT MESSAGE"`). 

7. Push it your remote repository (`git push`).

8. Open a pull request by clicking [here](https://github.com/shravanasati/pyscreenrec/compare). 


## Reporting Issues

If you know a bug in the code or you want to file a feature request, open an issue.

Choose one of the issue templates by clicking [here](https://github.com/shravanasati/pyscreenrec/issues/new/choose).