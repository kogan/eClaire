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
from requests.exceptions import RequestException
from trello import ResourceUnavailable

BASE_WAIT = 30
MAX_WAIT = 30 * 60
log = logging.getLogger(__name__)


def main():
    setup_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=argparse.FileType("r"),
        required=True,
        help="Configuration file (for tokens & board setup)",
    )
    parser.add_argument("--run-once", action="store_true", help="Exit after running once")

    args = parser.parse_args()

    config = yaml.load(args.config)

    eclaire = EClaire(credentials=config["credentials"])

    wait_time = BASE_WAIT

    # Main program loop
    while True:
        for name, config in config["boards"].items():
            try:
                eclaire.process_board(config)
                wait_time = BASE_WAIT
            except (ResourceUnavailable, RequestException):
                log.warning("Waiting %d seconds before trying again", wait_time)
                time.sleep(wait_time)
                # exponential wait time up to MAX_WAIT on a timeout error
                wait_time = min(MAX_WAIT, wait_time * 2)

        log.info("-------")
        if args.run_once:
            break

        time.sleep(wait_time)
        if args.run_once:
            break


def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)-15s %(name)-15s %(levelname)-8s %(message)s"
    )
    logging.getLogger("requests").setLevel(logging.ERROR)


if __name__ == "__main__":
    main()
