import setuptools
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info

import os

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="medcat",
    setup_requires=["setuptools_scm"],
    use_scm_version={"local_scheme": "no-local-version", "fallback_version": "unknown"},
    author="w-is-h",
    author_email="w.kraljevic@gmail.com",
    description="Concept annotation tool for Electronic Health Records",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CogStack/MedCAT",
    packages=['medcat', 'medcat.utils', 'medcat.preprocessing', 'medcat.cogstack', 'medcat.ner', 'medcat.linking', 'medcat.datasets', 'medcat.deprecated', 'medcat.cli', 'medcat.tokenizers', 'medcat.utils.meta_cat', 'medcat.pipeline'],
    install_requires=[
        'numpy<1.21.0,>=1.19.0',
        'pandas<=1.3.4,>=1.1.5',
        'gensim~=4.1.2',
        'spacy<3.1.4,>=3.0.1',
        'scipy<=1.7.1,>=1.5.4',
        'transformers~=4.11.3',
        'torch<1.10,>=1.0',
        'tqdm>=4.27',
        'sklearn~=0.0',
        'elasticsearch>=7.10',
        'dill~=0.3.4',
        'datasets~=1.14.0',
        'psutil<6.0.0,>=5.8.0',
        'gitpython==3.1.18',
        'pydrive2==1.10.0',
        'dvc>=2.7.4',
        'fire==0.4.0',
        'wexpect>=4.0.0' if os.name == "nt" else "",
        'pexpect>=4.8.0',
        'jsonpickle==2.0.0',
        'pywin32>=301' if os.name == "nt" else "",
        'pypiwin32>=223' if os.name == "nt" else "",
        'multiprocess' # seems to work better than standard mp
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
