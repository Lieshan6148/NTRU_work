from unittest import result
from fpylll import IntegerMatrix, BKZ, Pruning,FPLLL
from fpylll.fplll.bkz_param import Strategy
import time
from fpylll.fplll.pruner import PruningParams
from fpylll import SVP
import copy
import random
from fpylll.algorithms.bkz2 import BKZReduction as BKZ2
import os
def write_basis(B, filename):
    filepath = os.path.join("database", filename)
    f = open(filepath, 'w')
    for t in B:
        tmp=str(t).replace(',','') +'\n'
        f.write( tmp )
    f.close()

def linear_pruning_strategy(block_size, level):
    if level > block_size - 1:
        raise ValueError
    if block_size  < 5:
        raise ValueError
    preprocessing = 3
    strategies1 = [Strategy(i) for i in range(6)]
    for b in range(6, block_size+1):
        if block_size == b:
            pr = PruningParams.LinearPruningParams(block_size, level)
            s = Strategy(b, [preprocessing], [pr])
        else:
            s = Strategy(b, [preprocessing])
        strategies1.append(s)
    param = BKZ.Param(block_size = block_size, strategies = strategies1)
    return param

def test_pruning(A,mode,block_size,q):
    # print(A)
    if(mode==1):
        # 不使用剪枝
        param = BKZ.Param(block_size, strategies=None)
        start_time = time.time()
        A_bkz=BKZ.reduction(A, param)
        end_time = time.time()
        diff=end_time-start_time
        print("using time is ",diff,"seconds")
    if(mode==2):
        # 线性剪枝
        LP = linear_pruning_strategy(block_size, 6)
        start_time = time.time()
        A_bkz=BKZ.reduction(A, LP)
        end_time = time.time()
        diff=end_time-start_time
        print("using time is ",diff,"seconds")
        # print("faster",time1-time2,"seconds than without pruning")
    if(mode==3):
        # 极值剪枝
        flags = BKZ.AUTO_ABORT|BKZ.MAX_LOOPS|BKZ.GH_BND
        param = BKZ.Param(block_size, strategies=BKZ.DEFAULT_STRATEGY,flags=flags,max_loops=2**10)
        
        filename='N='+str((A.nrows)/2)+'q='+str(q)+'_BEFORE.txt'
        # write_basis(A, filename)
        start_time = time.time()
        # A_bkz=BKZ2(A)
        A_bkz=BKZ.reduction(A, param)
        end_time = time.time()
        diff=end_time-start_time
        print("using time is ",diff,"seconds")
        # print(A)
        filename='N='+str((A.nrows)/2)+'q='+str(q)+'_RESULT.txt'
        # write_basis(A, filename)
        # result1=A[1].norm() <= 2^q
        lenth=A[0].norm()
        result1=all(A[0][i]<2 for i in range (A.ncols))
        # print( all(Bk[i].norm() < 2^24 for i in range(k)) )
        # f,g=A[0]
        # print(f,'\n',g)
        print(A[0])
        print(result1)
    # print("faster",time1-time3,"seconds than without pruning")
    # print(A_bkz2)
    return A_bkz,result1,diff

def shift_matrix(n, m):
    """
    生成一个n行m列的矩阵，每一行都是上一行的循环移位，第一行是0-100间的随机数
    :param n: 矩阵的行数
    :param m: 矩阵的列数
    :return: 生成的矩阵
    """
    # 初始化第一行为0-100间的随机数
    first_row = [random.randint(0, 15) for _ in range(m)]
    
    # 创建一个n*m的矩阵
    A = IntegerMatrix(n, m)
    
    # 填充矩阵
    for i in range(0,n):
        for j in range(m):
            A[i, j] = first_row[(i + j) % m]
    
    return A

def shift_matrix2(n, m):
    """
    生成一个n行m列的矩阵，每一行都是上一行的循环移位，第一行是0-100间的随机数
    :param n: 矩阵的行数
    :param m: 矩阵的列数
    :return: 生成的矩阵
    """
    # 初始化第一行为0-100间的随机数
    first_row = [random.randint(0, 15) for _ in range(m)]
    
    # 创建一个n*m的矩阵
    A = IntegerMatrix(n, m)
    
    # 填充矩阵
    for i in range(0,20):
        for j in range(m):
            A[i, j] = random.randint(0, 15)
    for i in range(20,40):
        for j in range(m):
            A[i, j] = random.randint(100, 255)
    
    return A
# 示例：生成一个3行4列的矩阵
def selectmode(latticeType,dimension,blksize,max):
    FPLLL.set_random_seed(time.time())
    if(latticeType==1):
        A = IntegerMatrix.random(dimension, "ntrulike",q=max)
        print("维数=",dimension,",blocksize=",blksize,",mod=",max,",格种类为:NTRU格")
    if(latticeType==2):
        A=IntegerMatrix.random(dimension, "intrel",bits=100)
        print("维数为",dimension,",blocksize=",blksize,",格种类为:一般格")
    if(latticeType==3):
        A=IntegerMatrix.random(dimension, "uniform", bits=7)
        print("维数为",dimension,",blocksize=",blksize,",格种类为:随机格")
    if(latticeType==4):
        # A= shift_matrix(dimension, dimension)
        A= shift_matrix2(dimension, dimension)
        print("维数为",dimension,",blocksize=",blksize,",格种类为:随机循环格")
    # print(A)
    # print("不使用剪枝")  
    # A1=copy.copy(A)
    # A_bkz1=test_pruning(A1,1,blksize)
    # print("线性剪枝")
    # A2=copy.copy(A)
    # A_bkz2=test_pruning(A2,2,blksize)
    print("极值剪枝") 
    A3=copy.copy(A)
    A_bkz3,output,times=test_pruning(A3,3,blksize,max)
    # print(A_bkz3[0])
    # if(A_bkz1==A_bkz2==A_bkz3):
    #     print("same reduction result")
    # else:
    #     print("different reduction result")
    # print("stortest vector is",A_bkz1[0])
    # print("stortest vector is\n",A_bkz3[0])
    # SVP.shortest_vector(A_bkz)
    # print("stortest vector is",A_bkz[0])
    # print("lenth is",A_bkz[0].norm())
    return output,times
    
if __name__=='__main__':
    latticeType=1
    dimension=80
    blksize=50
    max=128
    selectmode(latticeType,dimension,blksize,max)