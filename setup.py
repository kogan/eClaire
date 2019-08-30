from setuptools import find_packages, setup

setup(
    name="eClaire",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests >= 2.6.0",
        "py-trello == 0.14.0",
        "fpdf >= 1.7.2",
        "pillow >= 2.9.0",
        "pyyaml == 3.11",
        "pyOpenSSL >= 0.15.1",
        "pyasn1 >= 0.1.9",
        "ndg-httpsclient >= 0.4.0",
    ],
    entry_points={"console_scripts": ["eclaire = eclaire.main:main"]},
    package_data={"eclaire": ["font/*.ttf"]},
)
