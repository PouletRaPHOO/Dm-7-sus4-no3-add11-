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
    
    def __str__(self):
        return f"({self.x},{self.y})"

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
        self.discovered = False

    def peuplade(self,click:Pos,b_num:int) :
        l = []
        for y in range(len(self.grid)) :
            for x in range(len(self.grid[y])) :
                perl = perlin(x,y)
                ran = (int((abs(y-click.y))>2 or abs(x-click.x)>2))*randint(0,50)#*perl
                l = [(ran+1,(-1,-1))] + l
                i = 0
                while i<len(l)-1 and ran<l[i][0]:
                    l[i] = l[i+1]
                    i+=1
                l[i-1] = (ran,(x,y))
        for k in l[:b_num] :
            self.grid[k[1][1]][k[1][0]] = self.grid[k[1][1]][k[1][0]] | 2**5 #Si on stocke la case sous la forme d'un int
    
    def discover(self,click:Pos) :
        casea = self.grid[click.y][click.x]
        neighbours = self.neighbours(click)
        number = 0
        for k in neighbours :
            number += (self.grid[k.y][k.x] >> 5) & 1
        casea >>= 4
        casea <<= 4 
        casea |= number
        casea |= 2**4
        self.grid[click.y][click.x] = casea
        if number :
            return 0
        for k in neighbours : 
            if not(self.grid[k.y][k.x] & 2**4):
                self.discover(k)
        return 0

    def click(self,case:Pos,flag:bool):
        casea = self.grid[case.y][case.x]
        if not flag :
            if casea & 2**6 :
                print("Vous avez placé un drapeau sur cette case. Drapeau retiré veuillez confirmer")
                self.grid[case.y][case.x] &= (2**6)-1
            elif casea & 2**5 :
                return 0
            elif casea & 2**4:
                print("Vous avez déja découvert cette case")
            else :
                self.discover(case)
            return 1
        else :
            if casea & 2**4 :
                print("Vous avez déja découvert cette case")
            else :
                self.grid[case.y][case.x] |= 2**6
            return 1

    def neighbours(self, case:Pos)-> list :
        L = []
        x = case.x
        y = case.y
        for y1 in range(y-1,y+2) :
            for x1 in range(x-1,x+2) :
                if not(y1==y and x1==x) and 0<=x1<self.width and 0<=y1<self.height:
                    L.append(Pos(x1,y1))
        return L
                
    def __str__(self) :
        a = "  |"
        for k in range(1,self.width+1) :
            if k<10:
                a+=str(k)+" "
            else :
                a+=str(k)
        a+="\n"
        for y in range(len(self.grid)) :
            a+= str(y+1)+(" "*(y<9))+"|"
            for x in range(len(self.grid[y])) :
                if self.discovered :
                    if self.grid[y][x] & 2**6 :
                        if self.grid[y][x] & 2**5 :
                            a+= "🏳"
                        else :
                            a+="🚩"
                    elif self.grid[y][x] & 2**5 :
                        a+= "💣"
                    elif self.grid[y][x] & 2**4:
                        a+= str(self.grid[y][x] & 15)+" "
                    else :
                        a+="■ "
                else :
                    if self.grid[y][x] & 2**6 :
                        a+= "🏁"
                    elif self.grid[y][x] & 2**4:
                        a+= str(self.grid[y][x] & 15)+" "
                    else :
                        a+="■ "
            a+="\n"
        return a

    def reset(self,height,width) :
        self.height = height
        self.width = width
        self.grid = [[0 for k in range(width)]for i in range(height)]
        self.discovered = False

    def check_discovered(self, n_b):
        number = 0
        for y in range(len(self.grid)) :
            for x in range(len(self.grid[y])) :
                number += not(self.grid[y][x] & 2**4)
                if number>n_b :
                    return False
        return True


class Game :
    def __init__(self,name) :
        self.name = name
        self.grid = Grille(0,0)
        self.loose = 0
        self.wins = 0
        self.playing = False

    def launchGame(self):
        w = int(input("Entrez la largeur de la grille :"))
        h = int(input("Entrez la hauteur de la grille :"))
        n_b = int(input("Entrez le nombre de bombes voulues :"))
        while (n_b>(h*w)/2) :
            n_b = int(input("Nombre trop élevé entrez le nouveau nombre de bombes :"))
        self.grid.reset(w,h)
        self.playing = True
        self.play(n_b)

    def check_victory(self) :
        pass

    def play(self,n_b) :
        print(self.grid)
        click = input("Entrez la case à cliquer (x y):").split()
        pos = Pos(int(click[0])-1,int(click[1])-1)
        self.grid.peuplade(pos,n_b)
        self.grid.click(pos, len(click)>2)
        print(self.grid)
        while self.playing :
            click = input("Entrez la case à cliquer (x y):").split()
            pos = Pos(int(click[0])-1,int(click[1])-1)
            if not(self.grid.click(pos, len(click)>2)) :
                self.playing = False
                self.loose +=1
                self.grid.discovered = True
                print(self.grid)
                print("Vous avez appuyé sur une bombe ! Fin de Partie !")
                print(f"{self.name} a gagné {self.wins} parties, et perdu {self.loose} parties !")
            else :
                if self.grid.check_discovered(n_b):
                    self.playing = False
                    self.wins +=1
                    self.grid.discovered = True
                    print(self.grid)
                    print("Vous avez fini la grille, vous avez gagné ! Fin de Partie !")
                    print(f"{self.name} a gagné {self.wins} parties, et perdu {self.loose} parties !")
                else :
                    print(self.grid)

        again = input("Voulez vous Rejouer ? (O/N)")
        if again == "O" :
            print("Rechargement de la partie")
            self.launchGame()
        elif again == "N" :
            return 0
        else :
            again = input("Mauvaise entrée. Voulez vous Rejouer ? (O/N)")

game = Game(input("Entrez votre nom :"))
game.launchGame()


        






        