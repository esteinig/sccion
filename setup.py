from setuptools import setup, find_packages

setup(
    name="sccion",
    url="https://github.com/esteinig/sccion",
    author="Eike J. Steinig",
    author_email="eikejoachim.steinig@my.jcu.edu.au",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "tqdm",
        "pandas",
        "click",
        "pytest",
    ],
    entry_points="""
        [console_scripts]
        sccion=sccion.terminal.client:terminal_client
    """,
    version="0.1",
    license="MIT",
    description="""
        Whole genome and real-time nanopore typing for Staphylococcus aureus
    """,
)
