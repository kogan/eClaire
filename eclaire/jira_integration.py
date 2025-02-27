from jira import JIRA, JIRAError
import typing as t
import logging

from eclaire.render import generate_epic, generate_idea

log = logging.getLogger(__name__)


class JiraIntegration:
    def __init__(self, credentials):
        self.username = credentials["jira_username"]
        self.api_token = credentials["jira_token"]

        self.jira = JIRA(credentials["jira_url"], basic_auth=(self.username, self.api_token))

    def process(self):
        for issue, issue_type in self._get_tickets():
            if issue_type == 'epic':
                yield generate_epic(f"{issue.key}: {issue.fields.summary}")
            elif issue_type == 'idea':
                yield generate_idea(issue)
            self._update_ticket(issue)

    def _get_tickets(self) -> t.List[t.Tuple[str, str]]:
        ticket_list = []
        for ticket in self.jira.search_issues(f"type='Epic' and labels='printme'"):
            ticket_list.append((ticket, 'epic'))
        for ticket in self.jira.search_issues(f"type='Idea' and labels='printme'"):
            ticket_list.append((ticket, 'idea'))
        return ticket_list

    def _update_ticket(self, issue):
        labels = issue.fields.labels
        labels.remove("printme")
        labels.append("printed")
        try:
            issue.update(fields={"labels": labels})
        except JIRAError:
            pass
