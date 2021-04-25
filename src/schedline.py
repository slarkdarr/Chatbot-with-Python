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
    o = p.objek(text)
    m = p.matkul(o)
    t = p.topik(o)
    j = p.jenis(text)
    if (p.pertanyaan(text)):
        print("pertanyaan")
    else:
        tp = p.tanggalPada(text)
        response = "[TASK BERHASIL DICATAT]<br>"
        
        datetype = p.tanggalTipe(tp)
        tp = p.translateTanggal(tp)
        if (datetype == 1):
            date = datetime.datetime.strptime(tp, "%d %B %Y")
        elif (datetype == 2):
            date = datetime.datetime.strptime(tp, "%B %d %Y")
        else:
            date = datetime.datetime.strptime(tp, "%d/%m/%Y")
        task = j.capitalize()+"---"+date.strftime("%m/%d/%Y")+"---"+m+"---"
        if (t != None):
            task += t.capitalize()+"\n"
        else:
            task += " \n"
        
        f = open("../data/tasks.txt", "a+")
        f.write(task)
        f.close()
        
        f = open("../data/tasks.txt", "r")
        lines = f.readlines()
        f.close()
        
        now = datetime.datetime.now()
        f = open("../data/logs.txt", "a+")
        response += responseBody(lines)
        log = "B"+now.strftime("%m/%d/%Y %H:%M:%S")+response+"\n"
        f.write(log)
        f.close()
        
def responseBody(lines):
    tasks = {}
    body = ""
    for line in lines:
        line = line.replace("\n", "")
        info = line.split("---")
        if (info[1] in tasks.keys()):
            tasks[info[1]].append([info[0], info[2], info[3]])
        else:
            tasks[info[1]] = [[info[0], info[2], info[3]]]
        
    times = sorted(list(tasks.keys()))
    i = 1
    for time in times:
        for task in tasks[time]:
            print(task)
            body += "(ID: "+str(i)+") "+time+" - "+task[1]+" - "+task[0]+" - "+task[2]+"<br>"
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
