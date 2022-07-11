#! /usr/bin/python
import sys
import numpy as np
#np.__version__


def main():
    c,A,b, var_num = read_file()
    
    B = [] #initial B = all constrains
    N = [] #initial N = all vars
    for i in range(var_num + len(b)):
        if(i < var_num):
            N.append(i)
        else:
            B.append(i)
    # print (A)
    # print (b)
    # print (c)
    # print(B)
    # print(N)
    dual_simplex(A,b,c, B, N)
    
def read_file():
    var_num = 0
    objective_list = []
    constrain_function_list = []
    constrain_value_list = []
    f = open(sys.argv[1],"r")
    for line in f:
        l = line.split()
        if var_num == 0:
            var_num = len(l)
            for item in l:
                objective_list.append(float(item))
        else:
            new_array = []
            for n in range(var_num + 1):
                if n < var_num:
                    new_array.append(float(l[n]))
                else:
                    constrain_value_list.append(float(l[n]))
            constrain_function_list.append(new_array)
    constrain_value = np.array(constrain_value_list)
    
    b = np.transpose([constrain_value])
    for i in range(len(constrain_value)):
        objective_list.append((0))
    c = np.array(objective_list)

    for n in range(len(b)):
        for i in range(len(b)):
            if(n == i):
                constrain_function_list[n].append(1.0)
            else:
                constrain_function_list[n].append(0.0)
            
    A = np.array(constrain_function_list)
    f.close()
    return c, A, b, var_num
    
def dual_simplex(A, b, c , B, N):
    ZB = 0 
    AB = get_matrix_A(A,B)
    AB_inverse = np.linalg.inv(AB) 
    AN = get_matrix_A(A,N)
    cB = get_matrix_C(c,B)
    cN = get_matrix_C(c,N)
    ZN = np.subtract(np.matmul(np.transpose(np.matmul(AB_inverse, AN)), cB), cN)
    #ZN = np.subtract(np.dot(np.matmul(AB_inverse,AN),cB),cN)
    print(ZN)
    return 0

def get_matrix_C(c, vector):
    c_x = []
    new_list = []
    for item in vector:
        new_list.append(c[item])
    c_x = np.transpose((new_list))
    return c_x

def get_matrix_A(A, vector):
    A_x = []
    for item in vector:
        new_list = []
        for list in A:
            new_list.append(list[item])
        A_x.append(new_list)
    A_x = np.transpose(A_x)
    return A_x

if __name__ == "__main__":
    main()