#https://stackoverflow.com/questions/14928057/reportlab-text-background-size-doesnt-match-font-size

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import PageTemplate, Frame, NextPageTemplate, BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.units import cm

doc = SimpleDocTemplate("report.pdf",pagesize=letter,
                    rightMargin=30,leftMargin=30,
                    topMargin=30,bottomMargin=30)

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Table Top Black Back', fontName ='Helvetica',fontSize=14, leading=16,backColor = colors.black, textColor=colors.white, alignment=TA_LEFT))
styles.add(ParagraphStyle(name='Table Top Red Back', fontName ='Helvetica',fontSize=9, leading=12, backColor = colors.red, textColor=colors.black, alignment=TA_LEFT))

styleN = styles["BodyText"]

# Header
report = []
ptext = "SP"
report.append(Paragraph(ptext, styles["Normal"]))

##############################
# Table
##############################
csv_data = "SP_holders.csv"
csv_file = open(csv_data,"r")

table_data = []
for line in csv_file:
    str_line = line.strip();
    line_elems = str_line.split(",")
    print(line_elems)
    table_data.append(line_elems)
csv_file.close();

t=Table(table_data, rowHeights = len(table_data)*[0.5*cm])
t.setStyle(TableStyle([
#    ('BACKGROUND', (0, 0), (4, 0), colors.gray),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.gray),
    ('BOX', (0, 0), (-1, -1), 0.25, colors.gray),
]))

report.append(t)

#######################
report.append(Spacer(1, 24))
#######################

csv_data = "SP_summary.csv"
csv_file = open(csv_data,"r")

table_data = []
for line in csv_file:
    str_line = line.strip();
    line_elems = str_line.split(",")
    print(line_elems)
    table_data.append(line_elems)
csv_file.close();

t=Table(table_data, rowHeights = len(table_data)*[0.5*cm])
t.setStyle(TableStyle([
#    ('BACKGROUND', (0, 0), (4, 0), colors.gray),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.gray),
    ('BOX', (0, 0), (-1, -1), 0.25, colors.gray),
]))

report.append(t)

#######################
report.append(Spacer(1, 24))
#######################

##############################
# Chart
##############################
report.append(PageBreak())

chart = "SP_chart.png"
im = Image(chart,width=10*cm,height=3.8*cm)
report.append(im)

# Build Document
doc.build(report)
