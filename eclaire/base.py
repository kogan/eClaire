from __future__ import print_function

import logging
import sys

from eclaire.render import generate_pdf, print_card
from trello import TrelloClient

log = logging.getLogger(__name__)


FILTER_LABEL = "PRINTME"
DONE_LABEL = "PRINTED"
SPECIAL_LABELS = (FILTER_LABEL, DONE_LABEL)
MAX_LABEL_CHARS = 50


class PrintingError(Exception):
    pass


class EClaire(object):
    def __init__(self, credentials, boards=None):
        self.trello_client = TrelloClient(
            api_key=credentials["public_key"], token=credentials["member_token"]
        )

        self.boards = boards

    def process_boards(self, dry_run=False, notify_fn=None, notify_config=None):
        """
        Process each board in self.boards
        """

        for name, board_config in self.boards.items():
            log.info("Polling %s", name)
            processed = self.process_board(board_config, dry_run)

            if board_config.get("notify", False) and notify_fn is not None:
                for card in processed:
                    notify_fn(card, **notify_config)

    def process_board(self, board_config, dry_run=False):
        """
        Process each card in a given board
        """
        processed = []
        for card in self.fetch_cards(board_id=board_config["id"]):
            log.info('Printing card "%s"', card.name)

            pdf = generate_pdf(card)
            if not dry_run:
                print_card(pdf, printer_name=board_config["printer"])
            self.update_card(card, board_config)
            processed.append(card)

        return processed

    def fetch_cards(self, board_id):
        """
        Fetch all candidate cards on a board for processing
        """
        data = []
        board = self.trello_client.get_board(board_id)
        for card in board.open_cards():
            if card.labels and FILTER_LABEL in (l.name for l in card.labels):
                card.fetch_actions()
                data.append(card)

        return data

    def discover_labels(self):
        """
        Store object references for special labels
        """
        for name, config in self.boards.items():
            board = self.trello_client.get_board(config["id"])
            labels = {}
            for label in board.get_labels(limit=1000):
                if label.name in SPECIAL_LABELS:
                    labels[label.name] = label
            missing = set(SPECIAL_LABELS) - set(labels.keys())
            if missing:
                log.fatal('Board "%s" is missing the labels %s', board.name, " and ".join(missing))
                log.fatal("Exiting")
                sys.exit(1)
            config["labels"] = labels

    def remove_label(self, card, label):
        """
        Remove a lable from a card.

        At the time of writing there is no way to remove a label with py-trello
        """
        self.trello_client.fetch_json(
            "/cards/" + card.id + "/idLabels/" + label.id, http_method="DELETE"
        )

    def update_card(self, card, board_config):
        """
        Replace PRINTME label with PRINTED
        """
        printme_label = board_config["labels"]["PRINTME"]
        printed_label = board_config["labels"]["PRINTED"]

        self.remove_label(card, printme_label)

        if printed_label not in card.labels:
            card.add_label(printed_label)

    def list_boards(self):
        """
        Fetch all board IDs from trello & print them out
        """
        for board in self.trello_client.list_boards():
            print("Board:", board.name)
            print("   ID:", board.id)
            print()
