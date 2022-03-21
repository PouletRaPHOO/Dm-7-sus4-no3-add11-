import math
import random

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
    __slots__ = ['x', 'y']

#Create pseudorandom direction vector
def randomGradient(ix, iy) -> vector2:
    # No precomputed gradients mean this works for any number of grid coordinates
    w = 8 * sizeof(unsigned);
    s = w / 2; # rotation width
    a = ix
    b = iy
    a *= 3284157443
    b ^= a << s | a >> w-s
    b *= 1911520717
    a ^= b << s | b >> w-s
    a *= 2048419325
    ran = a * (3.14159265 / ~ ( ~ 0 >> 1)) # in [0, 2*Pi]
    v =vector2()
    v.x = math.cos(ran)
    v.y = math.sin(ran)
    return v;


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
    x0 = math.floor(x)
    x1 = x0 + 1
    y0 = math.floor(y)
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

class Case(Pos) :
    def __init__(self,x,y) :
        super().__init__(x,y)
        self.visible = False
        self.isBomb = False
        self.neighbours = -1


class Grille :
    def __init__(self,width:int,height:int) :
        self.grid = [[Case(k,i)for k in range(width)]for i in range(height)]
        self.height = height
        self.width = width

    def peuplade(self,click:Pos,b_num:int) :
        l = []
        for ligne in self.grid :
            for j in ligne :
                ran = int(abs(j.y-click.y)>2 or abs(j.x-click.x)>2)*random.randint(0,50)*perlin(j.x,j.y)
                i = 0
                while i<len(l) and ran<l[i]:
                    pass # Inserer le nombre dans la liste flemme un peu la
        for k in l[0:b_num] :
            self.grid[k[1][1]][k[1][0]].isBomb = True
            #self.grid[k[1][1]][k[1][0]] += 1 Si on stocke la case sous la forme d'un int
    
    def discover(self,click:Pos) :
        case = self.grid[click.y][click.x]
        if case.neighbours > 0 :
            case.visible = True
            # case += 2
        else :
            x = click.x
            y = click.y
            for k in range(1,9) : #Regarder les cases autour
                discover

    def calculate(case:Pos):
        






        