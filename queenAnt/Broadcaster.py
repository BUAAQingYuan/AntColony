__author__ = 'PC-LiNing'

from socket import *
import time
import multiprocessing

# signal
Start_Recovery = 'recovery start'
End_Recovery = 'recovery end'

# constant
Waiting_time_each_round = 5  # Waiting time for each round of voting , 30 seconds
Worken_port = 9000


class QueenServer():

    # udp client to send data to all nodes.
    # udp server to receive data from all nodes.this make it easy.
    def __init__(self,host=None,port=9000):
        # init udp client , udp server
        self._host = host
        self._port = port
        sock_server = socket(AF_INET,SOCK_DGRAM)
        address = (self._host,self._port)
        sock_server.bind(address)
        self._socketserver = sock_server

        sock_client = socket(AF_INET,SOCK_DGRAM)
        self._socketclient =  sock_client
        # block vote
        self._current_block_id = None
        self._current_vote_id = None
        # node public key
        self._nodes_keyring = []
        # node ip list
        self._address_list = ['10.2.1.35']
        # receive data
        self._receive_data = multiprocessing.Queue()

    def close_Server(self):
        self._socketserver.close()

    # send data to a group of address
    def send_to_nodes(self,data):
        address = ('10.2.1.35', 9000)
        self._socketclient.connect(address)
        self._socketclient.sendto(data.encode(),address)

    # receive process
    def receiver(self):
        print('receiver start .')
        while True:
            data,addr = self._socketserver.recvfrom(8192)
            print('%s: got %r' % (addr[0], data))
            current_time = time.time()
            self._receive_data.put((current_time,data,addr))

    # vote process
    def voter(self):
        print('voter start .')
        print('length: '+str(self._receive_data.qsize()))
        temp = self._receive_data.get()
        print('first data : '+str(temp[1]))

    # main process
    # one round : send request -- receiver response ---vote
    def start(self):
        # start recovery
        self.send_to_nodes(Start_Recovery)

        receiver = multiprocessing.Process(name='receiver',target=self.receiver)
        receiver.start()
        receiver.join(10)
        # kill
        if receiver.is_alive():
            print("receiver timeout.")
            receiver.terminate()
            receiver.join()

        voter = multiprocessing.Process(name='voter',target=self.voter)
        voter.start()
        voter.join()


if __name__ == '__main__':
    print('start Broadcaster on localhost:9000')
    QueenServer(host='10.2.1.57',port=9000).start()
