#!/usr/bin/env python3
import sys
import random
from time import time_ns
from grid_display import GridDisplay
from convert import str_to_definition, str_to_float, str_to_positive_int


class Ball:
    """Balles rebondissantes"""

    # constantes de classe
    DIRECTIONS = [
        (-1, -1), (-1, 1), (1, 1), (1, -1),
        (0, 1), (1, 0), (-1, 0), (0, -1),
    ]
    COLORS = [(240, 50, 50), (0, 200, 0), (0, 100, 255)]

    # paramètres de classe
    p_change_direction = 0.01
    p_dup = 0.001

    def __init__(self):
        self.direction = random.choice(self.DIRECTIONS)
        self.color = random.choice(self.COLORS)

    def change_direction(self):
        # changement de direction probabiliste
        if random.random() < Ball.p_change_direction:
            self.direction = random.choice(self.DIRECTIONS)

    def get_future_position_with_bounce(self, sp, xy):
        nx = xy[0] + self.direction[0]
        if nx < 0 or nx >= sp.width:
            self.direction = (-self.direction[0], self.direction[1])
            nx = xy[0] + self.direction[0]
        ny = xy[1] + self.direction[1]
        if ny < 0 or ny >= sp.height:
            self.direction = (self.direction[0], -self.direction[1])
            ny = xy[1] + self.direction[1]
        return (nx, ny)

    def move_or_death(self, sp, xy, nxy):
        # tentative de déplacement
        if isinstance(sp.get_box_content(nxy), BlackHole):
            # déplacement impossible: la balle (courante) disparaît
            sp.remove_ball(xy)
        else:
            if isinstance(sp.get_box_content(nxy), Ball):
                # on détruit la balle (visée)
                sp.remove_ball(nxy)
            else:
                # déplacement
                sp.move_object(xy, nxy)
                # duplication probabiliste
                if random.random() < Ball.p_dup:
                    sp.add_new_ball(xy)

    def act(self, sp, xy):
        self.change_direction()
        nxy = self.get_future_position_with_bounce(sp, xy)
        self.move_or_death(sp, xy, nxy)

    def get_color(self):
        return self.color


class BlackHole:
    """Trous noirs"""
    COLOR = (0, 0, 0)

    def __init__(self):
        pass

    def act(self, sp, xy):
        pass

    def get_color(self):
        return self.COLOR


