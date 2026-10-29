import  threading
import  random
import  pygame
import time

WIDTH, HEIGHT = 800, 600
class ball:
    def __init__(self, ball_id):
        """
        enter: ball_id
        exit: Initializes ball attributes (id, radius, x, y, color)
        """
        self.id = ball_id
        self.radius = 20
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def move(self):
        """
        enter: None
        exit: Randomly repositions the ball within bounds
        """
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)


def ball_thread(ball):
    """
    enter: ball
    exit: Moves the ball in a loop with delays and prints completion
    """
    print(f"ball id:{ball.id}")
    amount_to_move = random.randint(1,10)
    for i in range(amount_to_move):
        ball.move()
        time.sleep(1)
    print(f"{ball.id} finished")

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Display a Ball")
    ball_radius = 20
    ball_x,ball_y = 0,0

    try:
        balls_num = int(input("Enter ball amount: "))
    except Exception as e:
        print("value was not an int")
        # 5 is defult if they dont enter good input
        balls_num = 5
    if balls_num == 0:
        # 5 is defult if they dont enter good input
        balls_num = 5
    ball_list = []
    for i in range(balls_num):
        ball_list.append(ball(i))
    threads_list = []
    for ball in ball_list:
        t = threading.Thread(target=ball_thread, args=(ball,))
        threads_list.append(t)
        t.start()
    # to break from the nesxted loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #check when to stop program
        active_threads = [t.is_alive() for t in threads_list]
        if not any(active_threads):
            running = False

        screen.fill((0, 0, 0))
        for ball in ball_list:
            pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.radius)
        pygame.display.flip()
        pygame.time.delay(30)
    pygame.quit()

