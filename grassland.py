#!/usr/bin/env python3

from grid_display import GridDisplay 
import random as r
import time

seed_value = time.time_ns()
r.seed(seed_value)
print(f"seed: {seed_value:_d} ns")

def count_object ( objects , object):
    return len ( [v for k,v in objects.items() if v is objects])

def is_in_list (list , object ):
    for e in list :
        if e.__class__.__name__ == object:
            return True
    return False 

def find_in_list ( list , object : str ):
    """retourne les index de ou des éléments voulu dans une liste 
    /!\ object est un str !!"""
    return [i for i , e in enumerate(list) if e.__class__.__name__ ==  object]



def is_overpopulated ( list , object: str)->bool:
    """La taille de la liste est connue et dois etre de 9
    /!\ object est un str !!"""
    return [i for i , e in enumerate(list) if e.__class__.__name__ ==  object or e.__class__.__name__ == "Wall" ] == [0,1,2,3,4,5,6,7,8]


class Wall :
    """C'est ce qui définit les limites du terrain"""
    def __init__ (self):
        pass


class Grass :
    COLOR = (0,100,0)
    """Ce sont les cases libres """
    def __init__  (self , coord ):
        self.coord = coord
        
    def act(self , grassland):
        pass



class Grassland :
    """l'espace bidimentionel dans lequel nos deux populations évoluent"""

    def __init__ (self , gd : GridDisplay):
        self.gd = gd
        self.width = gd.size[0]  # int
        self.height = gd.size[1] # int s
        self.objects = {}

    def move_object (self , coord , new_coord):
        obj = self.get_box(coord)
        assert self.get_box(new_coord).__class__ is Grass , "Can't move here, there is something"
        self.objects[new_coord] = obj
        self.objects[coord] = Grass(coord)

    def remove_object(self, coord):
        self.objects[coord] = Grass(coord)


    def get_box (self , coord) -> object:
        """Donne l'objet en coordonnée 'coord = [x,y] ' sur la grille.
            Si il n'y a pas d'objet retourne Grass.  
        """
        
        assert -1 <= coord[0] <= self.width
        assert -1 <= coord[1] <= self.height
        if coord[0] == self.width or coord[1] == self.height or coord[0] < 0 or coord[1] < 0:
            return Wall()
        else :
            return self.objects.get(coord , Grass(coord))
    
    def get_neighbours (self , coord: tuple[int,int])->list  :  # FONCTION A TESTER !!!

        """Renvoie une liste sous forme de matrice avec au centre coord et autour les objets exemple liste = [ Rabbit-62, Grass ,         Grass,
                                                                                                               Grass  ,    objet central, Grass,
                                                                                                               Wall  ,    Wall ,         Wall ] """ 
        x = coord[0]
        y = coord[1]
        liste = []

        for i in range (x-1 , x+2) :
                for j in range (y-1 , y+2) :
                    liste.append(self.get_box( (i,j) ) )
        return liste 

    def get_random_position(self):
        return (r.randint(0, self.width - 1), r.randint(0, self.height - 1))
    
    def get_random_empty_position(self):
        assert self.width * self.height - len(self.objects) > 0, "No empty position"
        pos = self.get_random_position()
        
        while self.get_box(pos).__class__ is not Grass:
            pos = self.get_random_position()
        return pos
    
    def act_objects(self):
        # copie du dictionnaire en début de période (indispensable pour
        # pouvoir le parcourir alors qu'il risque d'être modifié durant
        # son parcours).
        objects_copy = dict(self.objects)
        # chaque objet (dans l'ordre d'ajout au dictionnaire) effectue
        # ses actions
        for pos, object in objects_copy.items():
            # si l'objet existe toujours
            if self.get_box(pos) is object:
                # on fournit à l'objet l'espace dans lequel il évolue et sa
                # position
                object.act(self)

    def place_new_object(self, coord , object):
        assert self.get_box(coord).__class__ is Grass , f"il faut de l'herbe pour poser un animal c'est {self.get_box(coord).__class__}"
        self.objects[coord] = object
    
    def populate_with_foxes(self , nb_fox):
        for i in range (nb_fox):
            coord = self.get_random_empty_position()
            self.place_new_object(coord , Fox(coord) )
    
    def populate_with_rabbits(self , nb_fox):
        for i in range (nb_fox):
            coord = self.get_random_empty_position()
            self.place_new_object(coord , Rabbit(coord ) )
    
    def get_nb_objects(self):
        nb_objects = {}
        for obj in self.objects.values():
            obj_class = type(obj).__name__
            if obj_class not in nb_objects.keys():
                nb_objects[obj_class] = 0
            nb_objects[obj_class] += 1
        return nb_objects
    
    def draw_objects(self):
        for coord, object in self.objects.items():
            if type(coord) != tuple :
                print(self.objects)
            assert type (coord) == tuple , type(coord)
            self.gd.draw_box(coord, object.COLOR)


if __name__ == "__main__" :
    from fox import Fox
    from  rabbit import Rabbit
    gd = GridDisplay((100,50), nb_pixels_by_box = 10 ,bg_color=(0,250,0) ,period_duration = 10)
    grass = Grassland(gd)
    # grass.populate_with_foxes(1)
    grass.populate_with_rabbits(1)
    #grass.place_new_object(  (5,5) , Rabbit( (5,5) )  )

    nb_obj = grass.get_nb_objects()
    grass.draw_objects()
    text = ", ".join(f"{name}: {nb_obj[name]}" for name in sorted(nb_obj.keys()))
    while gd.next_period(text=", " + text ) and gd.period < 50000 :
        grass.act_objects()
        nb_objects = grass.get_nb_objects()
        #si plus de fox on en remet un
        # if 'Fox' not in nb_objects.keys():
        #     grass.populate_with_foxes(1)
        #     nb_objects['Fox'] = 1
        if 'Rabbit' not in nb_objects.keys():
            grass.populate_with_rabbits(1)
            nb_objects['Rabbit'] = 1
        grass.draw_objects()
        text = ", ".join(f"{name}: {value}" for name, value in nb_objects.items())


    # for i in range(9,12):
    #         for j in range(9,12):
    #             grass.place_new_object((i,j),Fox((i,j)))
    #             grass.draw_objects()
    # grass.objects[(10,10)].act(grass)
    # while gd.next_period(text=", ") and gd.period < 5000 :
    #     grass.draw_objects()
        




