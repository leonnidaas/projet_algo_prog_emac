#!/usr/bin/env python3

from grassland import Grassland

class Rabbit :

    Color = (128,128,128)
    
    def __init__ (self, p_live : float, p_birth : float, coord : tuple[int, int], grassland : Grassland, living : bool = True) -> None:
        self.p_live = p_live
        self.p_birth = p_birth
        self.coord = coord
        self.living = living
        grassland.objects [coord] = self

    def x(self) :
        return self.coord[0]

    def y(self) :
        return self.coord[1]

    def move (self) :
        pass
    # grassland.objects [coord] = self  /!\ pas oublier de modifier les coord de l'objet
    

    def dying (self) :
        """Définit si le lapin meurt ou non d'une cause d'over-population
        c'est-à-dire que tous ces mouvements sont bloqués par d'autres lapins"""
        if self.living :
            neighbours = Grassland.get_neighbours(self, self.coord)
            for elt in neighbours :                                     # on regarde pour tous les voisins de Rabbit, s'ils sont occupés par Rabbit
                                                                        # ou par Wall (si oui, alors il meurt au prochain tour)
                if elt != "Rabbit" and elt != "Wall" :
                    pass
                    
            self.living = False


    def give_birth (self) :
        pass


