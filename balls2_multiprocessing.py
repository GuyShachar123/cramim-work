import math
import random
import pygame
import time
import multiprocessing

WIDTH, HEIGHT = 800, 600

class ball:
    def __init__(self, ball_id):
        """
        enter: initialize ball object
        exit: ball object created with id, radius, position, and color
        """
        self.id = ball_id
        self.radius = 20
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def move(self):
        """
        enter: call move on ball object
        exit: ball position updated to new random coordinates
        """
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)


def ball_Process(ball_obj, to_detector_queue, print_queue):
    """
    enter: start ball process execution
    exit: ball process finished and sentinel sent to queue
    """
    print_queue.put(f"Ball id:{ball_obj.id} started")
    amount_to_move = random.randint(1, 10)
    
    for i in range(amount_to_move):
        ball_obj.move()
        to_detector_queue.put(ball_obj)
        time.sleep(0.5)

    print_queue.put(f"Ball {ball_obj.id} finished")
    to_detector_queue.put(None)


def check_collision(to_detector_queue, detector_to_gui_queue, print_queue, total_balls):
    """
    enter: start collision detection process
    exit: collision detection process finished all checks
    """
    print_queue.put("Collision detector process started")
    active_balls = {}
    finished_balls_count = 0
    
    while finished_balls_count < total_balls:
        ball_obj = to_detector_queue.get()
        
        if ball_obj is None:
            finished_balls_count += 1
            print_queue.put(f"Collision detector: A ball finished. Active balls remaining: {total_balls - finished_balls_count}")
            continue
            
        active_balls[ball_obj.id] = ball_obj
        
        for other_id, other_ball in list(active_balls.items()):
            if other_id != ball_obj.id:
                dx = ball_obj.x - other_ball.x
                dy = ball_obj.y - other_ball.y
                distance = math.sqrt((dx ** 2) + (dy ** 2))
                if distance < 40:
                    other_ball.move()
                    
        for b in active_balls.values():
            detector_to_gui_queue.put(b)
            
    print_queue.put("Collision detector process finished")


def print_p(print_queue):
    """
    enter: start print background process
    exit: print process terminated upon receiving None
    """
    while True:
        msg = print_queue.get()
        if msg is None:
            break
        print(msg)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My Jumping Balls - Processes")

    print_queue = multiprocessing.Queue()
    ball_to_detector_queue = multiprocessing.Queue()
    detector_to_gui_queue = multiprocessing.Queue()
    try:
        balls_num = int(input("Enter ball amount: "))
    except Exception as e:
        print("value was not an int")
        #5 is defult if they dont enter good input
        balls_num = 5
    if balls_num == 0:
        # 5 is defult if they dont enter good input
        balls_num = 5



    p3 = multiprocessing.Process(target=print_p, args=(print_queue,))
    p3.start()
    print_queue.put("Print process started")

    ball_list = [ball(i) for i in range(balls_num)]

    p2 = multiprocessing.Process(target=check_collision, args=(ball_to_detector_queue, detector_to_gui_queue, print_queue, balls_num))
    p2.start()

    ball_processes = []
    for b in ball_list:
        p = multiprocessing.Process(target=ball_Process, args=(b, ball_to_detector_queue, print_queue))
        ball_processes.append(p)
        p.start()

    Process_list = ball_processes + [p2]
    #i draw all each frame cause else they only flush for a second
    running = True
    clock = pygame.time.Clock()
    gui_active_balls = {}
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not any(p.is_alive() for p in ball_processes):
            if not p2.is_alive():
                running = False

        while not detector_to_gui_queue.empty():
            updated_ball = detector_to_gui_queue.get()
            if updated_ball is not None:
                gui_active_balls[updated_ball.id] = updated_ball

        screen.fill((0, 0, 0))
        
        for ball_obj in gui_active_balls.values():
            pygame.draw.circle(screen, ball_obj.color, (ball_obj.x, ball_obj.y), ball_obj.radius)
            
        pygame.display.flip()
        clock.tick(30)

    print("Shutting down all processes...")
    
    for p in ball_processes:
        if p.is_alive():
            p.terminate()
            p.join()

    if p2.is_alive():
        p2.terminate()
        p2.join()

    print_queue.put(None)
    p3.join()

    pygame.quit()
    print("Program exited successfully.")
