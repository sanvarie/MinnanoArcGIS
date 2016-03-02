# -*- coding: utf-8 -*-
import arcpy
import pandas as pd

def updateAttribute(row,cur,conTable):
    row.setValue("NAME", conTable[0])
    row.setValue("CAPITAL", conTable[2])
    row.setValue("LANGUAGE", conTable[4])

    AreaSquere = conTable[5]
    #変な文字列がまじっているので
    if isinstance(AreaSquere, float):
        row.setValue("AREASQUARE", AreaSquere)
    elif isinstance(AreaSquere, long):
        row.setValue("AREASQUARE", AreaSquere)
    #なぜかdatetimeとして認識されるものがあるのでそれは無視
    elif isinstance(AreaSquere, datetime.date):
        pass
    else:
        if AreaSquere.find(u"平方キロ") > -1:
            row.setValue("AREASQUARE", AreaSquere[0:AreaSquere.find(u"平方キロ")])

    population = conTable[6]
    #変な文字列がまじっているので
    if isinstance(population, float):
        row.setValue("POPULATION", population)
    else:
        if population.find(u"約") > -1:
            if population.find(u"人") > -1:
                population = population[population.find(u"約")+1:]
                row.setValue("POPULATION", population[0:population.find(u"人")])
            else:
                row.setValue("POPULATION", population[population.find(u"約")+1:])
        elif population.find(u"人") > -1:
            row.setValue("POPULATION", population[0:population.find(u"人")])

    currency = conTable[7]
    if currency.find(u"（") > 1:
        row.setValue("CURRENCY", currency[0:currency.find(u"（")])
    else:
        row.setValue("CURRENCY", currency)

    cur.updateRow(row)

tableList = []
countryList = []

#対象のURL
countryList.append("http://www.mofa.go.jp/mofaj/kids/ichiran/i_europe.html")
countryList.append("http://www.mofa.go.jp/mofaj/kids/ichiran/i_africa.html")
countryList.append("http://www.mofa.go.jp/mofaj/kids/ichiran/i_chuto.html")
countryList.append("http://www.mofa.go.jp/mofaj/kids/ichiran/i_asia.html")
countryList.append("http://www.mofa.go.jp/mofaj/kids/ichiran/i_oceania.html")
countryList.append("http://www.mofa.go.jp/mofaj/kids/ichiran/i_n_america.html")
countryList.append("http://www.mofa.go.jp/mofaj/kids/ichiran/i_latinamerica.html")

#対象のフィーチャクラス
arcpy.env.workspace = "C:\ArcPySample\Map.gdb"
spatial_reference=arcpy.SpatialReference(4326)

for l in countryList:
    #HTMLを読込
    df = pd.io.html.read_html(l)
    tableList.append(df[0])

#データフレームを結合
conTable = pd.concat(tableList, ignore_index=True)
conTable.columns = ["NAME","ENGLISH_NAME","CAPITAL","INDE_YEAR","LANGUAGE","AREASQUARE","POPULATION","CURRENCY"]

for i in conTable.index:
    dfEnglishName = conTable.ix[i][1]
    cursor = arcpy.UpdateCursor("WorldMap")
    for row in cursor:
        if dfEnglishName == row.NAME_EN:
            updateAttribute(row,cursor,conTable.ix[i])
        #色々力技
        elif dfEnglishName.find("of") > -1:
            if dfEnglishName.find("Australia") > -1 and row.NAME_EN.find("Australia") > -1:
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName.find("Vatican") > -1 and row.NAME_EN.find("Vatican") > -1:
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName.find("Hungary") > -1 and row.NAME_EN.find("Hungary") > -1:
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName.find("Verde") > -1 and row.NAME_EN.find("Verde") > -1:
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName.find("Gambia") > -1 and row.NAME_EN.find("Gambia") > -1:
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName.find("Comoros") > -1 and row.NAME_EN.find("Comoros") > -1:
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName.find("Principe") > -1 and row.NAME_EN.find("Principe") > -1:
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName.find("Nepal") > -1 and row.NAME_EN.find("Nepal") > -1:
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName.find("Viet") > -1 and row.NAME_EN.find("Viet") > -1:
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName.find("Bahamas") > -1 and row.NAME_EN.find("Bahamas") > -1:
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName == "Republic of Guinea" and row.NAME_EN == "Republic of Guinea":
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName == "Independent State of Papua New Guinea" and row.NAME_EN == "Independent State of Papua New Guinea":
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName.find("Cote") > -1  and row.NAME_EN == "Republic of Ivory Coast":
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName == "Republic of Congo" and row.NAME_EN == "Republic of Congo":
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName == "Democratic Republic of the Congo" and row.NAME_EN == "Democratic Republic of the Congo":
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName.find("Togo") > -1 and row.NAME_EN == "Togolese Republic":
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName.find("Lebanon") > -1 and row.NAME_EN == "Lebanese Republic":
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName == "Republic of Korea" and row.NAME_EN == "Republic of Korea":
                updateAttribute(row,cursor,conTable.ix[i])
            elif dfEnglishName.find(row.NAME_EN[row.NAME_EN.find("of")+3:]) > -1 and row.NAME_EN.find("of") > -1 \
                 and dfEnglishName != "Republic of Korea" and dfEnglishName != "Republic of Congo" and dfEnglishName != "Independent State of Papua New Guinea" \
                 and dfEnglishName != "Republic of Equatorial Guinea" and dfEnglishName != "Republic of Guinea-Bissau" and dfEnglishName != "Democratic Republic of the Congo":
                updateAttribute(row,cursor,conTable.ix[i])
        elif dfEnglishName.find("Spain") > -1 and row.NAME_EN.find("Spain") > -1:
                updateAttribute(row,cursor,conTable.ix[i])
        elif dfEnglishName.find("Brunei") > -1 and row.NAME_EN.find("Brunei") > -1:
            updateAttribute(row,cursor,conTable.ix[i])
        elif dfEnglishName.find("Nevis") > -1 and row.NAME_EN.find("Nevis") > -1:
            updateAttribute(row,cursor,conTable.ix[i])
        elif row.NAME_EN.find(dfEnglishName) > -1 and row.NAME_EN.find("Kingdom") == -1  and dfEnglishName.find("of") == -1 \
             and row.NAME_EN != "South Georgia and South Sandwich Islands" and row.NAME_EN != "Indian Ocean Territories" and row.NAME_EN != "British Indian Ocean Territory":
            updateAttribute(row,cursor,conTable.ix[i])