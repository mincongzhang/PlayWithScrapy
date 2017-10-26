#https://stackoverflow.com/questions/14928057/reportlab-text-background-size-doesnt-match-font-size

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import PageTemplate, Frame, NextPageTemplate, BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.units import cm

OUT_PATH = "/home/user/mizhang/hackathon/crawler/out/"
DELIM = "|"

def create_table(report,filename):
    if not os.path.isfile(filename):
        print("File not exist ["+filename+"]")
        return False

    csv_file = open(filename,"r")
    table_data = []
    for line in csv_file:
        str_line = line.strip();
        line_elems = str_line.split(DELIM)
        print(line_elems)
        table_data.append(line_elems)

    csv_file.close();

    t=Table(table_data, rowHeights = len(table_data)*[0.5*cm])
    t.setStyle(TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.gray),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.gray),
                ]))
    report.append(t)

    report.append(Spacer(1, 24))
    return True



doc = SimpleDocTemplate(OUT_PATH+"report.pdf",pagesize=letter,
                    rightMargin=30,leftMargin=30,
                    topMargin=30,bottomMargin=30)

styles=getSampleStyleSheet()

# Begin of the report
report = []

tickers = []
ticker_file = open(OUT_PATH+"tickers.txt","r")
for line in ticker_file:
    tickers.append(line.strip())
ticker_file.close();

for ticker in tickers:
    holders_file = OUT_PATH+ticker+"_holders.csv"
    summary_file = OUT_PATH+ticker+"_summary.csv"

    if not os.path.isfile(holders_file) or not os.path.isfile(summary_file):
        continue

    report.append(Paragraph("Ticker: "+ticker, styles["Normal"]))
    report.append(Spacer(1, 24))

    ##############################
    # Table
    ##############################
    success = False
    success |= create_table(report,summary_file)
    success |= create_table(report,holders_file)

    if not success:
        continue

    ##############################
    # Chart
    ##############################
    chart = OUT_PATH+ticker+"_chart.png"
    if os.path.isfile(chart):
        im = Image(chart,width=10*cm,height=3.8*cm)
        report.append(im)

    report.append(PageBreak())


# Build Document
doc.build(report)

