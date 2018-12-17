# Copyright 2015 KOGAN.COM PTY LTD

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
import os
import pkg_resources
import subprocess
from tempfile import mktemp

from fpdf import FPDF
import qrcode


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
    process = subprocess.Popen(
        ['lpr', '-P', printer_name],
        stdin=subprocess.PIPE
    )

    process.communicate(pdf)

    if process.returncode != 0:
        raise PrintingError('Return code {}'.format(process.returncode))


def generate_pdf(card):
    """
    Make a PDF from a card

    :param card: dict from fetcher.py
    :return: Binary PDF buffer
    """
    from eclaire.base import SPECIAL_LABELS

    pdf = FPDF('L', 'mm', (62, 140))
    pdf.set_margins(2.8, 2.8, 2.8)
    pdf.set_auto_page_break(False, margin=0)

    pdf.add_page()

    font = pkg_resources.resource_filename('eclaire', 'font/Clairifont.ttf')
    pdf.add_font('Clairifont', fname=font, uni=True)
    pdf.set_font('Clairifont', size=48)

    pdf.multi_cell(0, 18, txt=card.name.upper(), align='L')

    qrcode = generate_qr_code(card.shortUrl)
    qrcode_file = mktemp(suffix='.png', prefix='trello_qr_')
    qrcode.save(qrcode_file)
    pdf.image(qrcode_file, 118, 35, 20, 20)
    os.unlink(qrcode_file)

    # May we never speak of this again.
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(0, 55, 140, 20, 'F')

    pdf.set_font('Clairifont', '', 16)
    pdf.set_y(-4)
    labels = ', '.join([label.name for label in card.labels
                        if label.name not in SPECIAL_LABELS])
    pdf.multi_cell(0, 0, labels, 0, 'R')

    return pdf.output(dest='S').encode('latin-1')


def generate_qr_code(url):
    """ Generate a QR Code for the given URL and return an Image file"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    return qr.make_image()
