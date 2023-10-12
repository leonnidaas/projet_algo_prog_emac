#!/usr/bin/env python3
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from typing import Tuple

Coordinate = Tuple[int, int]
Color = Tuple[int, int, int]

class GridDisplay:

    def __init__(self, # l'objet à créer
                 size: Coordinate, # taille de la grille (largeur, hauteur)
                 nb_pixels_by_box: int=4, # taille en pixel d'un emplacement du couvain
                 grid_color: Color=(220, 220, 220), # couleur de la grille
                 bg_color: Color=(255, 255, 255), # couleur du fond,
                 text_color: Color=(0, 0, 0), # couleur du texte
                 period_duration: int=100, # durée d'une période (en ms)
                 ):
        """Ouvre une fenêtre contenant un grille de la taille demandée."""
        self.size = size
        self.nb_pixels_by_box = nb_pixels_by_box
        self.colors = {
            "gr": grid_color,
            "bg": bg_color,
            "tx": text_color,
        }
        self.period_duration = period_duration
        self.period = 0
        self._initialize_display()

    def _initialize_display(self) -> None:
        """(interne) Initialise pygame."""
        pygame.init()
        self.font = pygame.font.SysFont("monospace", 12)
        if (self.nb_pixels_by_box < 3 or self.nb_pixels_by_box > 20):
            raise ValueError("Box size is out of range.")
        if (self.size[0] * self.nb_pixels_by_box + 1 > 1920
            or self.size[1] * self.nb_pixels_by_box + 1 > 1080):
            raise ValueError("Size of grid is too large.")
        self.screen = pygame.display.set_mode(
            (self.size[0] * self.nb_pixels_by_box + 1,
             self.size[1] * self.nb_pixels_by_box + 1 + 20)
        )
        self._draw_grid()

    def _is_quit_event(self, event):
        """(interne) Vérifie si un événement demande la fermeture de la
        fenêtre."""
        mods = pygame.key.get_mods()
        if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
            return True
        elif (event.type == pygame.KEYDOWN
              and (event.key == pygame.K_q or event.key == pygame.K_c)
              and mods & pygame.KMOD_CTRL):
            return True
        return False
        
    def next_period(self, text="") -> bool:
        """Passe à la période suivante en vérifiant s'il faut s'arrêter puis en
        attendant le nombre de microsecondes de la période et en redessinant la
        grille vide. Retourne False si la fenêtre doit être fermée."""
        cont = True

        # render text
        label = self.font.render(f"period: {self.period}" + text, 1, self.colors["tx"])
        self.screen.blit(label, (4,self.size[1] * self.nb_pixels_by_box + 4))

        pygame.display.flip()
        for event in pygame.event.get():
            if self._is_quit_event(event):
                cont = False
        if cont:
            pygame.time.wait(self.period_duration)
            self.period += 1
            self._draw_grid()
        return cont
                   
    def _draw_grid(self) -> None:
        """(interne) Efface la fenêtre, redessine la grille et affiche le numéro
        de pérdiode"""
        self.screen.fill(self.colors["bg"])
        for x in range(self.size[0] + 1):
            pygame.draw.line(
                self.screen,
                self.colors["gr"],
                (x * self.nb_pixels_by_box, 0),
                (x * self.nb_pixels_by_box, self.nb_pixels_by_box * self.size[1]),
            )
        for y in range(self.size[1] + 1):
            pygame.draw.line(
                self.screen,
                self.colors["gr"],
                (0, y * self.nb_pixels_by_box),
                (self.nb_pixels_by_box * self.size[0], y * self.nb_pixels_by_box),
            )

    def _check_color(self, color: Color) -> None:
        """(interne) Vérifie que les composantes d'une couleur sont
        acceptables."""
        for comp in color:
            if not isinstance(comp, int):
                raise ValueError("Color component should be an integer")
            if comp < 0 or comp > 255:
                raise IndexError("Color components out of range")

    def _check_coordinates(self, pos: Coordinate) -> None:
        """(interne) Vérifie que les cordonnées sont dans la grille."""
        if not isinstance(pos[0], int) or not isinstance(pos[1], int):
                raise ValueError("coordinates should be integers")
        if pos[0] < 0 and pos[0] >= self.size[0]:
            raise IndexError(f"x({pos[0]}) out of range")
        if pos[1] < 0 and pos[1] >= self.size[1]:
            raise IndexError(f"y({pos[1]}) out of range")
            
    def draw_box(self, pos: Coordinate, color: Color) -> None:
        """Remplit la case de la grille aux coordonées 'pos' avec le couleur
        'color'."""
        self._check_coordinates(pos)
        self._check_color(color)
        pygame.draw.rect(
            self.screen,
            color,
            pygame.Rect(
                (pos[0] * self.nb_pixels_by_box + 1, pos[1] * self.nb_pixels_by_box + 1),
                (self.nb_pixels_by_box - 1, self.nb_pixels_by_box - 1)
            )
        )

if __name__ == "__main__":

    import random
    from time import time_ns

    random.seed(time_ns())

    gd = GridDisplay(
        size=(30, 30),
        nb_pixels_by_box=10,
        period_duration=2,
    )

    def random_boxes(n_max=100, theme="black"):
        if theme == "black":
            gd.colors["bg"] = (0, 0, 0)
            gd.colors["gr"] = (255, 255, 255);
            gd.colors["tx"] = (255, 255, 255);
        else:
            gd.colors["bg"] = (255, 255, 255)
            gd.colors["gr"] = (200, 200, 200);
            gd.colors["tx"] = (0, 0, 0);
        n = 0
        cont = True
        while cont == True and n < n_max:
            for i in range(400):
                x = random.randint(0,29)
                y = random.randint(0,29)
                r = random.randint(0,255)
                g = random.randint(0,255)
                b = random.randint(0,255)
                gd.draw_box((x, y), (r, g, b))
            n += 1
            cont = gd.next_period()
        return cont

    for j in range(10):
        if not random_boxes(theme="white"):
            break
        if not random_boxes(theme="black"):
            break
