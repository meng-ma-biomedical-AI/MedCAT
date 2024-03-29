import setuptools
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info

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
    packages=['medcat', 'medcat.utils', 'medcat.preprocessing', 'medcat.cogstack', 'medcat.ner', 'medcat.linking', 'medcat.datasets', 'medcat.deprecated',
              'medcat.tokenizers', 'medcat.utils.meta_cat', 'medcat.pipeline'],
    install_requires=[
        'numpy<1.21.0,>=1.19.0',
        'pandas~=1.0',
        'gensim~=3.8',
        'spacy<3.1.0,>=3.0.1',
        'scipy~=1.5',
        'transformers~=4.10.0',
        'torch~=1.8.1',
        'tqdm<4.50.0,>=4.27',
        'sklearn~=0.0',
        'elasticsearch~=7.10',
        'dill~=0.3.3',
        'datasets~=1.6.0',
        'jsonpickle~=2.0.0',
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
