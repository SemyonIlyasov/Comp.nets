import socket
import pages

urls_list = ['/hobby_home', '/tst']
prod_table = []

def make_resp(req):
    method = req.split(" ")[0]

    if (method != 'GET' and method != "POST"):
        return('HTTP/1.1 405 Method not allowed\n\n', 405)

    if(method == 'GET' or method == "POST"):
        return ('HTTP/1.0 200 OK\n' + 'Content-Type: text/html\n\n' + pages.get_page(req, method), 200)

    return ('HTTP/1.1 404 Page not found\n\n', 404)



def sniffing():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOSTNAME = socket.gethostbyname(socket.gethostname())
    print(HOSTNAME)
    server_socket.bind((HOSTNAME, pages.local_port))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # чтобы убрать задержку закрытия соединения на порте после выключения сервера
    server_socket.listen(1)

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        print(request)
        print()
        print(addr)
        response = make_resp(request.decode())
        client_socket.send(response[0].encode())

        client_socket.close()


if __name__ == "__main__":
    sniffing()