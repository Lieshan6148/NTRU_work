from fpylll import BKZ, GSO, LLL, IntegerMatrix  
from sage import *
import time
def main():  
    # 创建一个整数矩阵  
    A = random_matrix(ZZ, 10, 10)   
    # 设置BKZ参数  
    params = BKZ.Param(block_size=20, strategies=BKZ.DEFAULT_STRATEGY)  
  
    # 应用BKZ算法
    starttime=time.time()  
    reduced_basis = BKZ.reduction(A, params)
    endtime=time.time()
    print("fplll time=",endtime-starttime)
    starttime=time.time() 
    red=A.BKZ(block_size=20, prune=0)
    endtime=time.time()
    print("sage time=",endtime-starttime)
    # 输出结果  
    print("Reduced basis:")  
    for row in reduced_basis:  
        print(row)  
  
if __name__ == "__main__":  
    main()  