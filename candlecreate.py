import itertools
from updMytime import updMytime
from myParsLine import getCandleFromSource
from myFile import myFile
from candleValues import candleValues

def candlecreate():
    files = myFile()
    files.myInit()
    #files.Qfiles['minFile'].write(files.source['f'].readline()) #первую строку переписываем, но только в минутный файл. мне надо, чтобы его понимал форексовый терминал
    #itertools.islice(files.source['f'],1)
    files.source['f'].readline()
    y = getCandleFromSource(files.source['f'].readline()) #вторую парсим чтоб задать стартовые значения (надо будет сделать это как-то изящнее)
    val = updMytime('000000','20010101') #TODO: убрать нахер отсюда, и сделать нормально
    val.d = date = olddate = y.date; val.t = time = oldtime = y.time
    candle = candleValues()
    candle.myInit(y)
    y.rememberOldDatatime(y, val)
    y.rememberOldCandle(y)
    j = j_min = 1
    itertools.islice(files.source['f'],2)
    for line in files.source['f']:
        y = getCandleFromSource(line)
        candle.updateMe(y,j_min, files, False) #update means file data update
        date = y.date
        time = y.time
        openVal = y.openVal
        hightVal = y.hightVal
        lowVal = y.lowVal
        closeVal = y.closeVal
        j = j +1; j_min = j_min +1 #c++ is crying
        val = updMytime(oldtime, olddate)
        y.rememberOldDatatime(y, val)
        oldtime = y.olddata['oldtime']
        olddate = y.olddata['olddate']
        while ((time > oldtime or date > olddate)): #таким вот образом обнаруживается дыра в исходных минутных данных, которая заполняется предыдущими свечками
            y.candle['auth'] = y.candle['auth'] + 1
            candle.updateMe(y,j_min, files, True)
            j_min = j_min +1
            val = updMytime(oldtime, olddate)
            y.rememberOldDatatime(y, val)
            oldtime = y.olddata['oldtime']
            olddate = y.olddata['olddate']
       #основная мысль: дыры в котировках появились за счет того, что в данный отрезок времени сделок небыло, следовательно мы их заполняем идентичными свечками, потому как ничего не менялось
       #возможны 100500 иных причин дырам в котировках, да ;) выходные и всяческие bank holydays например
       #возможно, апроксимация сработает лучше, но это будет видно уже при обучении
        y.rememberOldCandle(y)
        olDopenVal = openVal
        olDhightVal = hightVal
        olDlowVal = lowVal
        olDcloseVal = closeVal
        oldtime = time
        olddate = date
    files.myShutdowm()
    return files
    #print ("old " + str(j) + '\nnew ' + str(j_min))

