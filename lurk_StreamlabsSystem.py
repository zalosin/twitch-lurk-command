# ---------------------
# Import libraries
# ---------------------
import datetime
import sys
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

# ---------------------
# [Required] Script info
# ---------------------
ScriptName = "Lurk"
Website = "http://www.twitch.tv/zalosin"
Description = "Shows if a user is lurking or has stopped lurking by using !lurk"
Creator = "Zalosin"
Version = "1.2"

# ----------------------
# CHANGELOG
#
# v1.2 - added file clear
# v1.1 - added time lurked
#
# ----------------------

# ----------------------
# Set Variables
# ----------------------
m_Response = "Command initialized"
m_Command = "!lurk"
m_CooldownSeconds = 0
m_CommandPermission = "Everyone"
m_CommandInfo = ""

# --------------------
# EDIT THIS FOR YOUR SAVE LOCATION
# --------------------
saveLocation = "\Streamlabs Chatbot\Services\Scripts\Lurk\users.txt"

# ----------------------
# [Required] Intialize Data (only called on load)
# ----------------------


def Init():
    open(saveLocation, 'w').close()
    return

# ----------------------
# [Required] Execute Data / Process Messages
# ----------------------


def pretty_time_delta(seconds):
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%dd %dh %dm %ds' % (days, hours, minutes, seconds)
    elif hours > 0:
        return '%dh %dm %ds' % (hours, minutes, seconds)
    elif minutes > 0:
        return '%dm %ds' % (minutes, seconds)
    else:
        return '%ds' % (seconds,)


def Execute(data):
    if data.Message.lower() == m_Command:
        f = open(saveLocation, 'r')
        text = f.read()
        lines = text.split("\n")
        f.close()
        for line in lines:
            username = ""
            value = ""
            date = ""
            time = ""
            if line != "":
                username, value, date, time = line.split(" ")
            old_value = value
            old_date = date
            old_time = time
            if data.User == username:
                if value == "0":
                    new_time = datetime.datetime.now()
                    time_text = old_date + " " + old_time
                    old_composed = datetime.datetime.strptime(
                        time_text, '%Y-%m-%d %H:%M:%S')
                    delta = new_time - old_composed
                    global m_Response
                    m_Response = username + " has stopped lurking. You lurked for " + \
                        pretty_time_delta(
                            delta.total_seconds()) + ". Welcome back!"
                    value = "1"
                else:
                    global m_Response
                    m_Response = username + " has started lurking. See you soon!"
                    value = "0"
                    new_time = datetime.datetime.now()
                out = open(saveLocation, "w")
                for row in lines:
                    if row != lines[len(lines)-1]:
                        if username+" "+old_value+" "+old_date+" "+old_time == row:
                            out.write(username+" "+value+" " +
                                      new_time.strftime("%Y-%m-%d %H:%M:%S")+"\n")
                        else:
                            out.write(row+"\n")
                    elif username+" "+old_value+" "+old_date+" "+old_time == row:
                        out.write(username+" "+value+" " +
                                  new_time.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        out.write(row)
                out.close()
                Parent.SendTwitchMessage(m_Response)
                return
        out = open(saveLocation, "a")
        global m_Response
        m_Response = data.User + " has started lurking. See you soon!"
        value = "0"
        new_time = datetime.datetime.now()
        out.write("\n"+data.User + " "+value+" " +
                  new_time.strftime("%Y-%m-%d %H:%M:%S"))
        out.close()
        Parent.SendTwitchMessage(m_Response)
    else:
        f = open(saveLocation, 'r')
        text = f.read()
        lines = text.split("\n")
        f.close()
        for line in lines:
            username = ""
            value = ""
            date = ""
            time = ""
            if line != "":
                username, value, date, time = line.split(" ")
            old_value = value
            old_date = date
            old_time = time
            if data.User == username:
                if value == "0":
                    new_time = datetime.datetime.now()
                    time_text = old_date + " " + old_time
                    old_composed = datetime.datetime.strptime(
                        time_text, '%Y-%m-%d %H:%M:%S')
                    delta = new_time - old_composed
                    global m_Response
                    m_Response = username + " has stopped lurking. You lurked for " + \
                        pretty_time_delta(
                            delta.total_seconds()) + ". Welcome back!"
                    value = "1"
                    Parent.SendTwitchMessage(m_Response)
                else:
                    return
                out = open(saveLocation, "w")
                for row in lines:
                    if row != lines[len(lines)-1]:
                        if username+" "+old_value+" "+old_date+" "+old_time == row:
                            out.write(username+" "+value+" " +
                                      new_time.strftime("%Y-%m-%d %H:%M:%S")+"\n")
                        else:
                            out.write(row+"\n")
                    elif username+" "+old_value+" "+old_date+" "+old_time == row:
                        out.write(username+" "+value+" " +
                                  new_time.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        out.write(row)
                out.close()
                return
        return
    return

# ----------------------
# [Required] Tick Function
# ----------------------


def Tick():
    return