class Space:
    """L'espace de simulation."""

    def __init__(self, gd):
        self.gd = gd
        self.width = gd.size[0]
        self.height = gd.size[1]
        # objects est un dictionnaire dont la clé est un tuple (la
        # position) et dont la valeur est un objet contenu à cette
        # position.
        self.objects = {}

    def get_box_content(self, xy):
        """retourne ce qui est présent à la position demandée"""
        assert xy[0] >= 0 and xy[0] < self.width, f"Bad x in {xy}"
        assert xy[1] >= 0 and xy[1] < self.height, f"Bad y in {xy}"
        return self.objects.get(xy, None)

    def get_random_position(self):
        return (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
    
    def get_random_empty_position(self):
        assert self.width * self.height - len(self.objects) > 0, "No empty position"
        pos = self.get_random_position()
        while self.get_box_content(pos) is not None:
            pos = self.get_random_position()
        return pos
    
    def remove_ball(self, xy):
        obj = self.get_box_content(xy)
        assert obj is not None, f"Can't remove ball from empty position {xy}"
        assert isinstance(obj, Ball), f"Content of {xy} is not a ball"
        del self.objects[xy]

    def move_object(self, xy, nxy):
        obj = self.get_box_content(xy)
        assert obj is not None, "Can't move object: box {xy} is empty"
        assert self.get_box_content(nxy) is None, "Can't move object: box {xy} is not empty"
        del self.objects[xy]
        self.objects[nxy] = obj

    def add_new_ball(self, xy):
        assert self.get_box_content(xy) is None
        self.objects[xy] = Ball()

    def add_random_ball(self):
        assert self.width * self.height - len(self.objects) > 0
        pos = self.get_random_empty_position()
        self.add_new_ball(pos)

    def populate_with_balls(self, n):
        for i in range(n):
            self.add_random_ball()

    def add_new_black_hole(self, xy):
        assert self.get_box_content(xy) is None
        self.objects[xy] = BlackHole()

    def add_random_black_hole(self):
        pos = self.get_random_empty_position()
        self.add_new_black_hole(pos)

    def populate_with_black_holes(self, n):
        for i in range(n):
            self.add_random_black_hole()

    def get_nb_objects(self):
        nb_objects = {}
        for obj in self.objects.values():
            obj_class = type(obj).__name__
            if obj_class not in nb_objects.keys():
                nb_objects[obj_class] = 0
            nb_objects[obj_class] += 1
        return nb_objects

    def act_objects(self):
        # copie du dictionnaire en début de période (indispensable pour
        # pouvoir le parcourir alors qu'il risque d'être modifié durant
        # son parcours).
        objects_copy = dict(self.objects)
        # chaque objet (dans l'ordre d'ajout au dictionnaire) effectue
        # ses actions
        for pos, object in objects_copy.items():
            # si l'objet existe toujours
            if self.get_box_content(pos) is object:
                # on fournit à l'objet l'espace dans lequel il évolue et sa
                # position
                object.act(self, pos)

    def draw_objects(self):
        for pos, object in self.objects.items():
            self.gd.draw_box(pos, object.get_color())


def usage(error):
    """
    Affiche le message 'error',
    rappelle à l'utilisateur l'usage du script,
    et arrête la script en retournant 1 au système.
    """
    print(
        f"Erreur -- {error}\n"
        f"Usage: {sys.argv[0]} seed grid_size nb_balls nb_black_holes p_dup p_change_direction duration\n"
        "\n"
        "                seed: (un mot) graine pour le générateur aléatoire\n"
        "           grid_size: (sous la forme 19x30) taille de la grille\n"
        "            nb_balls: nombre de balles\n"
        "      nb_black_holes: nombre de trous noirs\n"
        "               p_dup: probabilité de duplication d'une balle\n"
        "  p_change_direction: probabilité de changement de direction d'une balle\n"
        "            duration: durée d'affichage (en ms) d'une période\n"
        "\n"
        "Simule des balles qui rebondissent dans un espace discrétisé.",
        file=sys.stderr,
    )
    sys.exit(1)


def decode_arguments():
    """Arguments attendus: graine, taille de grille, nb de balles, nb
    de trous noirs, probabilité de duplication d'une balle, probabilité
    de changement de direction d'une balle, durée d'une période."""

    # le nombre d'arguments
    len(sys.argv) == 8 or usage("nombre d'arguments incorrect")

    # numéro de l'argument à décoder
    arg_num = 1

    # la graine (un mot)
    seed = sys.argv[arg_num]
    arg_num += 1

    # la taille de la grille (ex: 100x100)
    grid_size = str_to_definition(sys.argv[arg_num])
    grid_size is not None or usage(f"taille de grille invalide: '{sys.argv[arg_num]}'")
    (grid_size[0] >= 2 and grid_size[1] >= 2) or usage(f"grille trop petite: '{sys.argv[arg_num]}'")
    arg_num += 1

    # le nombre de balles
    nb_balls = str_to_positive_int(sys.argv[arg_num])
    nb_balls is not None or usage(f"nombre de balles invalide: '{sys.argv[arg_num]}'")
    arg_num += 1

    # le nombre de trous noirs
    nb_black_holes = str_to_positive_int(sys.argv[arg_num])
    nb_black_holes is not None or usage(f"nombre de trous noirs invalide: '{sys.argv[arg_num]}'")
    arg_num += 1

    # probabilité de duplication d'une balle
    p_dup = str_to_float(sys.argv[arg_num])
    p_dup is not None or usage(f"probabilité de duplication invalide: '{sys.argv[arg_num]}'")
    (p_dup >= 0 and p_dup < 1) or usage("probabilité de duplication hors intervalle [0, 1[")
    arg_num += 1

    # probabilité de changement de direction
    p_change_direction = str_to_float(sys.argv[arg_num])
    p_change_direction is not None or usage(f"probabilité de changement de direction invalide: '{sys.argv[arg_num]}'")
    (p_change_direction >= 0 and p_change_direction < 1) or usage("probabilité de changement de direction hors intervalle [0, 1[")
    arg_num += 1

    # la durée à l'écran (en ms) d'une période
    duration = str_to_positive_int(sys.argv[arg_num])
    duration is not None or usage(
        f"durée d'affichage de période invalide: '{sys.argv[arg_num]}'"
    )
    arg_num += 1

    return (seed, grid_size, nb_balls, nb_black_holes, p_dup, p_change_direction, duration)


def main():
    NB_PIXELS_BY_BOX = 10

    (seed, grid_size, nb_balls_init, nb_black_holes_init, p_dup, p_change_direction, duration) = decode_arguments()

    if seed == "0":
        seed = f"{time_ns():_d}"
        print(f"Seed: {seed}")
    random.seed(seed)

    Ball.p_dup = p_dup
    Ball.p_change_direction = p_change_direction

    gd = GridDisplay(
        grid_size,
        nb_pixels_by_box=NB_PIXELS_BY_BOX,
        period_duration=duration,
    )

    sp = Space(gd)
    sp.populate_with_balls(nb_balls_init)
    sp.populate_with_black_holes(nb_black_holes_init)
    sp.draw_objects()
    nb_obj = sp.get_nb_objects()
    text = ", ".join(f"{name}: {nb_obj[name]}" for name in sorted(nb_obj.keys()))
    while gd.next_period(text=", " + text) and gd.period < 5000 :
        sp.act_objects()
        nb_objects = sp.get_nb_objects()
        if 'Ball' not in nb_objects.keys():
            sp.populate_with_balls(nb_balls_init)
            nb_objects['Ball'] = nb_balls_init
        sp.draw_objects()
        text = ", ".join(f"{name}: {value}" for name, value in nb_objects.items())



if __name__ == "__main__":
    main()
