# Contributing to pyscreenrec

👍🎉 First off, thanks for taking the time to contribute! 🎉👍

The following is a set of guidelines for contributing to *pyscreenrec*, which is hosted on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Repository structure
```
.
├── .github                 # issue templates and workflows
│   ├── ISSUE_TEMPLATE      # issue templates
        ├── bug_report.md
        ├── custom.md
        ├── feature_request.md
    ├── workflows           # CI/CD workflows
        ├── .python-package.yml
└── pyscreenrec
    ├── __init__.py         # main code
├── .gitignore
├── CHANGELOG
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── requirements.txt    
└── setup.py                # setup config for pypi

```

## Setup environment for contribution
This section shows how you can setup your development environment to contribute to *pyscreenrec*.

1. Fork the repository.
2. Clone it using Git (`git clone https://github.com/<YOUR USERNAME>/pyscreenrec.git`).
3. Install requirements using `pip install -r requirements.txt`.
4. Make changes.
5. Stage and commit (`git add .` and `git commit -m "COMMIT MESSAGE"`). 
6. Push it your remote repository (`git push`).
7. Open a pull request by clicking [here](https://github.com/shravanasati/pyscreenrec/compare). 


## Reporting Issues

If you know a bug in the code or you want to file a feature request, open an issue.

Choose one of the issue templates by clicking [here](https://github.com/shravanasati/pyscreenrec/issues/new/choose).