#!/usr/bin/env python3

import random as r
from grassland import Grassland , Wall , Grass , count_object, find_in_list, is_in_list, is_overpopulated

class Rabbit :

    COLOR = (128,128,128)
    
    def __init__ (self, coord : tuple[int, int] , p_birth : float = 0.04719, p_live : float = 0.9976 , living : bool = True) -> None:
        self.p_live = p_live
        self.p_birth = p_birth
        self.coord = coord
        self.living = living

    # def x(self) :
    #     return self.coord[0]

    # def y(self) :
    #     return self.coord[1]

    def dying (self, grassland : Grassland) :
        """Définit si le lapin meurt ou non d'une cause de :
        - over-population i.e. que tous ses mouvements sont bloqués par d'autres lapins
        - vieilesse"""
        if self.living :
            # mort de vieillesse
            living = r.random()
            if living > self.p_live :
                grassland.remove_object(self.coord)
                self.living = False

        if self.living :
            # mort d'over-population
            assert grassland.get_box(self.coord).__class__ == Rabbit, grassland.get_box(self.coord).__class__.__name__
            neighbours = grassland.get_neighbours(self.coord)
            
            if is_overpopulated(neighbours, "Rabbit") :
                grassland.remove_object(self.coord)
                self.living = False
            
            # for elt in neighbours :                                     # on regarde pour tous les voisins de Rabbit, s'ils sont occupés par Rabbit
            #                                                             # ou par Wall (si oui, alors il meurt au prochain tour)
            #     if elt.__class__ == Grass :  
            #         return
            # grassland.remove_object(self.coord)
            # self.living = False

            
        

    def is_giving_birth (self) :
        """Retourne un booléen pour savoir si ce lapin donne naissance à un nouveau lapin"""
        if self.living :
            p_give_birth = r.random()
            if p_give_birth < self.p_birth :
                return True
            else : return False

    def move_and_give_birth (self, grassland : Grassland) :
        if self.living :
            neighbours = grassland.get_neighbours(self.coord)
            birth = self.is_giving_birth()
            if birth :
                baby = Rabbit(self.coord)

            # faire bouger le lapin pour choisir une nouvelle position
            candidates = find_in_list(neighbours, "Grass")
            obj = neighbours[r.choice(candidates)]
            grassland.move_object(self.coord, obj.coord)
            # grassland.objects[self.coord] = self
            self.coord = obj.coord
            # print(grassland.objects)
        
            # placer le bébé à la position de la maman
            if birth :
                grassland.place_new_object(baby.coord, baby)    # grassland.objects [coord] = self  /!\ pas oublier de modifier les coord de l'objet

    def act(self, grassland) :
        self.dying (grassland)
        self.move_and_give_birth (grassland)

