import socket

PORT_NUMBER = 5698
image_list_1 = ["peers", "peer to peer", "p2p", "peer", "peers to peers", "network_project_1/photos/p2p.jpg", "../../../network_project_1/photos/p2p.jpg"]
video_list_1 = ["peers", "peer to peer", "p2p", "peer", "peers to peers", "what is peer", "what is p2p", "what is peer to peer", "network_project_1/Videos/What_Is_p2p.mp4", "../../../network_project_1/Videos/What_Is_p2p.mp4"]
video_list_2 = ["how p2p work", "how p2p works", "how peer to peer work", "how peer to peer works", "network_project_1/Videos/How_peer_to_peer_works.mp4", "../../../network_project_1/Videos/How_peer_to_peer_works.mp4"]

def image_request(client_topic):

    img_url = image_list_1[-1]
    response_body = f"""
                <html>
                <head>
                    <title>Response</title>
                </head>
                <body>
                    <h1>Topic: {client_topic.replace("+", " ")} Type:  Image</h1>
                    <img width="640" height="360" class="photos" src="{img_url}" alt="P2P" class="P2P" target="_blank"> />
                </body>
                </html>
                """

    return response_body

def video_request(client_topic):
    if client_topic.lower().replace("+", " ") in video_list_1:
        video_url = video_list_1[-1]
    elif client_topic.lower().replace("+", " ") in video_list_2:
        video_url = video_list_2[-1]
    response_body = f"""
                <html>
                <head>
                    <title>Response</title>
                </head>
                <body>
                    <h1>Topic: {client_topic.replace("+", " ")} Type:  Image</h1>
                     <video width="640" height="360" controls>
                        <source src="{video_url}">
                    </video>
                </body>
                </html>
                """

    return response_body

def handle_client(client_socket):
    request = client_socket.recv(1024 * 2).decode()

    request_line = request.splitlines()[0]
    requested_path = request_line.split()[1]
    print("Requested Path: ", requested_path)

    if requested_path.endswith(".css"):  # Handle CSS files
        try:
            with open("../../../network_project_1/supporting_material_en.css", "r") as css_file:
                css_data = css_file.read()

            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: text/css\r\n"
            response += f"Content-Length: {len(css_data)}\r\n"
            response += "\r\n"
            response += css_data

            client_socket.sendall(response.encode())

        except FileNotFoundError:
            response = "HTTP/1.1 404 Not Found\r\n\r\nCSS file not found."
            client_socket.sendall(response.encode())

    if requested_path.strip() == "/" + image_list_1[-2]:
        try:
            with open(image_list_1[-1], "rb") as image_file:
                image_data = image_file.read()

            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: image/jpg\r\n"
            response += f"Content-Length: {len(image_data)}\r\n"
            response += "\r\n"
            response = response.encode() + image_data

            client_socket.sendall(response)

        except FileNotFoundError:
            response = "HTTP/1.1 404 Not Found\r\n\r\nImage not found."
            client_socket.sendall(response.encode())

    elif requested_path.strip() == "/" + video_list_1[-2] or requested_path.strip() == "/" + video_list_2[-2]:
        try:
            if requested_path.strip() == "/" + video_list_1[-2]:
                with open(video_list_1[-1], "rb") as video_file:
                    video_data = video_file.read()

            elif requested_path.strip() == "/" + video_list_2[-2]:
                with open(video_list_2[-1], "rb") as video_file:
                    video_data = video_file.read()

            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: video/mp4\r\n"
            response += f"Content-Length: {len(video_data)}\r\n"
            response += "\r\n"
            response = response.encode() + video_data

            client_socket.sendall(response)

        except FileNotFoundError:
            response = "HTTP/1.1 404 Not Found\n\nVideo not found."
            client_socket.sendall(response.encode())

    else:
        try:
            with open("../../../network_project_1/supporting_material_en.html", "r") as file:
                response_body = file.read()

        except FileNotFoundError:
            response_body = "<html><body><h1>404 Not Found</h1><p>The requested file could not be found.</p></body></html>"

        if "POST" in request:

            # print("Got request from client: \n Request Body: \n" + request)

            print("Received POST request")

            client_request = request.strip().split("\n")[-1].split("=")
            client_topic = "".join(client_request[1].strip().split("&")[0])
            client_type = "".join(client_request[2].strip())

            if client_type == "Image":
                if client_topic.lower() in image_list_1:
                    response_body = image_request(client_topic)
                else:
                    redirect_url = "/alternative_page"
                    response = f"HTTP/1.1 307 Temporary Redirect\r\n"
                    response += f"Location: {redirect_url}\r\n"
                    response += f"Content-Length: 0\r\n"
                    response += f"\r\n"
                    return None

            elif client_type == "Video":
                response_body = video_request(client_topic)

        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html\r\n"
        response += f"Content-Length: {len(response_body)}\r\n"
        response += "\r\n"
        response += response_body

        client_socket.sendall(response.encode())

    client_socket.close()

def protocol_listener():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', PORT_NUMBER))
    server_socket.listen(10)

    print("Server running on port 5698...")

    while True:
        client_socket, addr = server_socket.accept()
        print("Got connection from", addr)
        handle_client(client_socket)

if __name__ == "__main__":
    protocol_listener()
