#!/usr/bin/env python3
 
import random as r 
import time
from grid_display import GridDisplay
from grassland import Grassland , Wall , Grass , count_object, is_in_list, find_in_list , is_overpopulated
from rabbit import Rabbit




class Fox :
    """Il s'agit du prédateur.
      Cette classe définit le commportement du rennard et son évolution dans le monde """

    COLOR = (255,127,0)  # Orange comme le renard ^^

    def __init__ (self, coord : tuple[int,int] ,p_live :float = 0.99679 , p_birth : float = 0.02438 , day_without_eating : int = 0 , max_hungry_duration : int = 8 , living : bool = True)-> None :
        self.p_live = p_live
        self.coord = coord
        self.p_birth = p_birth
        self.day_without_eating = day_without_eating 
        self.max_hungry_duration = max_hungry_duration
        self.living = living 
        

    def dying (self , grassland : Grassland):
        """On définit ici les causes de mort du renard:
            - S'il est mort de vieillesse
            - s'il meurt de faim
            - S'il se retrouve bloqué par ces confrères """
        if self.living :

            p_live = r.random()
            if p_live > self.p_live :
                grassland.remove_object(self.coord)
                self.living = False

            elif self.day_without_eating > self.max_hungry_duration :
                grassland.remove_object(self.coord)
                self.living = False 

    def dying_overpopulation(self , grassland : Grassland):
        if self.living:
    
            assert  grassland.get_box(self.coord).__class__ == Fox
            neighbours = grassland.get_neighbours(self.coord)
            if is_overpopulated(neighbours , "Fox"):
                grassland.remove_object(self.coord)
                self.living = False
            
    
    def is_giving_birth ( self ):
        """On vérifie ici si le renard va laisser un rejeton au prochain mouvement"""
        if self.living :
            p_give_birth = r.random()

            if p_give_birth < self.p_birth :
                return True 
            
            return False

            
    def hunt_or_move_give_birth (self , grassland : Grassland):
        """Cette fonction a pour but de faire évoluer le rennard dans une des cases adjacentes à lui
        pour ce faire on récupère les objets qui sont autour de lui. 
        S'il y a un lapin il s'y déplace le mange et son compteur de faim redescend à 0.
        S'il n'y a aucun lapin il se déplace aléatoirement sur une case Grass et son compteur de faim augmente de 1.
        S'il ne peut pas bouger (que des cases Fox et ou wall ) il meurt.
        """
        if self.living :  # Le loup ne peut rien faire si il est deja mort  
            neighbours = grassland.get_neighbours(self.coord)
            
            baby = self.is_giving_birth()

            if baby:
                     
                    fox = Fox(self.coord) # On crée bébé_renard avec les coordonnées de maman_renard mais sans le poser sur la grille

            if is_in_list(neighbours , "Rabbit"): #Si un lapin est dans ses voisins on va aller le chercher (si il en a plusieurs on choisit au hasard)

                candidate = find_in_list (neighbours , "Rabbit") #On récupère les indices 
                obj  = neighbours[r.choice(candidate)]
                
                grassland.remove_object(obj.coord)
                obj.living = False
                grassland.move_object(self.coord, obj.coord)
                self.coord = obj.coord
                self.day_without_eating = 0
            
            else :
                candidate = find_in_list(neighbours , "Grass")
                
                obj = neighbours[r.choice(candidate)]
                grassland.move_object(self.coord , obj.coord)
                self.coord = obj.coord
                self.day_without_eating += 1

            if baby :
                grassland.place_new_object(fox.coord , fox)
    
    def act (self , grassland ):
        self.dying(grassland)
        self.dying_overpopulation(grassland)
        self.hunt_or_move_give_birth(grassland)


if __name__ == '__main__':
    pass





                


        
