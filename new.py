import socket, time
from datetime import datetime
from functools import reduce

def ConstructHeader(msg_type, SenderCompID, TargetCompID, SenderSubID, TargetSubID, messageSequenceNumber):
    header = ''

    # Version of FIX
    header += "8=FIX.4.4|"

    message = ''

    # Type of message, A = String
    message += "35=" + msg_type + "|"

    message += "49="  + SenderCompID +  "|"
    message += "56="  + TargetCompID +  "|"

    message += "50="  + SenderSubID +  "|"
    message += "57="  + TargetSubID +  "|"

    message += "34="  + messageSequenceNumber +  "|"

    utctimenow_year = str(datetime.utcnow().year)
    utctimenow_month = str(datetime.utcnow().month)
    utctimenow_date = str(datetime.utcnow().day)
    utctimenow_date = utctimenow_date.zfill(2)

    utctimenow_hour = str(datetime.utcnow().hour)
    utctimenow_hour = utctimenow_hour.zfill(2)

    utctimenow_min = str(datetime.utcnow().minute)
    utctimenow_min = utctimenow_min.zfill(2)

    utctime = utctimenow_year+utctimenow_month+utctimenow_date+'-'+utctimenow_hour+':'+utctimenow_min+':00'

    message += "52="  + utctime +  "|"

    #message += "52=20171204-16:20:00|"

    return header, message

def ConstructTrailer(headerAndBody):
    headerAndBody = str(headerAndBody.replace('|', chr(0x01)))
    chksum = str(reduce(lambda x,y:x+y, map(ord, headerAndBody)) % 256)
    chksum = chksum.zfill(3)

    return chksum
    # expected 131

def LogonMessage(heartBeatSeconds, username, password, resetSeqNum):
    body = ''

    # Encryption
    body += "98=0|"

    body += "108="  + heartBeatSeconds +  "|"

    if resetSeqNum:
        body += "141=Y|"


    body += "553=" + username + "|"
    body += "554=" + password + "|"

    return body

def LogonPacket():

    # Header
    msg_type = 'A'

    SenderCompID = 'demo.icmarkets.8236701'
    TargetCompID = 'cServer'

    #SenderSubID = 'QUOTE'
    SenderSubID = 'TRADE'
    TargetSubID = 'TRADE'
    messageSequenceNumber = '1'

    header, message = ConstructHeader(msg_type, SenderCompID, TargetCompID, SenderSubID, TargetSubID, messageSequenceNumber)

    # Body
    heartBeatSeconds = '30'
    username = '8236701'
    password = 'provone'
    resetSeqNum = 1

    body = LogonMessage(heartBeatSeconds, username, password, resetSeqNum)

    length = len(message) + len(body)
    # FIX version + len of msg
    header += "9=" + str(length) + "|"

    # FIX version + len of msg + rest of the header
    header = header + message

    print('Header construction completed')
    print('Header is: ', header, '\n')

    # FIX version + len of msg + rest of the header + body (login)
    headerAndBody = header + body

    #headerAndBody = '8=FIX.4.4|9=126|35=A|49=theBroker.12345|56=CSERVER|34=1|52=20170117-08:03:04|57=TRADE|50=any_string|98=0|108=30|141=Y|553=12345|554=passw0rd!|'

    # Trailer
    chksum = ConstructTrailer(headerAndBody)
    trailer = "10="+str(chksum)+"|"
    #trailer = "10=254|"
    # 254 QUOTE, 224 TRADE

    #print('Trailer construction completed')
    #print('Trailer is: ', trailer, '\n')

    headerAndBodyAndTrailer = headerAndBody + trailer
    #print('ctrader packet is: ', headerAndBodyAndTrailer, '\n')

    headerAndBodyAndTrailer = headerAndBodyAndTrailer.replace("|", chr(0x01))

    # ctrader packet constructor finished

    return headerAndBodyAndTrailer

def buy():

    utctimenow_year = str(datetime.utcnow().year)
    utctimenow_month = str(datetime.utcnow().month)
    utctimenow_date = str(datetime.utcnow().day)
    utctimenow_date = utctimenow_date.zfill(2)

    utctimenow_hour = str(datetime.utcnow().hour)
    utctimenow_hour = utctimenow_hour.zfill(2)

    utctimenow_min = str(datetime.utcnow().minute)
    utctimenow_min = utctimenow_min.zfill(2)

    utctime = utctimenow_year+utctimenow_month+utctimenow_date+'-'+utctimenow_hour+':'+utctimenow_min+':00'

    msg_type = 'D'

    SenderCompID = 'demo.icmarkets.8236701'
    TargetCompID = 'cServer'

    #SenderSubID = 'QUOTE'
    SenderSubID = 'TRADE'
    TargetSubID = 'TRADE'
    messageSequenceNumber = '2'

    header, message = ConstructHeader(msg_type, SenderCompID, TargetCompID, SenderSubID, TargetSubID, messageSequenceNumber)

    body = ""

    body += "11="  + "1111" +  "|"

    body += "55="  + "1" +  "|"

    body += "54="  + "1" +  "|"

    body += "60="  + utctime +  "|"

    body += "38="  + "10000" +  "|"

    body += "40="  + "1" +  "|"

    length = len(message) + len(body)
    # FIX version + len of msg
    header += "9=" + str(length) + "|"

    # FIX version + len of msg + rest of the header
    header = header + message

    print('Header construction completed')
    print('Header is: ', header, '\n')

    # FIX version + len of msg + rest of the header + body (login)
    headerAndBody = header + body

    #headerAndBody = '8=FIX.4.4|9=126|35=A|49=theBroker.12345|56=CSERVER|34=1|52=20170117-08:03:04|57=TRADE|50=any_string|98=0|108=30|141=Y|553=12345|554=passw0rd!|'

    # Trailer
    chksum = ConstructTrailer(headerAndBody)
    trailer = "10="+str(chksum)+"|"
    #trailer = "10=254|"
    # 254 QUOTE, 224 TRADE

    #print('Trailer construction completed')
    #print('Trailer is: ', trailer, '\n')

    headerAndBodyAndTrailer = headerAndBody + trailer
    #print('ctrader packet is: ', headerAndBodyAndTrailer, '\n')

    headerAndBodyAndTrailer = headerAndBodyAndTrailer.replace("|", chr(0x01))

    # ctrader packet constructor finished

    return headerAndBodyAndTrailer


def Main():
    host = 'h51.p.ctrader.com'
    port = 5202

    s = socket.socket()
    s.connect((host, port))

    # Logon
    seq_num = 1
    headerAndBodyAndTrailer = LogonPacket()
    #print(headerAndBodyAndTrailer)
    #print('LOGON packet sent to ctrader!!!')

    s.send(str.encode(headerAndBodyAndTrailer))
    
    data = s.recv(1024)
    data = str(data)
    a = data[9]
    data = data.replace(a, '|')
    #print('\n\nLOGON RESP :  ', data)

    seq_num = 2
    headerAndBodyAndTrailer = buy()
    print(headerAndBodyAndTrailer)
    print('BUY packet sent to ctrader!!!')

    s.send(str.encode(headerAndBodyAndTrailer))
    
    data = s.recv(1024)
    data = str(data)
    a = data[9]
    data = data.replace(a, '|')
    print('\n\nBUY RESP :  ', data)



if __name__ == '__main__':
    Main()











