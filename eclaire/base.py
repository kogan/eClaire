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

from __future__ import print_function


from eclaire.jira_integration import JiraIntegration
from eclaire.render import print_card


class PrintingError(Exception):
    pass


class EClaire:
    processors = {"jira": JiraIntegration}

    def __init__(self, credentials):
        self.credentials = credentials

    def process_board(self, config):
        processor = self.processors.get(config.get("processor", "trello"))(self.credentials)
        for pdf in processor.process():
            print_card(pdf, config["printer"])
