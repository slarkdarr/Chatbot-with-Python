import re

formatTanggal1 = '([0-3]?[0-9]) ([a-zA-Z]+) ([0-9]{4})' #tanggal bulan tahun
formatTanggal2 = '([a-zA-Z]+) ([0-3]?[0-9]) ([0-9]{4})' #bulan tanggal tahun
formatTanggal3 = '([0-3][0-9])/([0-9][0-9])/([0-9]{4})' #DD/MM/YYYY
formatJenis = '([Tt]ubes|[Tt]ucil|[Kk]uis|[Uu]jian|[Pp]raktikum)'

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
#test9 = "Halo bot, tolong ingetin kalau ada Tucil IF2220 Bab 2 pada 22/04/21"
