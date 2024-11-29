import socket # Basic Socket library
import random # Random generator to generate random numbers
import pandas as pd # 2D array library to deal with CSV data's
import time # time function

SERVER = "192.168.56.1" # Local Host
PORT = 5689 # Port the server running on

# if the file doesn't exist save them in data frame which will transfer the data to file names user.csv later
try:
    users = pd.read_csv("users.csv")
except FileNotFoundError:
    users = pd.DataFrame(columns=["ID", "PASSWORD", "ALL_TIME_POINTS", "ALL_TIME_ROUNDS", "ALL_TIME_WINS"])

# Dict which saves the current location of the client to allow the client to return to their location when send data again
client_states = {}

# general Vars
question, answer, number_of_answers, players_count, number_of_questions, number_of_correct_answers = None, None, 0, 0, 0, 0

# Set of questions to try
def questions_set_all(number):
    if number == 1:
        return "1Who was the first president of the United States?", ("george washington", "washington", "george washington", "washington dc")
    elif number == 2:
        return "1In what year did World War II end?", ("1945", "nineteen forty five", "nineteen 45")
    elif number == 3:
        return "1Who was the queen of ancient Egypt?", ("cleopatra", "cleopatra", "cleo patra")
    elif number == 4:
        return "1What is the name of the ship that brought the Pilgrims to America?", ("mayflower", "may flower")
    elif number == 5:
        return "1Who is credited with discovering America?", ("christopher columbus", "columbus", "christopher columbus")
    elif number == 6:
        return "1What empire did Genghis Khan rule?", ("mongol empire", "mongol", "mongol empire", "genghis khan empire")
    elif number == 7:
        return "1In what year did the Berlin Wall fall?", ("1989", "nineteen eighty nine")
    elif number == 8:
        return "1Who was the British leader during World War II?", ("winston churchill", "churchill")
    elif number == 9:
        return "1What treaty ended World War I?", ("treaty of versailles", "versailles treaty", "versailles", "versai")
    elif number == 10:
        return "1Who was the first emperor of Rome?", ("augustus", "octavian")
    elif number == 11:
        return "1What is the name of the anime character with yellow hair?", ("naruto", "naruto uzumaki")
    elif number == 12:
        return "1In 'Dragon Ball', what is the name of Goku's transformation with golden hair?", ("super saiyan",)
    elif number == 13:
        return "1In 'One Piece', who is the captain of the Straw Hat Pirates?", ("luffy", "monkey d. luffy")
    elif number == 14:
        return "1In 'Attack on Titan', what do the characters use to fight Titans?", ("gear",)
    elif number == 15:
        return "1What is the name of the anime with a notebook that kills people?", ("death note",)
    elif number == 16:
        return "1What is the name of the anime where a girl works at a bathhouse?", ("spirited away",)
    elif number == 17:
        return "1In 'My Hero Academia', who inherits All Might's power?", ("deku", "izuku midoriya")
    elif number == 18:
        return "1In 'Pokemon', who is Pikachu's trainer?", ("ash", "ash ketchum")
    elif number == 19:
        return "1In 'Sailor Moon', what is Sailor Moon's real name?", ("usagi", "usagi tsukino")
    elif number == 20:
        return "1In 'Demon Slayer', what is the name of the main character?", ("tanjiro", "tanjiro kamado")
    elif number == 21:
        return "1What is the value of 7 × 8 - 5?", ("51",)
    elif number == 22:
        return "1What is 2 raised to the power of 5?", ("32",)
    elif number == 23:
        return "1Solve for x: 3x + 5 = 20", ("5",)
    elif number == 24:
        return "1What is the derivative of x^2 with respect to x?", ("2x",)
    elif number == 25:
        return "1What is the value of π (pi) rounded to 3 decimal places?", ("3.142",)
    elif number == 26:
        return "1What is the factorial of 5?", ("120",)
    elif number == 27:
        return "1What is the area of a circle with a radius of 7? (Use π = 3.14)", ("153.86",)
    elif number == 28:
        return "1What is the solution to the equation: 2x^2 - 8 = 0?", ("2", "-2")
    elif number == 29:
        return "1What is the value of the sine of 30 degrees?", ("0.5",)
    elif number == 30:
        return "1What is the greatest common divisor (GCD) of 48 and 18?", ("6",)
    elif number == 31:
        return "1What is the longest river in the world?", ("nile", "amazon")
    elif number == 32:
        return "1What is the highest mountain on Earth?", ("mount everest", "everest")
    elif number == 33:
        return "1Which country has the largest population?", ("china",)
    elif number == 34:
        return "1What is the smallest country in the world?", ("vatican city", "vatican")
    elif number == 35:
        return "1Which desert is the largest?", ("sahara",)
    elif number == 36:
        return "1What is the capital city of Australia?", ("canberra",)
    elif number == 37:
        return "1What is the imaginary line that divides the Earth?", ("equator",)
    elif number == 38:
        return "1Which ocean is the largest?", ("pacific ocean", "pacific")
    elif number == 39:
        return "1What is the sea bordered by Europe, Asia, and Africa?", ("mediterranean sea", "mediterranean")
    elif number == 40:
        return "1Which U.S. state is the largest by area?", ("alaska",)
    else:
        return "Invalid question number", ("n/a",)

