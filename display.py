import pygame
class Display:
    def __init__(self, map_):
        self.map = map_
    # def update(self)
    def start_render(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.map.width, self.map.height))
        pygame.display.set_caption("Prask Royal")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
        pygame.quit()
