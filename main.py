from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import *
from reportlab.lib.colors import *

def generatePDF(filename, gridSize, paperSize, colorMajor, lineWidthMajor, colorMinor, lineWidthMinor, dotted=0, colorOuter="", lineWidthOuter=0, gutter=0):
    canv = canvas.Canvas(filename+".pdf", paperSize)
    if colorOuter == "": colorOuter = colorMajor
    if lineWidthOuter == 0: lineWidthOuter = lineWidthMajor
    print(str(paperSize[0]))
    drawLine(canv, colorMinor, lineWidthMinor, paperSize, gridSize, gutter, 0)
    drawLine(canv, colorMajor, lineWidthMajor, paperSize, gridSize, gutter, 1)
    drawLine(canv, colorOuter, lineWidthOuter, paperSize, gridSize, gutter, 2)
    # drawLine(canv, colorMajor, lineWidthMajor, paperSize, gridSize, gutter, 1)
    canv.showPage()
    canv.save()

def drawLine(canv, color, lineWidth, paperSize, gridSize, gutter, type, dotted=0):
    canv.setStrokeColor(color)
    canv.setLineWidth(lineWidth)
    xStart = (paperSize[0] % (gridSize + gutter)) / 2
    yStart = (paperSize[1] % gridSize) / 2
    xlist = []
    ylist = []
    if type == 2:
        # outer
        xlist.append(xStart)
        xlist.append(paperSize[0] - xStart)
        ylist.append(yStart)
        ylist.append(paperSize[1] - yStart)
    elif type == 1:
        # major
        xx = xStart
        while xx < paperSize[0] - xStart - 0.01:
            xlist.append(xx)
            if gutter > 0: xlist.append(xx + gridSize)
            xx += gridSize + gutter
        xlist.append(paperSize[0] - xStart)
        
        yy = yStart
        while yy < paperSize[1] - yStart + 0.01:
            ylist.append(yy)
            yy += gridSize
    elif type == 0:
        # minor
        xx = xStart        
        while xx < paperSize[0] - xStart - 0.01:
            yy = yStart
            while yy < paperSize[1] - yStart - 0.01:
                xlist = []
                ylist = []
                for i in range(3):
                    xlist.append(xx + gridSize / 2 * i)
                    ylist.append(yy + gridSize / 2 * i)
                canv.grid(xlist,ylist)
                yy += gridSize
            if gutter > 0: xlist.append(xx + gridSize)
            xx += gridSize + gutter
        return
        
    canv.grid(xlist,ylist)

generatePDF("temp", 33, A4, blue, 1, yellow, 0.3, 0, red, 3, gutter=10)