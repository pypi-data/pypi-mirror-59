from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="allenpoly",
    packages=find_packages(),
    version="0.0.6",
    license="BSD",
    description="An library to use AllenNLP library in Polyaxon environment.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Evidence Prime Sp. z o.o.",
    author_email="mateusz.pieniak@evidenceprime.com",
    url="https://bitbucket.org/evidenceprime/allenpoly",
    keywords=["allennlp", "polyaxon"],
    install_requires=[
        "python-dateutil<2.8.1, >=2.1",  # Solves conflicts between allennlp & polyaxon-client
        "docutils<0.16, >=0.10",  # Solves conflicts between allennlp & polyaxon-client
        "rhea==0.5.4",  # Solves conflicts between allennlp & polyaxon-client
        "allennlp>=0.9.0",
        "polyaxon-client>=0.5.6",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["allenpoly=allenpoly.run:run"]},
)