from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
c = canvas.Canvas('report.pdf')
c.drawImage('SP_chart.png', 10, 10, 10*cm, 3.75*cm)
c.showPage()
c.save()
