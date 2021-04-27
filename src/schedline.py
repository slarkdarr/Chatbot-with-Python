import os
import datetime
import parser as p
from flask import Flask, render_template, flash, request, url_for, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')#, methods = ['GET', 'POST'])
def mainPage():
    #if request.method == "POST":
    #    n = request.form.get("message")
    
    return render_template('mainpage.html')
    
def processInput(text):
    text = text.strip()
    deadlineFlag = max(p.bm(text, "deadline"), p.bm(text, "Deadline"))
    kuisFlag = max(p.bm(text, "kuis"), p.bm(text, "Kuis"))
    tubesFlag = max(p.bm(text, "tubes"), p.bm(text, "Tubes"))
    tucilFlag = max(p.bm(text, "tucil"), p.bm(text, "Tucil"))
    ujianFlag = max(p.bm(text, "ujian"), p.bm(text, "Ujian"))
    praktikumFlag = max(p.bm(text, "praktikum"), p.bm(text, "Praktikum"))
    tugasFlag = max(p.bm(text, "tugas"), p.bm(text, "Tugas"))
    kapanFlag = max(p.bm(text, "kapan"), p.bm(text, "Kapan"))
    pertanyaanFlag = (p.bm(text, "?") == len(text)-1)
    undurFlag = max(p.bm(text, "undur"), p.bm(text, "Undur"))
    selesaiFlag = max(p.bm(text, "selesai"), p.bm(text, "Selesai"))
    menyelesaikanFlag = max(p.bm(text, "menyelesaikan"), p.bm(text, "Menyelesaikan"))
    
    if (pertanyaanFlag):
        if (kapanFlag != -1):
            print("Kapan")
            #read tasks
            #check parameter tipe (kuis/tubes/dll/none)
            #iterate tasks
            #jika tipe sama atau tipe none, tambahkan deadline dan tipe ke response
            #write response ke logs.txt
        elif (deadlineFlag != -1 or kuisFlag != -1 or tubesFlag != -1 or tucilFlag != -1 or ujianFlag != -1 or praktikumFlag != -1 or tugasFlag != -1):
            hariIniFlag = max(p.bm(text, "hari ini"), p.bm(text, "Hari ini"))
            hariFlag = p.bm(text, "hari")
            mingguFlag = p.bm(text, "minggu")
            today = datetime.datetime.now().date()
            mind = today
            maxd = None
            if (hariIniFlag != -1):
                maxd = today
            elif (hariFlag != -1):
                n = p.nWaktu(text)
                maxd = today+datetime.timedelta(days=n)
            elif (mingguFlag != -1):
                n = p.nWaktu(text)
                maxd = today+datetime.timedelta(days=7*n)
            else:
                d1, d2 = p.duaTanggal(text)
                mind = p.toDateObj(d1)
                maxd = p.toDateObj(d2)
            
            m = p.matkul(text)
            print(tugasFlag)
            if kuisFlag != -1:
                j = text[kuisFlag:kuisFlag+4].capitalize()
            elif tubesFlag != -1:
                j = text[tubesFlag:tubesFlag+5].capitalize()
            elif tucilFlag != -1:
                j = text[tucilFlag:tucilFlag+5].capitalize()
            elif ujianFlag != -1:
                j = text[ujianFlag:ujianFlag+5].capitalize()
            elif praktikumFlag != -1:
                j = text[praktikumFlag:praktikumFlag+9].capitalize()
            elif tugasFlag != -1:
                j = text[tugasFlag:tugasFlag+5].capitalize()
            else:
                j = None
            now = datetime.datetime.now()
            f = open("../data/logs.txt", "a+")
            body = responseBody(mindate=mind, maxdate=maxd, matkul=m, jenis=j)
            if (body != ""):
                response = "<b>[DAFTAR DEADLINE]</b><br>"+body
            else:
                response = "Tidak ada"
            log = "B"+now.strftime("%m/%d/%Y %H:%M:%S")+response+"\n"
            f.write(log)
            f.close()
        else:
            print("Bad command")
            #error handling
    
    elif (undurFlag != -1):
        print("undur")
        #read task number
        #read tasks
        #open file tasks.txt, write
        #rewrite tasks except for task number n
    
    elif (kuisFlag != -1 or tubesFlag != -1 or tucilFlag != -1 or ujianFlag != -1 or praktikumFlag != -1):
        o = p.objek(text)
        m = p.matkul(o)
        t = p.topik(o)
        if kuisFlag != -1:
            j = text[kuisFlag:kuisFlag+4].capitalize()
        elif tubesFlag != -1:
            j = text[tubesFlag:tubesFlag+5].capitalize()
        elif tucilFlag != -1:
            j = text[tucilFlag:tucilFlag+5].capitalize()
        elif ujianFlag != -1:
            j = text[ujianFlag:ujianFlag+5].capitalize()
        else:
            j = text[praktikumFlag:praktikumFlag+9].capitalize()
        
        #read, process tanggal
        tp = p.tanggalPada(text)
        date = p.toDateObj(tp)
        
        if (m == None or t == None or j == None or tp == None):
            print("Bad command")
            #error handling
        else:
            #write task, format "<Jenis>---<tanggal>---<matkul>---<topik>" dengan "---" sebagai separator karena kemungkinan kecil untuk menjadi input
            task = j.capitalize()+"---"+date.strftime("%m/%d/%Y")+"---"+m+"---"+t.title()+"\n"
        
            f = open("../data/tasks.txt", "a+")
            f.write(task)
            f.close()
        
            now = datetime.datetime.now()
            f = open("../data/logs.txt", "a+")
            response = "<b>[TASK BERHASIL DICATAT]</b><br>"
            response += responseBody()
            log = "B"+now.strftime("%m/%d/%Y %H:%M:%S")+response+"\n"
            f.write(log)
            f.close()
        
