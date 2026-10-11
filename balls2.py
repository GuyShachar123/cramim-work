import math
import  threading
import  random
import  pygame
import time
import multiprocessing

WIDTH, HEIGHT = 800, 600
class ball:
    def __init__(self, ball_id):
        self.id = ball_id
        self.radius = 20
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def move(self):
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)


def  ball_Process(ball_obj, to_detector_queue, print_queue):


        amount_to_move = random.randint(1,10)
        print_queue.put(f"ball id:{ball.id}")
        for i in range(amount_to_move):
            ball.move()
            to_detector_queue.put(('move', ball_obj)
            time.sleep(1)

        print_queue.put(f"{ball.id} finished")

def check_distance(b1, b2):
    """Returns True if two balls are overlapping."""
    dx = b1.x - b2.x
    dy = b1.y - b2.y
    return math.sqrt((dx ** 2) + (dy ** 2)) < 40

def check_collision(to_detector_queue,detector_to_gui_queue):
    while True:
        ball = to_detector_queue.get()
        to_detector_queue.put(-1)
        while not detector_to_gui_queue.empty():
            ball2 = to_detector_queue.get()
            to_detector_queue.put(ball2)


                for ball2 in ball_list:
                    if ball2 != ball:
                        dx = ball.x - ball2.x
                        dy = ball.y - ball2.y
                        distance = math.sqrt((dx ** 2) + (dy ** 2))
                        if distance <40:
                            ball2.move()




def print_p(print_queue):


    while True:
       msg = print_queue.get()
       print(msg)



if __name__ == '__main__':
    pygame.init()



    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Display a Ball")
    ball_radius = 20
    ball_x,ball_y = 0,0

    print_queue = multiprocessing.Queue()
    ball_to_detector_queue = multiprocessing.Queue()
    detector_to_gui_queue = multiprocessing.Queue()

    balls_num = int(input("enter ball amount"))


    Process_list = []
    ball_list = [ball(i) for i in range(balls_num)]
    p3 = multiprocessing.Process(target=print_p, args=(print_queue,))
    p3.start()

    ball_processes = []
    for ball in ball_list:
        p = multiprocessing.Process(target=ball_Process, args=(ball, ball_to_detector_queue, print_queue))
        ball_processes.append(p)
        p.start()



    p2 = multiprocessing.Process(target=check_collision, args=(ball_to_detector_queue,))


    p2.start()



    # to break from the nesxted loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #check when to stop program
        active_threads = [p.is_alive() for p in Process_list]
        if not any(active_threads):
            running = False

        screen.fill((0, 0, 0))
        for ball in ball_list:
            pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.radius)
        pygame.display.flip()
        pygame.time.delay(30)
    pygame.quit()
