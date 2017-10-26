from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm

doc = SimpleDocTemplate("report.pdf",pagesize=landscape(A4),
                        rightMargin=30,leftMargin=30,
                        topMargin=30,bottomMargin=30)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_LEFT, fontSize=9))

Story=[]

##############################
# Heading
##############################

ptext = '<font size=12>Ticker: SP</font>'
Story.append(Paragraph(ptext, styles["Normal"]))

ptext = '''
<seq>. </seq>Some Text<br/>
<seq>. </seq>Some more test Text
'''
Story.append(Paragraph(ptext, styles["Bullet"]))

ptext='<bullet>&bull;</bullet>Some Text'
Story.append(Paragraph(ptext, styles["Bullet"]))

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

t=Table(table_data)
t.setStyle(TableStyle([
#    ('BACKGROUND', (0, 0), (4, 0), colors.gray),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.gray),
    ('BOX', (0, 0), (-1, -1), 0.25, colors.gray),
]))

Story.append(t)

csv_data = "SP_summary.csv"
csv_file = open(csv_data,"r")

table_data = []
for line in csv_file:
    str_line = line.strip();
    line_elems = str_line.split(",")
    print(line_elems)
    table_data.append(line_elems)
csv_file.close();

t=Table(table_data)
t.setStyle(TableStyle([
#    ('BACKGROUND', (0, 0), (4, 0), colors.gray),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.gray),
    ('BOX', (0, 0), (-1, -1), 0.25, colors.gray),
]))

Story.append(t)


##############################
# Chart
##############################
chart = "SP_chart.png"
im = Image(chart)
Story.append(im)


doc.build(Story)
