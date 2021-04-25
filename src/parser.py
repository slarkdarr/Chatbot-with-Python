import re

formatTanggal1 = '([0-3]?[0-9]) ([a-zA-Z]+) ([0-9]{4})' #tanggal bulan tahun
formatTanggal2 = '([a-zA-Z]+) ([0-3]?[0-9]) ([0-9]{4})' #bulan tanggal tahun
formatTanggal3 = '([0-3][0-9])/([0-9][0-9])/([0-9]{4})' #DD/MM/YYYY
formatJenis = '([Tt]ubes|[Tt]ucil|[Kk]uis|[Uu]jian|[Pp]raktikum)'

def bm(text, pattern):
    lastx = {}
    lenP = len(pattern)
    lenT = len(text)
    i = lenP-1
    j = lenP-1
    found = False
    
    while (i < lenT and not found):
        j = lenP-1
        found = True
        #print(text)
        #print(" "*(i-(lenP-1))+pattern)
        #print(i)
        while (found and j >= 0):
            if (pattern[j] != text[i]):
                #print(j)
                found = False
            else:
                i -= 1
                j -= 1
        
        if (not found):
            if (text[i] not in lastx.keys()):
                k = lenP-1
                while (k >= 0 and pattern[k] != text[i]):
                    k -= 1
                lastx[text[i]] = k
                    
            if (lastx[text[i]] >= 0):
                if (lastx[text[i]] < j):
                    i += j-lastx[text[i]]
                    #print("case 1")
                else:
                    i += lenP-j
                    #print("case 2")
            else:
                i += lenP
                #print("case 3") 
        #print()
        
        if (i >= lenT):
            return -1
    
    i += 1
    #print(text)
    #print(" "*(i)+pattern)
    #print()
    
    return i

def objek(text):
    try:
        o = re.search(formatJenis+' (.+?) pada', text).group(2)
    except AttributeError:
        try:
            o = re.search(formatJenis+' (.+?)$', text).group(2)
        except AttributeError:
            o = None
        
    return o

def matkul(text):
    try:
        s = re.search('([A-Z]{2}[0-9]{4}) ?(.*)$', text).group(1)
    except AttributeError:
        s = None
        
    return s

def topik(text):
    try:
        t = re.search('([A-Z]{2}[0-9]{4}) ?(.+)$', text).group(2)
    except AttributeError:
        t = None
        
    return t
    
def jenis(text):
    try:
        j = re.search(formatJenis, text).group(0)
    except AttributeError:
        try:
            j = re.search('[Dd]eadline', text).group(0)
        except AttributeError:
            j = None
        
    return j

def tanggalPada(text):
    try:
        tp = re.search('pada ([a-zA-Z]+), (.+?)$', text).group(2)
    except AttributeError:
        try:
            tp = re.search('pada (.+?),', text).group(1)
        except AttributeError:
            try:
                tp = re.search('pada (.+?)$', text).group(1)
            except AttributeError:
                tp = None
        
    return tp
    
def tanggalTipe(text):
    try:
        tp = re.search(formatTanggal1, text).group(0)
        type = 1
    except AttributeError:
        try:
            tp = re.search(formatTanggal2, text).group(0)
            type = 2
        except AttributeError:
            try:
                tp = re.search(formatTanggal3, text).group(0)
                type = 3
            except AttributeError:
                type = None
                
    return type

def duaTanggal(text):
    try:
        # /(<formatTanggal1>|<formatTanggal2>|<formatTanggal3>) .+ (<formatTanggal1>|<formatTanggal2>|<formatTanggal3>)/g
        dt = re.search('('+formatTanggal1+'|'+formatTanggal2+'|'+formatTanggal3+') .+ ('+formatTanggal1+'|'+formatTanggal2+'|'+formatTanggal3+')', text)
        t1 = dt.group(1)
        t2 = dt.group(11)
    except AttributeError:
        t1 = None
        t2 = None
    
    return t1, t2
                
def translateTanggal(text):
    try:
        tp = re.search(formatTanggal1, text)
        d = tp.group(1)
        m = tp.group(2)
        y = tp.group(3)
        
        tanggal = d+" "+translateBulan(m)+" "+y
    except AttributeError:
        try:
            tp = re.search(formatTanggal2, text)
            d = tp.group(2)
            m = tp.group(1)
            y = tp.group(3)
        
            tanggal = d+" "+translateBulan(m)+" "+y
        except AttributeError:
            tanggal = text
        
    return tanggal
    
def pertanyaan(text):
    try:
        tp = re.search('?$', text).group(0)
    except:
        tp = None
    
    return (tp != None)
    
def task(text):
    try:
        tp = int(re.search('[Tt]ask ([0-9]+)', text).group(1))
    except AttributeError:
        tp = None
        
    return None
    
def translateBulan(bulan):
    listbulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    listmonth = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    try:
        id = listbulan.index(bulan)
        month = listmonth[id]
    except:
        month = None
    
    return month
    
#test1 = "tolong ingetin ada Tubes IF2211 String Matching pada 11 April 2021"
#test2 = "Kuis IF2230 pada 14/04/2021"
#test3 = "Tolong ingatkan ada Ujian IF2240 Bab 10 pada Senin, 12 Mei 2021"
#test4 = "Apa saja deadline yang dimiliki sejauh ini?"
#test5 = "3 minggu ke depan ada kuis apa saja?"
#test6 = "Ada kuis apa saja untuk 3 minggu ke depan?"
#test7 = "Apa saja deadline antara 03/04/2021 sampai 15/04/2021?"
#test8 = "Tubes IF2211 String Matching pada 14 April 2021"
#test9 = "Halo bot, tolong ingetin kalau ada Tucil IF2220 Bab 2 pada 22/04/2021"
#test10 = "Apa saja deadline antara 03/04/2021 sampai 15/04/2021?"
#test11 = "Apa saja deadline antara 03 April 2021 sampai 15/04/2021?"
#test12 = "Apa saja deadline antara 03/04/2021 sampai April 15 2021?"
text1 = "abcdefdbaec"
pattern1 = "bae"
text2 = "a pattern matching algorithm"
pattern2 = "rithm"
text3 = "bxaxyucwax"
pattern3 = "cwax"