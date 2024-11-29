import socket
import threading
import time

SERVER = "192.168.56.1"
PORT = 5689
ANSWER_TIME_OUT = 90

flag = False

def get_user_input(input_list):
    try:
        input_list.append(input("Enter an Answer:  "))
    except Exception:
        pass

def send_request():
    global flag
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto("start".encode(), (SERVER, PORT))
    print(f"Entered the server with IP {(SERVER, PORT)}")
    response, server_address = client_socket.recvfrom(1024)
    print(response.decode())
    
    while True:

        if flag:
            time.sleep(8)
            print("\nTime out happened !, Are you with us ?? \n Press any key to continue:  ", end='')
            flag = False

        if response[0] != "0" and response[0] != "1":
            flag = False
            message = input("Enter a response: ")
            client_socket.sendto(message.encode(), (SERVER, PORT))
            print(f"{message} sent to {SERVER}:{PORT}\n")

        elif response[0] == "1":
            input_result = []
            input_thread = threading.Thread(target=get_user_input, args=(input_result,))
            input_thread.start()
            input_thread.join(timeout=ANSWER_TIME_OUT)

            if input_result:
                flag = False
                message = input_result[0]
            else:
                flag = True
                message = "NULL"

            client_socket.sendto(message.encode(), (SERVER, PORT))
            print(f"{message} sent to {SERVER}:{PORT}\n\n")

        response, server_address = client_socket.recvfrom(1024)
        response = response.decode()

        if response == "quit":
            client_socket.close()
            break

        if response[0] == "0" or response[0] == "1":
            print(f"{response[1:]}")
        else:
            print(f"Response from Serve: {response}")

    print("End of Process")

if __name__ == "__main__":
    send_request()
