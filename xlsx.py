import xlsxwriter as xl


def writeItem(csitem):
    wbook = xl.Workbook(r'C:\Work\Python\buffsteamsorter\db.xlsx')
    page = wbook.add_worksheet("Items")

    row = 0
    clm = 0

    page.set_column("A:A", 10)
