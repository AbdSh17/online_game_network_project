# Online Game Network Project

This project implements a simple online game with a client-server using basic oscket library, developed as part of Task 3 of the Network Project ENCS3320. The game allows multiple clients to connect to a server playing "question anwer" game type.

## Table of Contents

1. [How to Start the Game](#how-to-start-the-game)
2. [How to Play](#how-to-play)
3. [Files](#files)
4. [Requirements](#requirements)
5. [Setup and Usage](#setup-and-usage)

## How to start the game

you need seperate terminals
- Run `server.py` on one terminal to start the server.
- Run `client.py` on other terimnal (same or different PCs that conneected to the same network) as many clients you want to join the game.

# How to play

when you run the client you will recive 5 options
- `LOG IN`: for entering in a already exist account, saved in users.csv.
- `Sign up`: for creating new account.
- `Join a game`: if the user logged in or signed up it will enter in the same account, if not it will enter as anonymous.
- `Game Descriprion`: for game guidline.
- `Exit`.

## Files

- `server.py`: Contains the server-side code that manages client connections, user authentication, and game logic.

- `client.py`: Contains the client-side code that handles user input, communicates with the server, and updates the game interface.

- `users.csv`: Stores user credentials in a CSV format for registration and login purposes.

- `NetworkProject.pdf`: Provides detailed documentation of the project requirements, design, and implementation details.

## Requirements

- Python 3.x

- Required Python libraries:
  - `socket` (for networking)
  - `threading` (for managing multiple client connections)
  - `pandas` (for maniging users data)

## Setup and Usage

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/AbdSh17/online_game_network_project.git
   cd online_game_network_project
