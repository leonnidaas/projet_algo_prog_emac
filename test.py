
class Wall :
    """C'est ce qui définit les limites tu terrain"""

    COLOR =(111,111,111)
    def __init__ (self):
        pass

w = Wall()
k =Wall()
m = Wall()
d =Wall()
print(d.__class__ is Wall)
liste = [w,k,m,d]
print(type(Wall) in liste)

print(m.__class__)