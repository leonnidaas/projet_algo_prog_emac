
class Wall :
    """C'est ce qui définit les limites tu terrain"""
    def __init__ (self):
        pass

w = Wall()
k =Wall()
m = Wall()
d =Wall()

liste = [w,k,m,d]
print(type(Wall) in liste)
if Wall in liste:
    print(True)

print(w.__class__)


n = None 

print (type(n).__name__)
print(n)