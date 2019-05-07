import argparse
import socket
import threading


def process_request(conn, addr):
    all_data = b''
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            all_data += data
                
    for i in range(4):
        if (all_data[i:i+1].decode() == "$"):
             
            data = all_data[i+1:]
            client_thread_ind = int(all_data[:i].decode())
            d[client_thread_ind] = data

            break


parser = argparse.ArgumentParser()
parser.add_argument('-recieve','--recieve', action = 'store_true')
args = parser.parse_args()



if __name__ == '__main__':
    if (args.recieve):
        print ("Server is ready to accept data")
        
        #принимаем имя файла и количесто потоков
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ssFT:
            host = socket.gethostbyname(socket.gethostname())
            print ("Server_host: ", host)
            ssFT.bind((host, 10001))
            ssFT.listen(1)

            (conn, address) = ssFT.accept()

            fn_and_sp = conn.recv(1024).decode()    
            file_name = fn_and_sp.split("$")[0]
            part_size = int(fn_and_sp.split("$")[1])
            num_threads = int (fn_and_sp.split("$")[2])


        # тут многопоточно принимаем данные файла. Сначала создаём сокет,
        # а зетем в цикле принимаем входящие соединения от клиента. Как только приняли соединение,
        # создаём поток и продлжаем ацептить ноые соединения.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ssFT_thread:
            ssFT_thread.bind((host, 10001))
            ssFT_thread.listen(num_threads)

            threads = []
            d = {}
            for i in range(num_threads):
                conn, address = ssFT_thread.accept()
        
                th = threading.Thread(target = process_request, args = (conn, address))
                threads.append(th)
                th.start()

            for thread in threads:
                thread.join()
        


        #записыаем данные в файл
        with open(file_name, "wb") as f:
            for key in range (len(d)):
                clear_byte_data = d[key]
                f.write(clear_byte_data)

        print ("Check your directory")
