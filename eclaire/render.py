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

import logging
import subprocess

import pkg_resources

from fpdf import FPDF

log = logging.getLogger(__name__)


class PrintingError(Exception):
    pass


def print_card(pdf, printer_name):
    """
    Send the PDF to the printer!

    Shells out to `lpr` to do the work.

    :param pdf: Binary PDF buffer
    :param printer_name: Name of the printer on the system (ie. CUPS name)
    """
    process = subprocess.Popen(["lpr", "-P", printer_name], stdin=subprocess.PIPE)

    process.communicate(pdf)

    if process.returncode != 0:
        raise PrintingError("Return code {}".format(process.returncode))


def generate_epic(title):
    pdf = FPDF("L", "mm", (62, 140))
    pdf.set_margins(2.8, 2.8, 2.8)
    pdf.set_auto_page_break(False, margin=0)

    pdf.add_page()

    font = pkg_resources.resource_filename("eclaire", "font/Clairifont.ttf")
    pdf.add_font("Clairifont", fname=font, uni=True)
    pdf.set_font("Clairifont", size=30)

    pdf.write(10, title)

    # May we never speak of this again.
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(0, 55, 140, 20, "F")

    pdf.set_font("Clairifont", "", 20)
    pdf.multi_cell(0, 20)
    pdf.set_y(40)
    pdf.write(10, "Due Date:                Live Date: \n")
    pdf.set_y(55)
    pdf.write(0, "Progress: ")
    pdf.set_font("arial", size=30)
    pdf.write(0, "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")

    return pdf.output(dest="S").encode("utf-8")
