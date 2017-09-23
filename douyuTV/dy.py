
import multiprocessing
import socket
import time
import re
import signal

client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host=socket.gethostbyname("openbarrage.douyutv.com")
port=8601
client.connect((host,port))
danmu_re=re.compile(b'txt@=(.+?)/cid@')
username_re = re.compile(b'nn@=(.+?)/txt@')
def send_req_msg(msgstr):
	msg=msgstr.encode('utf-8')
	data_length=len(msg)+8
	code=689
	msgHead=int.to_bytes(data_length,4,'little')\
			+int.to_bytes(data_length,4,'little')+\
			int.to_bytes(code,4,'little')

	client.send(msgHead)
	sent=0
	while  sent<len(msg):
		tn =client.send(msg[sent:])
		sent=sent+tn

def DM_start(roomid):
		msg='type@=loginreq/roomid@={}/\0'.format(roomid)
		send_req_msg(msg)
		msg_more = 'type@=joingroup/rid@={}/gid@=-9999/\0'.format(roomid)
		send_req_msg(msg_more)
		while  True:
			data=client.recv(1024)
			danmu_username=username_re.findall(data)
			danmu_content=danmu_re.findall(data)
			if not data:
				break
			else:
				for i in range(0,len(danmu_content)):
					try:
						print('[{}]:{}'.format(danmu_username[0].decode('utf8'), danmu_content[0].decode(encoding='utf8')))
					except:
						continue

					with open('zhuaqudanmu.txt','a+',encoding='utf-8') as f:
						f.write('[{}]:{}\n'.format(danmu_username[0].decode('utf8'), danmu_content[0].decode(encoding='utf8')))
def keeplive():
	while  True:
		msg= 'type@=keeplive/tick@=' + str(int(time.time())) + '/\0'
		send_req_msg(msg)
		print('发送心跳包')
		time.sleep(15)

def logout():
	msg='type@=logout/'
	send_req_msg(msg)
	print('已经退出服务器')
def signal_handler(signal,fram):
	p1.terminate()
	p2.terminate()
	logout()
	print('拜拜')
if __name__ == '__main__':
	room_id=input('请输入斗鱼房间号：')
	signal.signal(signal.SIGINT, signal_handler)
	p1 = multiprocessing.Process(target=DM_start, args=(room_id,))
	p2 = multiprocessing.Process(target=keeplive)
	p1.start()
	p2.start()