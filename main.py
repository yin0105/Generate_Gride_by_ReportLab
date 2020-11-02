from reportlab.graphics.shapes import scale
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import *
from reportlab.lib.colors import *
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
import re, time


def generatePDF(filename, gridSize, paperSize, colorMajor, lineWidthMajor, colorMinor, lineWidthMinor, dotted=0, colorOuter="", lineWidthOuter=0, gutter=0, svg=[], svgNewColor='#999999'):
    canv = canvas.Canvas(filename+".pdf", paperSize)
    if colorOuter == "": colorOuter = colorMajor
    if lineWidthOuter == 0: lineWidthOuter = lineWidthMajor
    print(str(paperSize[0]))    
    print("len_0 = " + str(len(svg)))
    drawLine(canv, colorMinor, lineWidthMinor, paperSize, gridSize, gutter, 0, dotted, svg, svgNewColor=svgNewColor)
    drawLine(canv, colorMajor, lineWidthMajor, paperSize, gridSize, gutter, 1, svgNewColor=svgNewColor)
    drawLine(canv, colorOuter, lineWidthOuter, paperSize, gridSize, gutter, 2, svgNewColor=svgNewColor)
    # drawLine(canv, colorMajor, lineWidthMajor, paperSize, gridSize, gutter, 1)

    # drawing = svg2rlg("svg/1553857808.svg")
    # scaleXY = gridSize / max(drawing.width, drawing.height)
    # drawing.width = drawing.width * scaleXY
    # drawing.height = drawing.height * scaleXY
    # drawing.scale(scaleXY, scaleXY)

    # renderPDF.drawToFile(drawing, "file.pdf")
    # renderPM.drawToFile(drawing, "file.png", fmt="PNG")
    # renderPDF.draw(drawing, canv, 100, 100)
    
    canv.showPage()
    canv.save()

def changeSVGColor(svg, svgNewColor):
    with open(svg, 'r') as in_file:
        content = in_file.read()
        with open('temp.svg', 'w', newline='') as out_file:
            content = re.sub('#[f|F]{6}', '#######', content)
            content = re.sub('\"#\w{6}\"', '\"' + svgNewColor + '\"', content)
            content = re.sub('fill:#\w{6}', 'fill:' + svgNewColor + '', content)
            content = re.sub('stroke:#\w{6}', 'stroke:' + svgNewColor + '', content)
            content = re.sub('#{7}', '#FFFFFF', content)
            out_file.write(content)


def drawLine(canv, color, lineWidth, paperSize, gridSize, gutter, type, dotted=0, svg=[], svgNewColor='#999999'):
    print("len = " + str(len(svg)))
    canv.setStrokeColor(color)
    canv.setLineWidth(lineWidth)
    xStart = (paperSize[0] % (gridSize + gutter)) / 2
    yStart = (paperSize[1] % gridSize) / 2
    xlist = []
    ylist = []
    canv.setDash(1)
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
        xIndex = 0  
        if dotted == 1: canv.setDash(1, 2)  
        while xx < paperSize[0] - xStart - 0.01:
            yy = yStart
            yIndex = 0
            while yy < paperSize[1] - yStart - 0.01:
                xlist = []
                ylist = []
                for i in range(3):
                    xlist.append(xx + gridSize / 2 * i)
                    ylist.append(yy + gridSize / 2 * i)                
                
                if len(svg) > yIndex and len(svg[yIndex]) > xIndex:
                    # print(str(xIndex) + " :: " + svg[xIndex] + ".svg")
                    changeSVGColor(svg[yIndex][xIndex] + ".svg", svgNewColor=svgNewColor)
                    time.sleep(0.5)
                    drawing = svg2rlg('temp.svg')
                    scaleXY = gridSize / max(drawing.width, drawing.height)
                    drawing.width = drawing.width * scaleXY
                    drawing.height = drawing.height * scaleXY
                    drawing.scale(scaleXY, scaleXY)
                    renderPDF.draw(drawing, canv, xx, yy) 

                canv.grid(xlist,ylist)
                yy += gridSize
                yIndex += 1
            if gutter > 0: xlist.append(xx + gridSize)
            xx += gridSize + gutter
            xIndex += 1
        return
        
    canv.grid(xlist,ylist)
# svg=['svg/1553857808', 'svg/0ff41', 'svg/1553687147']
svg=[
['svg/1553857808', 'svg/0ff41', 'svg/1553687147'], # first row
['svg/1553687147'], # second row
['svg/1553857808', 'svg/0ff41'], # third row
]
generatePDF("temp", 33, A4, blue, 1, green, 0.3, 1, red, 3, gutter=10, svg=svg, svgNewColor='#BBBBBB')