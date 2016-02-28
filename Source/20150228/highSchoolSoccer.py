# -*- coding: utf-8 -*-
import arcpy
import pandas as pd
import geocoder
import datetime

def getCoordinate(location_name):
    try:
        #地名から座標を取得する
        ret = geocoder.google(location_name)
    except KeyError, e:
        print "KeyError(%s)" % str(e)
        return

    return ret

def createPoint(name,points,year):

    #ジオコーディング
    loc = getCoordinate(name)

    if loc.lat is not None:
        point = arcpy.Point()
        point.X = loc.lng
        point.Y = loc.lat
        pointGeometry = arcpy.PointGeometry(point,spatial_reference)

        cur = arcpy.da.InsertCursor(infc, ["SHAPE@","Name","Point","Year"])

        #校名のあとに県などがついている場合、分解する
        if name.find(" ") > 0:
            if len(name.split(" ")) == 2:
                name,ken = name.split(" ")
            if len(name.split(" ")) == 3:
                name,ken,nihon = name.split(" ")
        cur.insertRow((pointGeometry,name,points,year))
        del cur
    else:
        print name + u"の座標がとれない"

        #多々良学園などの座標がとれないのでこれで対応
        if name != "":
            name = name + " " + u"日本"
            #浦和南 埼玉 日本とかだとだめなのでこの場合は南浦和にする
            if len(name.split(" ")) == 4:
                name,ken,nihon,nihon2 = name.split(" ")
                createPoint(name,points,year)
            else:
                createPoint(name,points,year)

#対象のフィーチャクラス
infc = "C:\ArcPySample\Soccer.gdb\HighShcool"
spatial_reference=arcpy.SpatialReference(4612)

#保存したHTML
html = 'http://www.tigerkaz.info/highschool/senshuken.html'

#HTMLを読込
dataframes = pd.io.html.read_html(html)

#表の部分を取得
table = pd.DataFrame(dataframes[0])

#カラム作成
table.columns = ['LINK','Time','Year','Champion','Prefecture','Time2','Finalist','Prefecture2','Best4','Prefecture3','Best4_2','Prefecture4']

schoolList = []

for key,row in table.iterrows():

    #年度を保持
    if row.Year.year != -1:
        year = row.Year.year

    #戦後の結果のみを対象とする
    if row.Year.year == datetime.datetime(1945,1,1).year:
        break

    if row.Champion == u"優勝":
        continue

    #両校優勝の場合、変なとこに優勝校の一つが入っているので
    if isinstance(row.Champion, float):
        yusho = row.LINK

        if yusho.find("(") > 0:

            yusho = yusho[0:yusho.find("(")]

        #帝京とかだと中国にジオコーディングされてしまうので
        yusho = yusho  + " " + u"日本"

        schoolList.append([yusho,"","","",year])
    else:
        #校名 + 県名でジオコーディングする。国見とかだと変なとこに飛ぶので。
        #ただし、これをやると高校から微妙に座標がずれる。が、とりあえず近くなのでよしとする。
        yusho = row.Champion   + " " + row.Prefecture

        if yusho.find("(") > 0:
            yusho = yusho[0:yusho.find("(")] + " " + row.Prefecture

        #両校優勝の場合列がずれているので
        if row.Finalist == u"(両校優勝)":
            best4 = row.Prefecture2 + " " + row.Best4
            best4_2 = row.Prefecture3 + " " + row.Best4_2
            schoolList.append([yusho,"",best4,best4_2,row.Year.year])
        else:
            junYusho = row.Finalist + " " + row.Prefecture2
            best4 = row.Best4 + " " + row.Prefecture3
            best4_2 = row.Best4_2 + " " + row.Prefecture4
            schoolList.append([yusho,junYusho,best4,best4_2,row.Year.year])

#リストをデータフレームに変換
schooDf = pd.DataFrame(schoolList)
schooDf.columns = ['Champion','Finalist','Best4','Best4_2','Year']

for key,rowS in schooDf.iterrows():
    #ポイントをプロット
    createPoint(rowS.Champion,10,rowS.Year)
    createPoint(rowS.Finalist,5,rowS.Year)
    createPoint(rowS.Best4,3,rowS.Year)
    createPoint(rowS.Best4_2,3,rowS.Year)