import socket
import sys
import datetime
import time

server = "irc.twitch.tv"
channel = "#wetish"

count = 0
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connected = False
def connect():
    while connected is False:
        try:
            print "connecting to:"+server
            global irc
            irc.connect((server, 443))
            #guest details filled in. unable to send messages.
            irc.send('PASS blah\r\n')
            irc.send('NICK justinfan23423\r\n')
            irc.send('USER justinfan23423 0 * :justinfan23423\r\n')
            irc.send('JOIN ' + channel + '\r\n')
            irc.send("TWITCHCLIENT 3\r\n")
            global connected
            connected = True
        except socket.error:
            print "Attempting to connect..."
            time.sleep(5)
            continue

connect()

#:twitchnotify!twitchnotify@twitchnotify.tmi.twitch.tv PRIVMSG #sodapoppin :Popin_fresh just subscribed!
last_ping = time.time()
threshold = 5 * 60 # five minutes
while 1:
    connect()
    while connected:
        try:
            data = irc.recv (2040)
            print data

            if data.startswith(':twitchnotify') and data.find('just subscribed') != -1:
                d = data[data.index(' :') + 2:data.index(' just subscribed')]
                print d
                irc.send("PRIVMSG "+channel+" :PogChamp Drop the fucking LoKor PogChamp\r\n")

            if data.startswith ( 'PING' ) != -1:
                irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
                last_ping = time.time()

            if (time.time() - last_ping) > threshold:
                global connected
                connected = False
                break

        except socket.error:
            print "Attempting to connect..."
            time.sleep(5)
            continue
