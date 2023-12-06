# Score Counter
import pygame as pg

class ScoreCounter:
    def __init__(self, font_path, font_size, x, y):
        self.score = 0
        self.font = pg.font.Font(None, font_size)
        self.position = (x, y)

    def increase_score(self, points):
        self.score += points

    def decrease_score(self, points):
        self.score -= points
        if self.score < 0:
            self.score = 0  # Prevent negative scores

    def get_score(self):
        return self.score

    def reset_score(self):
        self.score = 0

    def render_score(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_text, self.position)