#!/usr/bin/python

import subprocess
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def disk_usage():
        p = subprocess.Popen("df -h", shell=True, stdout=subprocess.PIPE)
        return p.stdout.readlines()


def create_pdf(input,output="disk_report.pdf"):
        now = datetime.datetime.today()
        date = now.strftime("%h %d %Y %H:%M:%S")
        c = canvas.Canvas(output)
        textobject = c.beginText()
        textobject.setTextOrigin(inch, 11*inch)
        textobject.textLines('''Disk Capacity Report %s''' % date)
        for line in input:
                textobject.textLine(line.strip())
        c.drawText(textobject)
        c.showPage()
        c.save()

report = disk_usage()
create_pdf(report)
