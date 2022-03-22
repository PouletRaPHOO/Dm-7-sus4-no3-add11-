from math import cos,sin,floor
from random import randint,uniform
seed = uniform(-65536, 65535)

# Function to linearly interpolate between a0 and a1
# Weight w should be in the range [0.0, 1.0]
def interpolate(a0, a1, w) :
    #You may want clamping by inserting: if (0.0 > w) return a0; 
    # if (1.0 < w) return a1;
    #Use this cubic interpolation [[Smoothstep]] instead, for a smooth appearance:
    # return (a1 - a0) * (3.0 - w * 2.0) * w * w + a0;
    
    # // Use [[Smootherstep]] for an even smoother result with a second derivative equal to zero on boundaries:
    # return (a1 - a0) * ((w * (w * 6.0 - 15.0) + 10.0) * w * w * w) + a0;
    return (a1 - a0) * w + a0
    
class vector2(object):
    def __init__(self,x,y) :
        self.x =x
        self.y =y

#Create pseudorandom direction vector
def randomGradient(ix, iy) -> vector2:
    # No precomputed gradients mean this works for any number of grid coordinates
    random = 2920.0 * sin(ix * 21942.0 + iy * 171324.0 + 8912.0 + seed) * cos(ix * 23157.0 * seed * iy * 217832.0 + 9758.0)
    return vector2(cos(random), sin(random))


# Computes the dot product of the distance and gradient vectors.
def dotGridGradient(ix, iy, x, y) -> float:
    #Get gradient from integer coordinates
    gradient = randomGradient(ix, iy);

    # Compute the distance vector
    dx = x - float(ix);
    dy = y - float(iy);

    # Compute the dot-product
    return (dx*gradient.x + dy*gradient.y);


#Compute Perlin noise at coordinates x, y
def perlin(x, y) -> float:
    # Determine grid cell coordinates
    x0 = floor(x)
    x1 = x0 + 1
    y0 = floor(y)
    y1 = y0 + 1

    # Determine interpolation weights
    # Could also use higher order polynomial/s-curve here
    sx = x - float(x0)
    sy = y - float(y0)

    # Interpolate between grid point gradients

    n0 = dotGridGradient(x0, y0, x, y)
    n1 = dotGridGradient(x1, y0, x, y)
    ix0 = interpolate(n0, n1, sx)

    n0 = dotGridGradient(x0, y1, x, y)
    n1 = dotGridGradient(x1, y1, x, y)
    ix1 = interpolate(n0, n1, sx)

    value = interpolate(ix0, ix1, sy)
    return value

class Pos :
    def __init__(self,x,y) :
        self.x = x
        self.y = y

#class Case(Pos) : # Classe Cas non utilisée puisque qu'on le stocke sous un Int 
    #def __init__(self,x,y) :
    #super().__init__(x,y)
    #self.visible = False
    #self.isBomb = False
    #self.neighbours = -1


class Grille :
    def __init__(self,width:int,height:int) :
        self.grid = [[0 for k in range(width)]for i in range(height)]
        self.height = height
        self.width = width

    def peuplade(self,click:Pos,b_num:int) :
        l = []
        for y in range(len(self.grid)) :
            for x in range(len(self.grid[y])) :
                perl = perlin(x,y)
                ran = (int((abs(y-click.y))>2 or abs(x-click.x)>2))*randint(0,50)#*perl
                l = [(ran+1,(-1,-1))] + l
                i = 0
                # print((x,y), end="")
                # print(i<len(l)-1, end="")
                while i<len(l)-1 and ran<l[i][0]:
                    #print("i ="+str(i))
                    l[i] = l[i+1]
                    i+=1
                l[i-1] = (ran,(x,y))
        #print(l)
        for k in l[:b_num] :
            #self.grid[k[1][1]][k[1][0]].isBomb = True
            self.grid[k[1][1]][k[1][0]] = self.grid[k[1][1]][k[1][0]] | 2**5 #Si on stocke la case sous la forme d'un int
    
    def discover(self,click:Pos) :
        casea = self.grid[click.y][click.x]
        neighbours = self.neighbours(click) 
        number = 0
        for k in neighbours :
            number += self.grid[k.y][k.x] & 2**5
        self.grid[click.y][click.x] = casea | number
        self.grid[click.y][click.x] = casea | 2**4
        if number :
            return 0
        for k in neighbours : 
            if not(self.grid[k.y][k.x]%2**4):
                self.discover(Pos(k.x,k.y))
        return 0

    def click(case:Pos):
        casea = grid[case.y][case.x]
        if casea & 2**5 :
            pass # TODO : C'est une bombe casser le jeu
        else :
            self.discover(case)

    def neighbours(self, case:Pos)-> list : #TODO : Trouver les voisins 
        L = []
        x = case.x
        y = case.y
        for i in range(1,4) :
            for k in range(1,i+1):
                x+=1 * int((int(not(i%2==0))-0.5) * 2)
                if 0<x<self.width and 0<y<self.height :
                    L.append(Pos(x,y))
            for l in range(1,i+1):
                y+= 1 * int((int(i%2==0)-0.5) * 2)
                if 0<x<self.width and 0<y<self.height :
                    L.append(Pos(x,y))
        return L
                

    def __str__(self) :
        a = ""
        for x in range(len(self.grid)) :
            for y in range(len(self.grid[x])) :
                print((x,y))
                if self.grid[x][y] & 2**5 :
                    a+="b "
                elif self.grid[x][y] & 2**4:
                    a+= str(self.grid[x][y] & 15)+" "
                else :
                    self.discover(Pos(x,y))  # A retirer si on veut pas se faire spoil la grid c'est uniquement pour le debug
                    a+= str(self.grid[x][y] & 15)+" "
                    #a+="* "
            a+="\n"
        return a

grid = Grille(5,5)
grid.peuplade(Pos(5,5),5)
print(grid)


        






        