from setuptools import find_packages, setup

VERSION = 0.4
with open("README.md") as f:
    README = f.read()

setup(
    name = "pyscreenrec",
    version = VERSION,
    description = "A small and cross-platform python library for recording screen.",
    long_description_content_type = "text/markdown",
    long_description = README,
    url="https://github.com/shravanasati/pyscreenrec",
    author = "Shravan Asati",
    author_email = "dev.shravan@protonmail.com",
    packages = find_packages(),
    install_requires = ["pyscreeze", "opencv-python", "natsort"],
    license = 'MIT',
    keywords = ["python", "screen recording", "screen", "recording", "screenshots"],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries"
    ]
)