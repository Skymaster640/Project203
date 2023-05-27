import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ipAddress = "127.0.0.1"
port = 8000
server.bind((ipAddress,port))

server.listen()

listofClients = []
nicknames=[]

questions = [
    "What was the first Pokemon to ever be created? \n a.Bulbasaur\n b.Mew\n c.Rhydon\n d.Arceus",
    "Which of these Kirby Copy Abilities doesn't exist? \n a.Mage\n b.Cupid\n c.Light\n d.Circus",
    "Which of these Super Mario games does not contain a Goomba in the first level? \n a.Super Mario Bros. 3\n b.Super Mario World\n c.Super Mario 64\n d.New Super Mario Bros. Wii",
    "In the Disney TV Show, The Owl House, what was the first Glyph that Luz learns? \n a.Plant\n b.Ice\n c.Fire\n d.Light",
    "In the game, Portal. Which of these Test Chambers introduced the Turrets? \n a.Test Chamber 9\n b.Test Chamber 16\n c.Test Chamber 15\n d.Test Chamber 10",
    "In World of Warcraft, which race has the racial ability called Shadowmeld? \n a.Night Elf\n b.Orc\n c.Troll\n d.Worgen",
    "Which of these characters from Super Smash Bros first made their appearance in Melee? \n a.Ness\n b.King Dedede\n c.Ice Climbers\n d.Rosalina & Luma",
    "Which of these Legend of Zelda games introduced the character, Tingle? \n a.Twilight Princess\n b.Wind Waker\n c.Ocarina of Time\n d.Majora's Mask",
    "Which of these TV Shows were made by Alex Hirsch? \n a.Steven Universe\n b.Gravity Falls\n c.Amphibia\n d.The Ghost and Molly McGee",
    "In the game, Spore. Which of these stages doesn't exist? \n a.Space Stage\n b.Civilization Stage\n c.Aquatic Stage\n d.Cell Stage",
    
    
]

answers = ['c', 'a', 'b', 'd', 'b', 'a', 'c', 'd', 'b', 'c']

def clientThread(conn,nickname):
    score=0
    conn.send("Welcome to the quiz game!".encode('utf-8'))
    conn.send("You will recieve a question. The answer to that question should be one of a, b, c, or d\n".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index,question,answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
            else:
                remove(conn)
                removenickname(nickname)
        except:
            continue

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def remove(connection):
    if connection in listofClients:
        listofClients.remove(connection)

def removenickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

while True:
    conn,addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname=conn.recv(2048).decode('utf-8')
    listofClients.append(conn)
    nicknames.append(nickname)
    print(nickname +" Connected!")
    new_Thread = Thread(target=clientThread,args=(conn,nickname))
    new_Thread.start()
    

