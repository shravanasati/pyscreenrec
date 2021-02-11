from setuptools import find_packages, setup

VERSION = 0.1

setup(
    name = "pyscreenrec",
    version = VERSION,
    description = "A small python library to record screen.",
    long_description_content_type = "text/markdown",
    long_description = "https://github.com/Shravan-1908/pyscreenrec#readme",
    url="https://github.com/Shravan-1908/pyscreenrec",
    author = "Shravan Asati",
    author_email = "dev.shravan@protonmail.com",
    packages = find_packages(),
    install_requires = ["pyscreeze", "opencv-python", "natsort"],
    license = 'MIT',
    keywords = ["python", "screen recording", "screen", "recording", "screenshots"],
    classifiers = [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
    )