import sys,random ,numpy as np
class a:
    arr=0;
    cube_size=0;
    def __init__(self,_cube_size ):
        self.cube_size=_cube_size;
        self.arr= ([[[z for x in range(self.cube_size)] for y in range(self.cube_size)] for z in range(6)])
        self.arr= np.array([[[z for x in range(self.cube_size)] for y in range(self.cube_size)] for z in range(6)])

        #self.arr=mixCube(self.arr);



def mixCube(arr):
        print(len(arr[0]));
        for x in range(50):
            
            row= random.randint(0,len(arr[0])-1);
            function=random.randint(0,5);
            arr= move(arr,function,row)
              
        return arr;
    
def anticlockwise(Matrix):
    
    Matrix=Matrix.transpose()
    Matrix=Matrix[::-1]
    return Matrix

def clockwise(Matrix):
    Matrix=Matrix.transpose()
    Matrix=Matrix[:,::-1]
    return Matrix
    


def moveLeft(arr,row):
        temp=np.copy(arr[1][row]);
        arr[1][row]=arr[2][row];
        arr[2][row]=arr[3][row];
        arr[3][row]=arr[4][row];
        arr[4][row]=temp;

        if(row==0):
            arr[0]=clockwise(arr[0])
        if(row==len(arr[0])-1):
            arr[5]=anticlockwise(arr[5])

        return arr;

def moveUp(arr,col):
        temp=[];
        for i in range(len(arr[0])):  
            temp.append(arr[0][i][col]);

        for i in range(len(arr[0])):          
            arr[0][i][col]=arr[1][i][col];

        for i in range(len(arr[0])):  
            arr[1][i][col]=arr[5][i][col];

        for i in range(len(arr[0])):  
            arr[5][len(arr[0])-1-i][col]= arr[3][i][len(arr[0])-1 -col];

        for i in range(len(arr[0])):  
            arr[3][len(arr[0])-1-i][len(arr[0])-1 -col]=temp[i];

        if(col==0):
            arr[4]=anticlockwise(arr[4])
        if(col==len(arr[0])-1):
            arr[2]=clockwise(arr[2])
        return arr;

    
def moveClockWise(arr,dep):
        temp=[];
        for i in range(len(arr[0])): 
            temp.append(arr[0][dep][i]);

        for i in range(len(arr[0])):  
            arr[0][dep][i]=arr[4][len(arr[0])-1-i][dep];

        for i in range(len(arr[0])):  
            arr[4][i][dep]=arr[5][len(arr[0])-1-dep][i];
                        
        for i in range(len(arr[0])):  
            arr[5][len(arr[0])-1-dep][len(arr[0])-1-i]=arr[2][i][len(arr[0])-1-dep];
        
        for i in range(len(arr[0])):  
            arr[2][i][len(arr[0])-1-dep]=temp[i];
    
        if(dep==0):
            arr[3]=anticlockwise(arr[3])
        if(dep==len(arr[0])-1):
            arr[1]=clockwise(arr[1])
        return arr;

def moveRight(arr,row):
        for i in range(3):
            arr=moveLeft(arr,row);

        return arr;
    
def moveDown(arr,col):
        for i in range(3):
            arr=moveUp(arr,col);

        return arr;
    
def moveCounterClockWise(arr,dep):
        for i in range(3):
            arr=moveClockWise(arr,dep);

        return arr;
def print_mat(arr):  
            for i in range(6): 
                for j in range(len(arr[0])):
                    for k in range(len(arr[0])):
                        
                        print(arr[i][j][k],end="");
                    print();
                print();
            print("__________________")
def move(arr,movement,i):
        m=[];
        if(movement==0):
            m=moveLeft(arr,i)
        if(movement==1):
            m=moveRight(arr,i)
        if(movement==2):
            m=moveUp(arr,i)
        if(movement==3):
            m=moveDown(arr,i);
        if(movement==4):
            m=moveClockWise(arr,i);
        if(movement==5):
            m=moveCounterClockWise(arr,i);
        return m;
        
