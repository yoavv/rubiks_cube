import rub,copy
class a:
    _map = {}
    pairs=[5,3,4,1,2,0]
    minScore=0;
    nextI=0;
    nextJ=0;
    maxDepth=0;
    minDepth=0;
#    def __init__(self):

        
        
    def perpendicular(self,num1,num2):
        if(self.pairs[num1] != num2):
            return False
        return True

    def arrToStr(self,arr):
        l=arr.flatten()
        return ''.join(map(str, l))
            
    def algo1(self,arr):
        key=self.arrToStr(arr)
        score=self._map.get(key)
        
        if(score == None):
            score=self.hueristics1(arr)
            self._map[key]=score;

        return score
                            
    def algo2(self,arr):

        return self.hueristics2(arr)

                  
    def hueristics1(self,arr):
        score=0
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    if((arr[i][j][k])!= arr[i][1][1]):
                        score=score+1
        return score
    
    def hueristics2(self,arr):
        score=0
        for i in range(0,6):
            for j in range(3):
                for k in range(3):
                    if(arr[i][j][k] != arr[i][1][1]):
                        if(self.perpendicular(arr[i][1][1], arr[i][j][k])):
                            score=score+2
                        else:
                            score=score+1
        return score
    
    def hueristics3(self,arr):
        score1=0
        score2=0;
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    if(arr[i][j][k] != arr[i][1][1]):
                        if(i ==1 & j ==1):
                            continue
                        
                        if(i == 1 | j == 1):
                            if(self.perpendicular(arr[i][1][1], arr[i][j][k])):
                                score1=score1+2
                            else:
                                score1=score1+1
                                
                        else:
                            if(self.perpendicular(arr[i][1][1], arr[i][j][k])):
                                score2=score2+2
                            else:
                                score2=score2+1                            
                        
        return max(score1/8,score2/8)
    
    def solve(self,arr,depth,minI,minJ):
            cube=copy.copy(arr)
            if(depth==0):
                return [self.algo1(cube),0,0]
            
            else:
                for i in range(0, 6 ,2):
                    for j in range(0, 3 ):
                        score,movement,row=self.solve(rub.move(cube,i,j),depth-1,minI,minJ)
                        if (score<self.minScore):
                            self.minScore=score
                            minI=i
                            minJ=j
     
                return[self.minScore,minI,minJ]

    def solve2(self,arr,depth,orgI,orgJ):
        

        if (depth==0):
            
            score=self.algo2(arr)
            if(score < self.minScore):
               self.minScore = score
               self.nextI=orgI
               self.nextJ=orgJ
               
               
        else:
            cube=copy.copy(arr)
            for i in range(0, 6 ):
                for j in range(0, 3,2 ):
                    if(depth == self.maxDepth):
                        self.solve2(rub.move(cube,i,j),depth-1,i,j)
                    else:
                        self.solve2(rub.move(cube,i,j),depth-1,orgI,orgJ)

                            
    def solve3(self,arr,depth,orgI,orgJ):

        if (depth==0 ):
            return
        else:             
            if(depth == self.maxDepth):
                for i in range(0, 6 ):
                    for j in range(0, 3 ):
                        cube=copy.copy(arr)
                        self.solve3(rub.move(cube,i,j),depth-1,i,j)
                        self.getMin(cube,depth,i,j)
            else:
                for i in range(0, 6 ):
                    for j in range(0, 3 ):
                        cube=copy.copy(arr)
                        self.solve3(rub.move(cube,i,j),depth-1,orgI,orgJ)
                        self.getMin(cube,depth,orgI,orgJ)



    def getMin(self,cube,depth,orgI,orgJ):
        score=self.algo1(cube)
        if(score < self.minScore or (score == self.minScore and self.minDepth < depth)):
           self.minScore = score
           self.minDepth = depth
           self.nextI=orgI
           self.nextJ=orgJ
            
        
        

    
    def hint(self,arr,depth):
        self.minScore=1000
        self.maxDepth = depth
        self.solve3(arr,depth,0,0)
        print(" ")
        print(self.minScore)
        v=[]
        v.append(self.nextI)
        v.append(self.nextJ)
        return v
      
        


