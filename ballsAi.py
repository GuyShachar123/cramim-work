import pygame
import threading
import random
import time
import requests

import queue

RADIUS = 20

log_file = open("ball_log.txt", "w")

def log_message(message):
    print(message)                  # Print to terminal
    log_file.write(message + "\n")  # Write to file
    log_file.flush()

def create_ball(qBalls):
    """
    Thread worker for a single ball: moves it to random places on the screen.

    :param qBalls: queue shared with the main thread, used to send draw/erase requests
    :return: None
    """
    times = random.randint(1, 17)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    for i in range(times):
        x = random.randint(RADIUS, 800 - RADIUS)
        y = random.randint(RADIUS, 600 - RADIUS)
        qBalls.put((x, y, color))
        time.sleep(0.5)
        qBalls.put((x, y, 0))

global balls_alive 


def ai_agent_commentary():
    url = "http://localhost:11434/api/generate"
    while running:
        prompt = f"There are currently {balls_alive} active balls. Write a short status report."
        data = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(url, json=data, timeout=3)
            if response.status_code == 200:
                reply = response.json().get("response", "")
                log_message(f"[AI Agent]: {reply}")
        except Exception as e:
            print(e)




balls = int(input("enter amount of balls: "))
pygame.init()
screen = pygame.display.set_mode((800, 600))


threads = []
threads_closed = []
balls_alive = balls
qBalls = queue.Queue()

created_ball = 0

running = True
olama_t = threading.Thread(target=ai_agent_commentary)
olama_t.start()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if created_ball < balls:
        t = threading.Thread(target=create_ball, daemon=True, args=(qBalls,))
        t.start()
        threads.append(t)
        log_message(f"[{t.name}] Ball created")
        created_ball += 1


    if not qBalls.empty():
        x, y, color = qBalls.get()
        pygame.draw.circle(screen, color, (x, y), RADIUS)
        pygame.display.flip()


    for t in threads:
        if not t.is_alive() and t not in threads_closed and created_ball >= balls:
            balls_alive -= 1
            threads_closed.append(t)
            log_message(f"[{t.name}] Ball finished")
            log_message(f"there are {balls_alive} balls alive")

    if balls_alive == 0:
        running = False



pygame.quit()
log_file.close()