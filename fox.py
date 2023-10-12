#!/usr/bin/env python3
 
import random as r 
import time
from grid_display import GridDisplay
from grassland import Grassland , Wall
from rabbit import Rabbit

seed_value = time.time_ns()
r.seed(seed_value)
print(f"seed: {seed_value:_d} ns")


def is_in_list (list , object ):
    for e in list :
        if type(e).__name__ == object:
            return True
    return False 


def find_in_list ( list , object ):
    """retourne les index de l'élément voulu dans une liste """
    return [i for i , e in enumerate(list) if type(e).__name__ == object]



class Fox :

    COLOR = (255,127,0)  # Orange comme le renard ^^

    def __init__ (self, p_live :float , p_birth : float , coord : list[int,int] , grassland : Grassland ,day_without_eating : int = 0 , max_hungry_duration : int = 5 , living : bool = True)-> None :
        self.p_live = p_live
        self.coord = coord
        self.p_birth = p_birth
        self.day_without_eating = day_without_eating 
        self.max_hungry_duration = max_hungry_duration
        self.living = living 
        grassland.objects[coord] = self
    
    def x(self):
        return  self.coord[0]
    
    def y(self):
        return  self.coord[1]

    def dying (self):
        """On définit ici les causes de mort du renard:
            - S'il est mort de veillesse
            - s'il meurt de faim
            - S'il se retrouve bloqué par ces confrères """
        if self.living :

            p_live = r.random()
            if p_live > self.p_live :
                self.living = False

            if self.day_without_eating > self.max_hungry_duration :
                self.living = False 

    def dying_overpopulation(self , grassland : Grassland):
        if self.living:
            
            x = self.x() # int 
            y = self.y() # int

            assert  grassland.get_box(x,y) == Fox

            for i in range (x-1 , x+2) :
                for j in range (y-1 , y+2) :
                    if grassland.get_box(i,j) == Fox or grassland.get_box(i,j) == Wall : 
                        pass

                    else :
                        return
                    
            self.living = False 
            
    def hunt_or_move (self , grassland : Grassland):
        """Cette fonction a pour but de faire évoluer le rennard dans une des cases adjacentes à lui
        pour ce faire on récupère les objets qui sont autour de lui. 
        S'il y a un lapin il s'y déplace le mange et son compteur de faim redescend à 0.
        S'il n'y a aucun lapin il se déplace aléatoirement sur une case None et son compteur de faim augmente de 1.
        S'il ne peut pas bouger (que des cases Fox et ou wall ) il meurt.
        """
        if self.living :  # Le loup ne peut rien faire si il est deja mort  
            neighbours = grassland.get_neighbours(self.coord)
            if is_in_list(neighbours , Rabbit):
                candidate = find_in_list (neighbours , Rabbit)
                r.choice(candidate)
                


                


        
