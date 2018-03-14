import pandas as pd
from sys import argv
import pyperclip

script = argv

xlsFile = 'tables.xlsx'
sheets = ['cerebro','implant','base']
first  = True
choice = 0

while choice<1 or choice>len(sheets): 
    if first:
        print("\nChoose a Table to Generate")
        for i,sheetName in enumerate(sheets):
            print('{}: {}'.format(i+1,sheetName))
        # print("\nChoose a Table to Generate\n1: Cerebro\n2: Implant\n3: Base Station\n")
        typed = input("Choice = ")
        first = False
    else:
        print("\"{}\" is not an option".format(typed))
        typed = input("Choice = ")  
    try:
        choice = int(typed)
    except:
        choice = 0


sheet = sheets[choice-1]

def getColWidths(table):
    colMax = []
    for cols in table:
        lengths = []
        for entry in table[cols]:
            lengths.append(len(entry))
        colMax.append(max(lengths) if max(lengths)>len(cols) else len(cols) )
    return colMax

def printDivider(colWidths,emptyVec=[],doubleDash = False):
    dash = "=" if doubleDash else "-"
    index = 0
    dividerString = ""
    for width in colWidths:
        insert = dash
        if emptyVec:
            if emptyVec[index]:
                insert = " "
        dividerString += "{0}{1}".format("+",(width+2)*insert)
        index += 1
    dividerString += "+\n"
    return dividerString

def printContents(table,colWidths,isHeader=False,**kwds):
    contentString  = "| "
    index = 0
    blankCols = []
    for cols in table:
        content =  cols if isHeader else table.loc[row,cols]
        if content=="":
            blankCols.append(True)
        else:
            blankCols.append(False)
        fill = colWidths[index]-len(content)
        contentString += "{0}{1}{2}".format(content,(fill)*" "," | ")
        index +=1
    contentString += "\n"
    return contentString,blankCols


table = pd.read_excel(xlsFile,usecols=4,sheet_name=sheet).fillna("").astype(str) #read in table from excel file
widths = getColWidths(table) # get the maximum content width of each column

#print header
outputString = printDivider(widths) #first divider
outputString += printContents(table,widths,isHeader=True)[0] #header
outputString += printDivider(widths,doubleDash=True) #header divider

#print table contents
for row in range(len(table)):
    valString,blanks = printContents(table,widths)
    outputString += printDivider(widths,blanks)*(row != 0) + valString
outputString += printDivider(widths) #final divider

#copy string to clipboard
pyperclip.copy(outputString)
print("\n\"{}\" sheet copied to clipboard!\n".format(sheet))
