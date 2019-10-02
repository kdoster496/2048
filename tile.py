import pygame


class Tile:
    def __init__(self, val, w, boxColor, textColor):
        w = int(w)
        self.numDisplay = val
        assert val % 2 == 0

        self.surface = pygame.Surface((w, w))
        pygame.draw.rect(self.surface, boxColor, (0, 0, w, w))

        self.font = getScaledFont(w, w, str(self.numDisplay), 'Comic Sans')
        self.text = self.font.render(str(self.numDisplay), 1, textColor)
        self.text_rect = self.text.get_rect(center=(w / 2, w / 2))
        self.surface.blit(self.text, self.text_rect)



def getScaledFont(max_w, max_h, text, font_name):
    font_size = 0
    font = pygame.font.SysFont(font_name, font_size)
    w, h = font.size(text)
    while w < max_w and h < max_h:
        font_size += 1
        font = pygame.font.SysFont(font_name, font_size)
        w, h = font.size(text)
    return pygame.font.SysFont(font_name, font_size - 1)
