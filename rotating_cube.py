import sys, math, pygame,rub, heuristics, numpy as np,timeit,copy
from operator import itemgetter

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
         
    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)
 
    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)
 
    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)
 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, self.z)

class Simulation:
    def __init__(self, win_width = 640, win_height = 480):
        self.angle_x = 30;
        self.angle_y = 20;
        self.angle_z = 0;
        pygame.init()

        self.screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption("Rubick's Cube")
        
        self.vertices = [
            #0
            Point3D(-1,1,-1),#0
            Point3D(1,1,-1),#1
            Point3D(1,-1,-1),#2
            Point3D(-1,-1,-1),#3
            Point3D((-1/3),1,-1),#4
            Point3D((-1/3),(1/3),-1),#5
            Point3D(-1,(1/3),-1),#6
            Point3D((1/3),1,-1),#7
            Point3D((1/3),(1/3),-1),#8
            Point3D(1,1/3,-1),#9
            Point3D((-1/3),(-1/3),-1),#10
            Point3D(-1,(-1/3),-1),#11
            Point3D((1/3),(-1/3),-1),#12
            Point3D((1),(-1/3),-1),#13
            Point3D(-1/3,-1,-1),#14
            Point3D(1/3,-1,-1),#15
            #1
            Point3D(-1,-1,1),#0
            Point3D(1,-1,1),#1
            Point3D(1,-1,-1),#2
            Point3D(-1,-1,-1),#3
            Point3D((-1/3),-1,1),#4
            Point3D((-1/3),-1,1/3),#5
            Point3D(-1,-1,1/3),#6
            Point3D((1/3),-1,1),#7
            Point3D((1/3),-1,1/3),#8
            Point3D(1,-1,1/3),#9
            Point3D((-1/3),-1,(-1/3)),#10
            Point3D(-1,-1,(-1/3)),#11
            Point3D((1/3),-1,(-1/3)),#12
            Point3D((1),-1,(-1/3)),#13
            Point3D(-1/3,-1,-1),#14
            Point3D(1/3,-1,-1),#15
            #2
            Point3D(1,1,-1),#0
            Point3D(1,1,1),#1
            Point3D(1,-1,1),#2
            Point3D(1,-1,-1),#3
            Point3D(1,1,(-1/3)),#4
            Point3D(1,(1/3),(-1/3)),#5
            Point3D(1,(1/3),-1),#6
            Point3D(1,1,(1/3)),#7
            Point3D(1,(1/3),(1/3)),#8
            Point3D(1,1/3,1),#9
            Point3D(1,(-1/3),(-1/3)),#10
            Point3D(1,(-1/3),-1),#11
            Point3D(1,(-1/3),(1/3)),#12
            Point3D((1),(-1/3),1),#13
            Point3D(1,-1,-1/3),#14
            Point3D(1,-1,1/3),#15

            #3
            Point3D(-1,1,1),#0
            Point3D(1,1,1),#1
            Point3D(1,1,-1),#2
            Point3D(-1,1,-1),#3
            Point3D((-1/3),1,1),#4
            Point3D((-1/3),1,1/3),#5
            Point3D(-1,1,1/3),#6
            Point3D((1/3),1,1),#7
            Point3D((1/3),1,1/3),#8
            Point3D(1,1,1/3),#9
            Point3D((-1/3),1,(-1/3)),#10
            Point3D(-1,1,(-1/3)),#11
            Point3D((1/3),1,(-1/3)),#12
            Point3D((1),1,(-1/3)),#13
            Point3D(-1/3,1,-1),#14
            Point3D(1/3,1,-1),#15
            #4
            Point3D(-1,1,-1),#0
            Point3D(-1,1,1),#1
            Point3D(-1,-1,1),#2
            Point3D(-1,-1,-1),#3
            Point3D(-1,1,(-1/3)),#4
            Point3D(-1,(1/3),(-1/3)),#5
            Point3D(-1,(1/3),-1),#6
            Point3D(-1,1,(1/3)),#7
            Point3D(-1,(1/3),(1/3)),#8
            Point3D(-1,1/3,1),#9
            Point3D(-1,(-1/3),(-1/3)),#10
            Point3D(-1,(-1/3),-1),#11
            Point3D(-1,(-1/3),(1/3)),#12
            Point3D(-1,(-1/3),1),#13
            Point3D(-1,-1,-1/3),#14
            Point3D(-1,-1,1/3),#15

            #5
            Point3D(-1,1,1),#0
            Point3D(1,1,1),#1
            Point3D(1,-1,1),#2
            Point3D(-1,-1,1),#3
            Point3D((-1/3),1,1),#4
            Point3D((-1/3),(1/3),1),#5
            Point3D(-1,(1/3),1),#6
            Point3D((1/3),1,1),#7
            Point3D((1/3),(1/3),1),#8
            Point3D(1,1/3,1),#9
            Point3D((-1/3),(-1/3),1),#10
            Point3D(-1,(-1/3),1),#11
            Point3D((1/3),(-1/3),1),#12
            Point3D((1),(-1/3),1),#13
            Point3D(-1/3,-1,1),#14
            Point3D(1/3,-1,1),#15

        ]

        self.faces  = [
            (0,4,5,6),(4,7,8,5),(7,1,9,8),(6,5,10,11),(5,8,12,10),(8,9,13,12),(11,10,14,3),(10,12,15,14),(12,13,2,15),
            
            (27,26,30,19),(26,28,31,30),(28,29,18,31),(22,21,26,27),(21,24,28,26),(24,25,29,28),(16,20,21,22),(20,23,24,21),(23,17,25,24),
            
            (43,42,46,35),(38,37,42,43),(32,36,37,38),(42,44,47,46),(37,40,44,42),(36,39,40,37),(44,45,34,47),(40,41,45,44),(39,33,41,40),
            
            (60,61,50,63),(58,60,63,62),(59,58,62,51),(56,57,61,60),(53,56,60,58),(54,53,58,59),(55,49,57,56),(52,55,56,53),(48,52,53,54),
            
            (64,68,69,70),(70,69,74,75),(75,74,78,67),(68,71,72,69),(69,72,76,74),(74,76,79,78),(71,65,73,72),(72,73,77,76),(76,77,66,79),
            
            (91,90,94,83),(90,92,95,94),(92,93,82,95),(86,85,90,91),(85,88,92,90),(88,89,93,92),(80,84,85,86),(84,87,88,85),(87,81,89,88),
            ]
        
    def getColors(self,num):
        if(num==0):
            return (255,255,255)
        if(num==1):
            return (255,0,0)
        if(num==2):
            return (0,255,0)
        if(num==3):
            return (0,0,255)
        if(num==4):
            return (255,255,0)
        if(num==5):
            return (128,9,219)
        
        return (0,0,0)

    def listen(self,cube,h):
        gameLoop=True;
        move_angle=15;
        while gameLoop:

            for event in pygame.event.get():
         
                if (event.type==pygame.QUIT):
                    pygame.quit();
                    sys.exit();
                    gameLoop=False
         
                if (event.type==pygame.KEYDOWN):
         
                    if (event.key==pygame.K_LEFT):
                        x=self.angle_x;
                        while (self.angle_x<x+move_angle):
                            self.move(0.01,0,0);

                        gameLoop=False;
         
                    if (event.key==pygame.K_RIGHT):
                        x=self.angle_x;
                        while (self.angle_x>x-move_angle):
                            self.move(-0.01,0,0);

                        gameLoop=False;
                        
         
                    if (event.key==pygame.K_UP):
         
                        y=self.angle_y;
                        while (self.angle_y<y+move_angle):
                            self.move(0,0.01,0);

                        gameLoop=False;
         
                    if (event.key==pygame.K_DOWN):
                         
                        y=self.angle_y;
                        while (self.angle_y>y-move_angle):
                            self.move(0,-0.01,0);

                        gameLoop=False;
                        
                    if (event.key==pygame.K_q):
                        cube.arr=rub.move(cube.arr,0,0);
                        gameLoop=False;
                    if (event.key==pygame.K_a):
                        cube.arr=rub.move(cube.arr,0,2);
                        gameLoop=False;                        
                    if (event.key==pygame.K_w):
                        cube.arr=rub.move(cube.arr,2,0);
                        gameLoop=False;
                    if (event.key==pygame.K_s):
                        cube.arr=rub.move(cube.arr,2,2);
                        gameLoop=False;
                    if (event.key==pygame.K_e):
                        cube.arr=rub.move(cube.arr,4,0);
                        gameLoop=False;
                    if (event.key==pygame.K_d):
                        cube.arr=rub.move(cube.arr,4,2);
                        gameLoop=False;
                    if (event.key==pygame.K_h):
                        arr_copy=copy.copy(cube.arr);
                        start = timeit.timeit()
                        huer=h.hint(arr_copy,3);
                        end = timeit.timeit()
                        print (end - start)
                        cube.arr=rub.move(cube.arr,int(huer[0]),huer[1]);
                        gameLoop=False;
                        

    def setColors(self,cube):
        arr=[]
        index=0;
        for i in range(6):
            for j in range(cube.cube_size):
                for k in range(cube.cube_size):
                    arr.append(self.getColors(cube.arr[i][j][k]));
                    index=index+1;


        self.colors=arr;
    def move(self,_x,_y,_z):

        #calc  
        t = []
        for v in self.vertices: 
            self.angle_x +=_x;
            self.angle_y +=_y;
            self.angle_z +=_z;
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            r = v.rotateX(self.angle_x).rotateY(self.angle_y).rotateZ(self.angle_z)
            # Transform the point from 3D to 2D
            p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
            # Put the point in the list of transformed vertices
            t.append(p)

        #draw    
        avg_z = []
        i = 0
        for f in self.faces:
            z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
            avg_z.append([i,z])
            i = i + 1
        for tmp in sorted(avg_z,key=itemgetter(1),reverse=True):
            face_index = tmp[0]
            f = self.faces[face_index]
            pointlist = [(t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),
            (t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y),
            (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y),
            (t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y)]
            pygame.draw.polygon(self.screen,self.colors[face_index],pointlist)

        pygame.display.flip();
        
    def run(self):
        cube=rub.a(3);
        
        h=heuristics.a()
        while 1:
            
            self.screen.fill((120,120,120))            
            self.setColors(cube);
            self.move(0,0,0);
            self.listen(cube,h);

if __name__ == "__main__":
    

    
    Simulation().run();
    