def loadTasks():
    #read data
    f = open("../data/tasks.txt", "r")
    lines = f.readlines()
    f.close()
    
    #gunakan dictionary, {<date1>: [<task1>, <task2>, ...], <date2>: [<task3>, <task4>, ...], ...}
    tasks = {}
    
    for line in lines:
        #abaikan newline
        line = line.replace("\n", "")
        #separator "---"
        info = line.split("---")
        if (info[1] in tasks.keys()):
            #jika tanggal sudah di dictionary, tambahkan task ke values
            tasks[info[1]].append([info[0], info[2], info[3]])
        else:
            #jika tidak, inisialisasi entri tanggal di dictionary dengan value = task kini
            tasks[info[1]] = [[info[0], info[2], info[3]]]
    
    return tasks
    
def responseBody(mindate=None, maxdate=None, matkul=None, jenis=None):
    body = ""
    tasks = loadTasks()
    
    times = sorted(list(tasks.keys()))
    i = 1
    for time in times:
        date = datetime.datetime.strptime(time, "%m/%d/%Y").date()
        validDate = True
        if (mindate != None):
            validDate = validDate and (date >= mindate)
        if (maxdate != None):
            validDate = validDate and (date <= maxdate)
        
        for task in tasks[time]:
            validObj = True
            if (matkul != None):
                validObj = validObj and (matkul == task[1])
            if (jenis != None):
                if (jenis != "Tugas"):
                    validObj = validObj and (jenis == task[0])
                else:
                    validObj = validObj and ((task[0] == "Tubes") or (task[0] == "Tucil"))
            
            if (validDate and validObj):
                body += "(ID: "+str(i)+") "+date.strftime("%d/%m/%Y")+" - "+task[1]+" - "+task[0]+" - "+task[2]+"<br>"
            i += 1
            
    return body
    
