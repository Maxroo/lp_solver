#! /usr/bin/python
import sys
import numpy as np
import fileinput
 
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
    #dual_simplex(A,b,c, B, N)
    primal_simplex(A,b,c, B, N)
    
def read_file():
    var_num = 0
    objective_list = []
    constrain_function_list = []
    constrain_value_list = []
    for f in fileinput.input():
        l = f.split()
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

def primal_simplex(A, b, c , B, N):
    #compute inital value of X
    AB = get_matrix_A(A,B)
    XB = np.matmul(np.linalg.inv(AB), b)
    # print(XB)
    XN = 0
    is_negative = True
    for i in range(len(XB)):
        if XB[i] >= 0:
            is_negative = False
    if is_negative:
        print("Infeasible")
        return "Infeasible"
    while True:
        #compute z and check for optimality 
        ZB = 0
        AB = get_matrix_A(A,B)
        AB_inverse = np.linalg.inv(AB) 
        AN = get_matrix_A(A,N)
        # cB = get_matrix_C(c,B)
        # cN = get_matrix_C(c,N)
        cB = c[B]
        cN = c[N]
        ZN = np.subtract(np.matmul(np.transpose(np.matmul(AB_inverse, AN)), cB), cN)
        is_optimal = True
        for item in ZN:
            if item < 0:
                is_optimal = False
        if is_optimal:
            optimal_value = np.multiply(np.multiply(np.transpose(cB),AB_inverse),b)
            return optimal_value
        #choose entering variable
        # print(N)
        # print(B)
        # print(cN)
        enter_j = 0
        largest_coefficient = 0
        for item in N:
            if c[item] > 0:
                if largest_coefficient < c[item]:
                    largest_coefficient = c[item]
                    enter_j = item
                break
        # print(enter_j)
        
        Aj = get_matrix_A(A,enter_j)
        change_XB = np.matmul(AB_inverse, Aj)
        print(Aj)
        break


def get_matrix_C(c, vector):
    c_x = []
    new_list = []
    for item in vector:
        new_list.append(c[item])
    c_x = np.transpose((new_list))
    return c_x

def get_matrix_A(A, vector):
    A_x = []
    # print(type(vector))
    if type(vector) != list:
        new_list = []
        for list_a in A:
            new_list.append(list_a[vector])
        A_x.append(new_list)
        A_x = np.transpose(A_x)
        return A_x

    for item in vector:
        new_list = []
        for list_a in A:
            new_list.append(list_a[item])
        A_x.append(new_list)
    A_x = np.transpose(A_x)
    return A_x

if __name__ == "__main__":
    main()