# make new client and save it in the general pandas
def create_client_data_frame(user_id, user_pass):

    global users
    if user_id in users["ID"].values: # if the user already in don't make new user ( handled late but why not )
        return None
    new_data = pd.DataFrame({
        "ID": [str(user_id)],
        "PASSWORD": [user_pass],
        "ALL_TIME_POINTS": [0],
        "ALL_TIME_ROUNDS": [0],
        "ALL_TIME_WINS": [0]
    })
    users = pd.concat([users, new_data], ignore_index=True)

# make new user account ( saved details in user.csv )
def sign_up(server_socket, client_address, data):
    user_id, user_pass = None, None
    client = client_states[client_address]

    # if the user entered back, return to the menu and make the step "option"
    if data == "back":
        client["step"] = "option"
        menu(server_socket, client_address, 0) # 0 option to not add a header
        return None

    if client["step"] == "option":
        response = "Please Enter your ID, Write back to return to main menu"
        client["step"] = "add_id"
        server_socket.sendto(response.encode(), client_address)
        return None

    if client["step"] == "add_id":
        while True:
            user_id = data
            if user_id in users["ID"].values:  # if the user is duplicated
                server_socket.sendto("This ID already exist, enter another ID".encode(), client_address)
                return None
            else:
                client["id"] = data
                break

    if client["step"] == "add_id":
        client["step"] = "add_password"
        server_socket.sendto("Enter Your Password, not less than 4 chars please".encode(), client_address)
        return None

    if client["step"] == "add_password":
        while True:
            user_pass = data
            if len(user_pass) < 4: # if the password is less than 4 chars
                server_socket.sendto("invalid Password, not less than 4 chars please".encode(), client_address)
                return None
            else:
                client["pass"] = user_pass
                break

    if client["step"] == "add_password":
        client["step"] = "done"

    if client["step"] == "done":
        create_client_data_frame(client["id"], client["pass"]) # if every thing is ok then create a client
        client["step"] = "option"
        menu(server_socket, client_address, 2)
        return None

# log ion to currently exist account
def log_in(server_socket, client_address, data):
    user_id, user_pass = None, None

    client = client_states[client_address]

    # if the user entered back, return to the menu and make the step "option"
    if data == "back":
        client["step"] = "option"
        menu(server_socket, client_address, 0) # 0 option to not add a header
        return None

    if client["step"] == "option":
        response = "Please Enter your ID, Write back to return to main menu"
        client["step"] = "id"
        server_socket.sendto(response.encode(), client_address)
        return None

    if client["step"] == "id":
        while True:
            user_id = data
            if user_id not in users["ID"].values:
                server_socket.sendto(f"ID {user_id} Does not Exist, please Try again, Write back to return to main menu".encode(), client_address)
                return None
            else:
                client["id"] = data
                break

    if client["step"] == "id":
        client["step"] = "pass"
        server_socket.sendto("Enter Your Password, Write back to return to main menu".encode(), client_address)
        return None

    if client["step"] == "pass":
        while True:
            user_pass = data
            if str((users.loc[users["ID"] == client["id"], "PASSWORD"].iloc[0])) != str(user_pass):
                server_socket.sendto("invalid Password!, please try again, Write back to return to main menu".encode(), client_address)
                return None
            else:
                client["pass"] = data
                break

    print(f"User with ID:  {client["id"]}, and PASSWORD:  {client['pass']} joined successfully")
    client["step"] = "option"
    menu(server_socket, client_address, 1)
    return None

