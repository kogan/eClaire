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


def generate_pdf(card):
    """
    Make a PDF from a card

    :param card: dict from fetcher.py
    :return: Binary PDF buffer
    """
    from eclaire.base import SPECIAL_LABELS, MAX_LABEL_CHARS

    pdf = FPDF("L", "mm", (62, 140))
    pdf.set_margins(2.8, 2.8, 2.8)
    pdf.set_auto_page_break(False, margin=0)

    pdf.add_page()

    font = pkg_resources.resource_filename("eclaire", "font/Clairifont.ttf")
    pdf.add_font("Clairifont", fname=font, uni=True)
    pdf.set_font("Clairifont", size=48)

    pdf.multi_cell(0, 18, txt=card.name.upper(), align="L")

    pdf.set_font("Clairifont", "", 16)
    pdf.set_y(-4)
    labels = ", ".join([label.name for label in card.labels if label.name not in SPECIAL_LABELS])[
        :MAX_LABEL_CHARS
    ]
    pdf.multi_cell(0, 0, labels, 0, "R")

    return pdf.output(dest="S").encode("latin-1")
