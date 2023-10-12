#!/usr/bin/env python3

from grid_display import GridDisplay 

class Wall :
    """C'est ce qui définit les limites tu terrain"""
    def __init__ (self):
        pass

class Grassland :
    """l'espace bidimentionel dans lequel nos deux populations évoluent"""

    def __init__ (self , gd : GridDisplay):
        self.gd = gd
        self.width = gd.size[0]  # int
        self.height = gd.size[1] # int 
        self.objects = {}

    def get_box (self , coord: tuple[int,int]):
        """Donne l'objet en coordonnée 'coord = [x,y] ' sur la grille.
            Si il n'y a pas d'objet retourne None.  
        """
        assert -1 <= coord[0] <= self.width
        assert -1 <= coord[1] <= self.height
        if coord[0] == self.width or coord[1] == self.height or coord[0] < 0 or coord[1] < 0:
            return Wall
        else :
            return self.objects.get(coord , None)
    
    def get_neighbours (self , coord: tuple[int,int])->dict  :  # FONCTION A TESTER !!!

        """Renvoie une liste sous forme de matrice avec au centre coord et autour les objets exemple liste = [ Rabbit-62, None ,         None,
                                                                                                               None  , objet central, None,
                                                                                                               Wall  , Wall ,         Wall ] """ 
        x = coord[0]
        y = coord[1]
        liste = []

        for i in range (x-1 , x+2) :
                for j in range (y-1 , y+2) :
                    liste.append(self.get_box( (i,j) ) )
        return liste 


if __name__ == "__main__" :

    test = Grassland(GridDisplay( ) )

