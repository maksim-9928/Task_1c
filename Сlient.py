import socket
import argparse
from threading import Thread
import os.path
import math


#Отправляем часть файла. В каждом потоке создаём соединение с сервером
def send_part_of_file(file_name, current_th_ind, size_part, position):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as csFT_thread:
        csFT_thread.connect((socket.gethostname(), 10001))

        
        with open(file_name, 'rb') as fs:
        
            fs.seek(position) #куда ставим указатель для файла
            data = fs.read(size_part)
            data_with_seppar = str(current_th_ind).encode() + b"$" + data
            csFT_thread.send(data_with_seppar)
        
        
        

def define_pos(filename, size_part, num_threads):

    positions_for_threads = {}
    positions_for_threads[0] = 0
    with open(filename, "rb") as f:
        for i in range(1,num_threads):
            tmp_data = f.read(size_part)
            positions_for_threads[i] = f.tell()
        return positions_for_threads

#работаем с командной строкой
parser = argparse.ArgumentParser()
parser.add_argument('-file','--file', type = str)
parser.add_argument('-threads','--threads', type = int)
parser.add_argument('-ip','--ip', type = str)
parser.add_argument('-send','--send', action = 'store_true')
args = parser.parse_args()



if __name__ == '__main__':
    if (args.send):
        
        file_name = args.file
        size_file = os.path.getsize(file_name)
        num_threads = args.threads
        size_part = math.ceil(size_file/num_threads)
        host = args.ip


        positions_for_threads = define_pos(file_name, size_part, num_threads)

        #Отпраляем отдельно имя файла и размер части
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as csFT:
            csFT.connect((socket.gethostname(), 10001))

            str_to_send = file_name + "$" + str(size_part) + "$" + str(num_threads) + "$"
            csFT.send(str_to_send.encode())


        threads = []
        for i in range(num_threads):
    
            my_thread = Thread(target = send_part_of_file, args = (file_name, i, size_part, positions_for_threads[i]))
            threads.append(my_thread)
            my_thread.start()


        for thread in threads:
            thread.join()

        print ("Sent")
        
        



