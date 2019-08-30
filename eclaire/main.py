#!/usr/bin/env python

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

import argparse
import logging
import time

import yaml
from eclaire.base import EClaire

# components of the system
from eclaire.notifications import hipchat_notification
from requests.exceptions import RequestException
from trello import ResourceUnavailable

BASE_WAIT = 30
MAX_WAIT = 30 * 60
log = logging.getLogger(__name__)


def main():
    setup_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Dont actually print the labels.")
    parser.add_argument(
        "--config",
        type=argparse.FileType("r"),
        required=True,
        help="Configuration file (for tokens & board setup)",
    )
    parser.add_argument("--list-boards", action="store_true", help="Discover board and label IDs")
    parser.add_argument("--run-once", action="store_true", help="Exit after running once")

    args = parser.parse_args()

    config = yaml.load(args.config)

    if args.list_boards:
        # List available boards then exit
        eclaire = EClaire(credentials=config["credentials"])
        eclaire.list_boards()
        return

    eclaire = EClaire(credentials=config["credentials"], boards=config["boards"])

    log.info("Discovering labels")
    eclaire.discover_labels()

    wait_time = BASE_WAIT

    # Main program loop
    while True:
        try:
            eclaire.process_boards(
                dry_run=args.dry_run,
                notify_fn=hipchat_notification,
                notify_config=config.get("hipchat"),
            )
        except (ResourceUnavailable, RequestException):
            log.exception("An error occurred polling Trello")

            if args.run_once:
                break

            log.warning("Waiting %d seconds before trying again", wait_time)
            time.sleep(wait_time)
            # exponential wait time up to MAX_WAIT on a timeout error
            wait_time = min(MAX_WAIT, wait_time * 2)
            continue

        wait_time = BASE_WAIT

        log.info("-------")

        if args.run_once:
            break

        time.sleep(wait_time)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)-15s %(name)-15s %(levelname)-8s %(message)s"
    )
    logging.getLogger("requests").setLevel(logging.ERROR)


if __name__ == "__main__":
    main()