# Function to count number of players currently in game
def in_game_players_count():
    return sum(1 for addresses in client_states.keys() if client_states[addresses]["step"] == "game_waiting" or client_states[addresses]["step"] == "in_game")

# option 3: join a game
# This function will handle all the game stuff from now tell the round ends
def join_a_game(server_socket, client_address, data):

    client = client_states[client_address]
    global question, answer, number_of_answers, players_count, number_of_questions, number_of_correct_answers
    if data == "back":
        client["step"] = "option"
        menu(server_socket, client_address, 0)
        return None

    if client["step"] == "option":
        client["step"] = "game_waiting"
        for clients_addresses in client_states.keys():
            if client_states[clients_addresses]["step"] == "game_waiting" or client_states[clients_addresses]["step"] == "in_game":
                server_socket.sendto(f"0{client["id"]} has joined the game, current player {players_count + 1}".encode(), clients_addresses)

    if players_count < 2:
        if client["step"] == "game_waiting":
            players_count += 1
            if players_count < 2:
                response = "0Waiting For players, Minimum of 2"
                server_socket.sendto(response.encode(), client_address)
                return None

            number = random.randint(1, 40)
            question, answer = questions_set_all(number)
            print("New round will begin now")
            print(f"question: {question}  Answer: {answer}  number: {number}")
            for clients_addresses in client_states.keys():
                if client_states[clients_addresses]["step"] == "game_waiting" or client_states[clients_addresses]["step"] == "in_game":
                    client_states[clients_addresses]["step"] = "in_game"
                    response = "0Game Found, please prepare\n"
                    client = client_states[clients_addresses]
                    users.loc[users["ID"] == client["id"], "ALL_TIME_ROUNDS"] += 1
                    server_socket.sendto(response.encode(), clients_addresses)

            time.sleep(60)
            for clients_addresses in client_states.keys():
                if client_states[clients_addresses]["step"] == "game_waiting" or client_states[clients_addresses]["step"] == "in_game":
                    server_socket.sendto(question.encode(), clients_addresses)
            return None


    elif client["step"] == "game_waiting":
        players_count += 1
        client["step"] = "in_game"
        response = "0Game Found, please prepare\n"
        users.loc[users["ID"] == client["id"], "ALL_TIME_ROUNDS"] += 1
        server_socket.sendto(response.encode(), client_address)
        server_socket.sendto(question.encode(), client_address)
        return None

    if client["step"] == "in_game":
        number_of_answers += 1
        if data.lower() == "null":
            client["time_out"] += 1
            server_socket.sendto("0Time Out, Will considered Wrong Answer".encode(), client_address)
        elif data.lower() in answer:
            print(f"Response from {client["id"]}, Status: Correct")
            number_of_correct_answers += 1
            client["points"] += round((1 / number_of_correct_answers), 3)
            response = "0Correct Answer (: \n"
            server_socket.sendto(response.encode(), client_address)
        else:
            print(f"Response from {client["id"]}, Status: Wrong")
            server_socket.sendto("0Wrong answer !!\n".encode(), client_address)

    if number_of_answers == players_count:
        number_of_correct_answers = 0
        standings = ""
        number_of_questions += 1
        max, winner_client = -1, None
        for clients_addresses in client_states.keys():
            if client_states[clients_addresses]["step"] == "game_waiting" or client_states[clients_addresses]["step"] == "in_game":
                standings += f"Player Name:  {client_states[clients_addresses]["id"]} -- Player Points: {client_states[clients_addresses]["points"]} \n"
                if max < client_states[clients_addresses]["points"]:
                    max = client_states[clients_addresses]["points"]
                    winner_client = client_states[clients_addresses]

        for clients_addresses in client_states.keys():
            if client_states[clients_addresses]["step"] == "game_waiting" or client_states[clients_addresses]["step"] == "in_game":
                if number_of_questions != 3:
                    server_socket.sendto(("0\n" + f"The correct Answer is: {answer}\nLeading player {winner_client["id"]}\nStandings:\n" + standings).encode(), clients_addresses)
                else:
                    print(f"Winner: {winner_client}")
                    server_socket.sendto(("0\n" + f"The correct Answer is: {answer}\nWinner player {winner_client["id"]}\nStandings:\n" + standings).encode(), clients_addresses)


        if number_of_questions == 3:
            users.loc[users["ID"] == winner_client["id"], "ALL_TIME_WINS"] += 1
            question, answer, number_of_answers, players_count, number_of_questions, number_of_correct_answers = None, None, 0, 0, 0, 0
            for clients_addresses in client_states.keys():
                if client_states[clients_addresses]["step"] == "game_waiting" or client_states[clients_addresses]["step"] == "in_game":
                    server_socket.sendto("0Thanks for playing the game".encode(), clients_addresses)
                    users.loc[users["ID"] == client_states[clients_addresses]["id"], "ALL_TIME_POINTS"] += client_states[clients_addresses]["points"]
                    client_states[clients_addresses]["points"] = 0
                    client_states[clients_addresses]["step"] = "option"
                    menu(server_socket, clients_addresses, 0)
            return None

        number_of_answers = 0
        question, answer = questions_set_all(random.randint(1, 40))

        time.sleep(60)
        for clients_addresses in client_states.keys():
            if client_states[clients_addresses]["step"] == "game_waiting" or client_states[clients_addresses]["step"] == "in_game":
                server_socket.sendto(question.encode(), clients_addresses)

