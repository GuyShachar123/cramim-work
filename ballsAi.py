import pygame
import threading
import random
import time
import requests

import queue

RADIUS = 20

log_file = open("ball_log.txt", "w")

def log_message(message):
    """
    enter: message
    exit: Prints the message to terminal and writes it to the log file
    """
    print(message)                  # Print to terminal
    log_file.write(message + "\n")  # Write to file
    log_file.flush()

def create_ball(qBalls):
    """
    enter: qBalls
    exit: Generates random ball coordinates and colors and pushes them to the queue
    """
    times = random.randint(1, 17)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    for i in range(times):
        x = random.randint(RADIUS, 800 - RADIUS)
        y = random.randint(RADIUS, 600 - RADIUS)
        qBalls.put((x, y, color))
        time.sleep(0.5)
        qBalls.put((x, y, 0))



def ai_agent_commentary(red_and_blue_count):
    """
    enter: None
    exit: Periodically queries the local LLM for commentary on active balls and logs the response
    """
    url = "http://localhost:11434/api/generate"

    prompt = f"tell me how meany red and blue balls are there (there were+{red_and_blue_count})"
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

try:
    balls = int(input("Enter ball amount: "))
except Exception as e:
    print("value was not an int")
    # 5 is defult if they dont enter good input
    balls = 5
if balls == 0:
    # 5 is defult if they dont enter good input
    balls = 5
pygame.init()
screen = pygame.display.set_mode((800, 600))

red_and_blue_count = 0
threads = []
threads_closed = []
balls_alive = balls
qBalls = queue.Queue()

created_ball = 0

running = True
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
        if color != 0:
            r, g, b = color
            # i checked what values i need to put
            if (r > 150 and g < 100 and b < 100) or (b > 150 and r < 100 and g < 100):
                red_and_blue_count += 1


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
ai_agent_commentary(red_and_blue_count)
pygame.quit()
log_file.close()