@app.route('/Chat', methods = ['GET', 'POST'])
def chatPage():
    f = open("../data/logs.txt", "a")
    
    if request.method == "POST":
        msg = request.form.get("messageInput").lstrip()
        if (msg.count(" ") < len(msg)):
            now = datetime.datetime.now()
            log = "U"+now.strftime("%m/%d/%Y %H:%M:%S")+msg+"\n"
            f.write(log)
            f.close()
            processInput(msg)
    
    f = open("../data/logs.txt", "r")
    chatLogs = f.readlines()
    
    html = ''
    html += '<!DOCTYPE html>\n'
    html += '<html>\n'
    html += '    <head>\n'
    html += '        <title>SchedLINE</title>\n'
    html += '        <style>\n'
    html += '            div.chatscroll {\n'
    html += '                overflow-y: auto;\n'
    html += '                border: 1px solid black;\n'
    html += '                height: 500px;\n'
    html += '                width: 400px;\n'
    html += '                display: flex;\n'
    html += '                flex-direction: column-reverse;\n'
    html += '            }\n'
    html += '            table.chat {\n'
    html += '                width: 400px;\n'
    html += '                border-collapse: separate;\n'
    html += '                border-spacing: 10px 0px;\n'
    html += '            }\n'
    html += '            p.datebubble {\n'
    html += '                border-radius: 5px 5px 5px 5px;\n'
    html += '                background: #d9d9d9;\n'
    html += '                padding: 3px;\n'
    html += '                text-align: center;\n'
    html += '                width: fit-content;\n'
    html += '                float: center;\n'
    html += '                font-weight: normal;\n'
    html += '                font-family: Arial;\n'
    html += '                font-size: 11px;\n'
    html += '            }\n'
    html += '            p.botbubble {\n'
    html += '                border-radius: 5px 20px 20px 20px;\n'
    html += '                background: #e3e3e3;\n'
    html += '                padding: 10px;\n'
    html += '                text-align: left;\n'
    html += '                width: fit-content;\n'
    html += '                max-width: 320px;\n'
    html += '                float: left;\n'
    html += '                font-weight: normal;\n'
    html += '                font-family: Arial;\n'
    html += '                font-size: 14px;\n'
    html += '                word-wrap: break-word;\n'
    html += '            }\n'
    html += '            p.bottime {\n'
    html += '                text-align: left;\n'
    html += '                vertical-align: text-bottom;\n'
    html += '                float: left;\n'
    html += '                width: fit-content;\n'
    html += '                font-weight: normal;\n'
    html += '                font-family: Arial;\n'
    html += '                font-size: 9px;\n'
    html += '                color: #3c3c3c;\n'
    html += '                padding: 5px;\n'
    html += '            }\n'
    html += '            p.userbubble {\n'
    html += '                border-radius: 20px 5px 20px 20px;\n'
    html += '                background: #d0e3bc;\n'
    html += '                padding: 10px;\n'
    html += '                text-align: right;\n'
    html += '                width: fit-content;\n'
    html += '                max-width: 320px;\n'
    html += '                float: right;\n'
    html += '                font-weight: normal;\n'
    html += '                font-family: Arial;\n'
    html += '                font-size: 14px;\n'
    html += '                word-wrap: break-word;\n'
    html += '            }\n'
    html += '            p.usertime {\n'
    html += '                text-align: right;\n'
    html += '                vertical-align: bottom;\n'
    html += '                float: right;\n'
    html += '                width: fit-content;\n'
    html += '                font-weight: normal;\n'
    html += '                font-family: Arial;\n'
    html += '                font-size: 9px;\n'
    html += '                color: #3c3c3c;\n'
    html += '                padding: 5px;\n'
    html += '            }\n'
    html += '            div.messageBox {\n'
    html += '                width: 400px;\n'
    html += '                border: 1px solid black;\n'
    html += '            }\n'
    html += '            \n'
    html += '            #message {\n'
    html += '                height: 24px;\n'
    html += '                width: 340px;\n'
    html += '            }\n'
    html += '            \n'
    html += '            #send {\n'
    html += '                float: right;\n'
    html += '                padding: 5px;\n'
    html += '            }\n'
    html += '            \n'
    html += '        </style>\n'
    html += '    </head>\n'
    html += '    <body>\n'
    html += '    <a style=\"text-decoration: none\" href=\"http://127.0.0.1:5000/Chat\"><h2>SchedLINE<span class=\"Searchy\"> Bot</span></h2></a>\n'
    html += '    <div class=\"chatscroll\">\n'
    html += '        <table class=\"chat\">\n'
    
    bar = None
    
    for line in chatLogs:
        type = line[0]
        date_time_obj = datetime.datetime.strptime(line[1:20], "%m/%d/%Y %H:%M:%S")
        if ((bar == None) or (date_time_obj.date() > bar.date())):
            bar = date_time_obj
            datestr = date_time_obj.strftime("%m/%d/%Y")
            now = datetime.datetime.now()
            sDiff = (now-bar).total_seconds()
            if sDiff < 60*60*24:
                if bar.day == now.day:
                    datestr = "Today"
                else:
                    datestr = "Yesterday"
            html += '            <tr><td><p class=\"datebubble\">'+datestr+'</p></td></tr>\n'
        message = line[20:-1]
        if type == "U":
            html += '            <tr><td><p class=\"userbubble\">'+message+'</p>'
            html += '<p class=\"usertime\">'+date_time_obj.time().isoformat(timespec='minutes')+'</p></td></tr>\n'
        elif type == "B":
            html += '            <tr><td><p class=\"botbubble\">'+message+'</p>'
            html += '<p class=\"bottime\">'+date_time_obj.time().isoformat(timespec='minutes')+'</p></td></tr>\n'
    
    html += '        </table>\n'
    html += '    </div>\n'
    html += '    <form action=\"http://127.0.0.1:5000/Chat\" method=POST>\n'
    html += '        <div class=\"messageBox\">\n'
    html += '            <input type=\"text\" name=\"messageInput\" id=\"message\" placeholder=\"Type your message...\" autocomplete="off">\n'
    html += '            <input type=\"submit\" id=\"send\" name=\"sendButton\" value=\"send\">\n'
    html += '        </div>\n'
    html += '        </form>\n'
    html += '    </body>\n'
    html += '</html>'
    with open("templates/chat.html", "w", encoding="utf8") as file:
        file.write(html)
    
    return html #render_template('chat.html')

if __name__ == '__main__':
    app.run()