# Main menu
def menu(server_socket, client_address, op):
    client = client_states[client_address]
    header_message = ""
    if op == 1:
        header_message = f"Welcome {client["id"]}, Log_in Operation Succeeded\n"
    if op == 2:
        header_message = f"Welcome {client["id"]}, sign_up Operation Succeeded\n"
    starting_message = "Welcome to our game (: \nPlease Enter an option \n1- Log_In \n2- Sign_up \n3- Join a game \n4- Game_Descriptions\n5- Quit"
    header_message += starting_message
    server_socket.sendto(header_message.encode(), client_address)

# Function to handle Each client request
def handle_client(server_socket, client_address, data):
    if client_address not in client_states: # if the request we got for new client
        client_states[client_address] = {"step": "menu", "option": None, "id": f"anonymous{len(client_states)}", "pass": None, "points": 0, "time_out": 0}
        print(f"Client with Address {client_address} has joined the game")

    client = client_states[client_address] # get a pointer for client with KEY: client_address

    # if the client in first step "menu", display the main menu then return "NONE" to wait for response
    if client["step"] == "menu":
        menu(server_socket, client_address, 0)
        client["step"] = "option"
        return None

    if client["step"] == "option": # if client step is waiting for response after displaying the main menu, make the next received data is the option
        client["option"] = data

    if client["option"] == "1": # if option one go to log in function
        log_in(server_socket, client_address, data)

    elif client["option"] == "2": # if option two go to sign in function
        sign_up(server_socket, client_address, data)

    elif client["option"] == "3": # if option three go to start game function
        join_a_game(server_socket, client_address, data)

    elif client["option"] == "4": # if option 4 display the game description
        # note for '0' in the starting of the response the client will know it's a just to display ont for wait for response
        description = "0This is interactive multiplayer trivia game which needs two players at least to start the game,\n every client will go in three rounds of randoms question that will test your knowledge on the end\n of each round you will receive message of how many points you have and if answered correctly,\n or not. But beware even if the player answers correctly\n only the first player to answer correctly will win the higher point.\n HOPE YOU ENJOY PLAYING!!!!\n"
        server_socket.sendto(description.encode(), client_address)
        menu(server_socket, client_address, 0)
        pass

    elif client["option"] == "5" :
        server_socket.sendto("quit".encode(), client_address)
    else:
        server_socket.sendto(f"0{data} is not an option".encode(), client_address)
        menu(server_socket, client_address, 0)

    users.to_csv("users.csv", index=False)
    print("==============================================================\n")

def protocol_listener():

        try: # any exception here means that the server failed to connect
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # create the server socket with the family and type
            server_socket.bind((SERVER, PORT)) # bind to the socket the IP address and Port number
            print(f"UDP server is listening on {SERVER}:{PORT}") # display on the server terminal
            try: # any exception here means that the server shut down ( the while true ends )
                while True:
                    try: # any exception here means that an error occur during handle the client request
                        data, client_address = server_socket.recvfrom(1024) # receiving the data
                        print(f"Received from {client_address}:   {data.decode()}")
                        data = data.decode() # decode the received data
                        handle_client(server_socket, client_address, data) # handle ir in handle_client
                    except Exception:
                        print("Server receive a request that didn't accept")
                        continue

            except Exception:
                print("The server Shut-down")
        except Exception:
            print(f"Port {PORT} or Server {SERVER} Failed to connect")

if __name__ == "__main__":
    protocol_listener()