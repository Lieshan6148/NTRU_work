from fpylll import IntegerMatrix, BKZ, Pruning,FPLLL
from fpylll.fplll.bkz_param import Strategy
import time
from fpylll import SVP
def test_linear_pruning():
    FPLLL.set_random_seed(time.time())
    A = IntegerMatrix.random(40, "ntrulike",q=127)
    # print(A)
    block_size  = 20
    start_time = time.time()
    A_bkz1 = BKZ.reduction(A, BKZ.Param(block_size))
    end_time = time.time()
    # print(A_bkz1)
    time1=end_time-start_time
    print("without pruning using time is ",time1)
    preprocessing = 3
    strategies = [Strategy(i) for i in range(5)]
    for b in range(5, block_size+1):
        strategies.append(Strategy(b, [preprocessing], [Pruning.LinearPruningParams(b, 2)]))
    param = BKZ.Param(block_size=block_size, strategies=strategies)
    start_time = time.time()
    A_bkz2=BKZ.reduction(A, param)
    end_time = time.time()
    time2=end_time-start_time
    print("with Linear pruning using time is ",time2)
    # print("faster",time1-time2,"seconds than without pruning")
    param = BKZ.Param(block_size=block_size, strategies=BKZ.DEFAULT_STRATEGY)
    start_time = time.time()
    A_bkz3=BKZ.reduction(A, param)
    end_time = time.time()
    time3=end_time-start_time
    print("with DEFAULT pruning using time is ",time3)
    # print("faster",time1-time3,"seconds than without pruning")
    # print(A_bkz2)
    if(A_bkz1==A_bkz2):
        if(A_bkz2==A_bkz3):
            print("same reduction result")
    else:
        print("different reduction result")
    print("stortest vector is",A_bkz1[0])
    return A_bkz1  

if __name__ == "__main__":  
    A_bkz=test_linear_pruning()
    # SVP.shortest_vector(A_bkz)
    # print("stortest vector is",A_bkz[0])
    # print("lenth is",A_bkz[0].norm())