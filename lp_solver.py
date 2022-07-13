#! /usr/bin/python
import numpy as np
import fileinput
 
#np.__version__


def main():
    print("-------------------------------------------------------------------------------------------")
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
    
def primal_simplex(A, b, c , B, N):
    #compute inital value of X
    # print(c)
    AB = get_matrix_A(A,B)
    #calculate X
    XB = np.matmul(np.linalg.inv(AB), b)
    X = []
    XB_count = 0
    for i in range(len(B) + len(N)):
        if i in N:
            X.append(0.0)
        if i in B:
            X.append(XB[XB_count][0])
            XB_count += 1
    X = np.transpose(X)[np.newaxis]
    X = X.T
    
    #check if initial feasible
    is_negative = True
    for i in range(len(XB)):
        if XB[i] >= 0:
            is_negative = False
    if is_negative:
        print("Infeasible")
        return "Infeasible"
    # print(c)
    # print(A)
    pivot_count = 0
    while True:
        #compute z and check for optimality 
        ZB = 0
        AB = get_matrix_A(A,B)
        # print(B)
        # print(AB)
        AB_inverse = np.linalg.inv(AB) 
        AN = get_matrix_A(A,N)
        # cB = get_matrix_C(c,B)
        # cN = get_matrix_C(c,N)
        # print(AB)
        cB = c[B]
        cN = c[N]
        # print(cN)
        ZN = np.subtract(np.matmul(np.transpose(np.matmul(AB_inverse, AN)), cB), cN)
        ZN_count = 0
        Z = []
        for n in range(len(N)+ len(B)):
            if n in N:
                Z.append(ZN[ZN_count])
                ZN_count += 1
            if n in B:
                Z.append(0)
        # print(ZN)
        is_optimal = True
        for item in ZN:
            if item < 0:
                is_optimal = False
        if is_optimal:
            # optimal_value = np.dot(cB,np.multiply((AB_inverse),b))
            optimal_value = np.matmul(np.transpose(cB),np.matmul((AB_inverse),b))
            # print(Z)
            # print("B = ", end=" ")
            # print(B)
            # print("cB = ", end=" ")
            # print(cB)
            # print("AB = ")
            # print(AB)
            # print("b = ")
            # print(b)
            print("optimal")
            print(optimal_value)
            for item in ZN:
                print(item, end="     ")
            print()
            return optimal_value
        #choose entering variable
        # print(N)
        # print(B)
        # print(cN)
        enter_j = 0
        # print(N)
        for i in range(len(ZN)):
            if ZN[i] < 0:
                enter_j = N[i]
                break
        # print(enter_j)
        #choose leaving variable
        # print(AB)
        Aj = get_matrix_A(A,enter_j)
       
                
        # print(Aj)
        # print("")
        # print(AB)
        # print("")
        # print(AB_inverse)
        # print("")
        delta_XB = np.matmul(AB_inverse, Aj)
        # print(delta_XB)
        delta_Xn = 0

                
        is_unbounded = True
        for item in delta_XB:
            if item > 0:
                is_unbounded = False
        if is_unbounded:
            print("unbounded")
            return "unbounded"
        # print(XB)
        t = 0
        count_leaving_var = 0
        leave_i = 0
        #choose leaving variable
        # print(XB)
        # print(delta_XB)
        for n in range(len(X[B])):
            if(delta_XB[n] > 0):
              temp_t = X[B][n]/delta_XB[n]
            #   print(delta_XB[n])
            #   print(n)
              if count_leaving_var == 0:
                t = temp_t
                i = n
                leave_i = B[n]
                count_leaving_var += 1
              else:
                  if t > temp_t:
                    t = temp_t
                    i = n
                    leave_i = B[n]
            
        # print("leave i: ")
        # print(leave_i)
        if count_leaving_var == 0:
            print("error: no leaving variable")
            return 0
        # print(XB) 
        print(enter_j, end="")
        print(" Entering ",end="")  
        print(leave_i, end="")
        print(" Leaving ")  
        X[B] = np.subtract(X[B], t* delta_XB)
        # X[B][i][0] = t
        # print(X[B])
        print(t)
        # print(leave_i)
        # print(X.T[0][leave_i])
        temp_x = X.T
        temp_x[0][enter_j] = t
        # print("B = ", end="")
        # print(B)
        print(temp_x.T[B])
        X = temp_x.T
        print("X = ")
        print(X)
        # temp_x = X[B]
        # temp_x[i][0] = t
        # # print(temp_x)
        # X[B] = temp_x
        # print(i)
        # print(t)
        # print(leave_i)
        
        # B[B.index(leave_i)] = enter_j
        # B = list(map(lambda x: x.replace(leave_i, enter_j), B))
        # print("B = ", end="")
        # print(B)
        B.append(enter_j)
        B.remove(leave_i)
        B.sort()
        pivot_count += 1
        N.append(leave_i)
        N.remove(enter_j)
        N.sort()
        # N[N.index(enter_j)] = leave_i
        # print("N = ", end="")
        # print(N)
        # print("Pivot Count: ", end="")
        # print(pivot_count)
        
        # if pivot_count > 2:
        #     break
            
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