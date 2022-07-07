from jira import JIRA
import typing as t
import logging

from eclaire.render import generate_epic

log = logging.getLogger(__name__)


class JiraIntegration:
    def __init__(self, credentials):
        self.username = credentials["jira_username"]
        self.api_token = credentials["jira_token"]

        self.jira = JIRA(credentials["jira_url"], basic_auth=(self.username, self.api_token))

    def process(self):
        for key, title in self._get_tickets():
            yield generate_epic(f"{key}: {title}")
            self._update_ticket(key)

    def _get_tickets(self) -> t.List[t.Tuple[str, str]]:
        tickets = self.jira.search_issues(f"type='Epic' and labels='printme'")
        ticket_list = []
        for ticket in tickets:
            ticket_list.append((ticket.key, ticket.fields.summary))
        return ticket_list

    def _update_ticket(self, ticket: str):
        issue = self.jira.issue(ticket)
        labels = issue.fields.labels
        labels.remove("printme")
        labels.append("printed")
        issue.update(fields={"labels": labels})
