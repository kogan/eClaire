# Copyright 2019 KOGAN.COM PTY LTD

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import find_packages, setup

setup(
    name="eClaire",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "requests ~= 2.22.0",
        "py-trello == 0.14.0",
        "fpdf >= 1.7.2",
        "pillow >= 6.2.2",
        "qrcode == 5.1",
        "pyyaml ~= 5.3",
        "pyOpenSSL >= 0.15.1",
        "pyasn1 >= 0.1.9",
        "ndg-httpsclient >= 0.4.0",
    ],
    entry_points={"console_scripts": ["eclaire = eclaire.main:main"]},
    package_data={"eclaire": ["font/*.ttf"]},
)
