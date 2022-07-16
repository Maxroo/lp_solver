#! /usr/bin/python
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
    return_value, B_p, N_p = primal_simplex(A,b,c, B, N, var_num)
    """
    Retrun Value:   -2 LP is Infeasible
                    -1 Unbounded
                    0  Optimal 
                    1  Call primal simplex method again with B' N' after getting feasible LP from two face method
    """
    if return_value == 1:
        primal_simplex(A,b,c, B_p, N_p, var_num)
    
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
    
def primal_simplex(A, b, c , B, N, var_num):
    #compute inital value of X
    # print(c)
    AB = get_matrix_A(A,B)
    #calculate Xb and X
    #revised method
    XB = np.linalg.solve(AB,b)
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
    for i in range(len(X[B])):
        if X[B][i] < 0:
            # print("The lP is Primal Infeasible")
            # print("calling dual simplex method")
            is_dual_feasible = True
            for item in c:
                if item > 0:
                    is_dual_feasible = False
            if is_dual_feasible:
                return dual_simplex(A, b, c , B, N, var_num, is_dual_feasible)
            # print(c)
            zero_c = []
            for n in range(len(c)):
                if n in N:
                    zero_c.append(-1)
                else:
                    zero_c.append(0)
            zero_c = np.array(zero_c)
            # print(c)
            return dual_simplex(A, b, zero_c , B, N, var_num, is_dual_feasible)
    # print(X)
    # print(c)
    # print(A)
    pivot_count = 0
    while True:
        #compute z and check for optimality 
        ZB = 0
        AB = get_matrix_A(A,B)
        # print(B)
        # print(AB)
        # AB_inverse = np.linalg.inv(AB) 
        AN = get_matrix_A(A,N)
        # cB = get_matrix_C(c,B)
        # cN = get_matrix_C(c,N)
        # print(AB)
        cB = c[B]
        cN = c[N]
        # print(cB)
        # print(cN)
        # print(cN)
        #calculated ZN without inverse
        v = np.linalg.solve(np.transpose(AB), cB)
        ZN = np.subtract(np.matmul(np.transpose(AN), v), cN)
        ZN_count = 0
        Z = []
        for n in range(len(N)+ len(B)):
            if n in N:
                Z.append(ZN[ZN_count])
                ZN_count += 1
            if n in B:
                Z.append(0)
        # print(ZN)
        # print(Z)
        is_optimal = True
        # print(XB)
        for item in ZN:
            if item < 0:
                is_optimal = False
        if is_optimal:
            # optimal_value = np.dot(cB,np.multiply((AB_inverse),b))
            v = np.linalg.solve(AB,b)
            optimal_value = np.matmul(np.transpose(cB), v)
            # optimal_value = np.matmul(np.transpose(cB),np.matmul((AB_inverse),b))
            # print(Z)
            # print("B = ", end=" ")
            # print(B)
            # print("cB = ", end=" ")
            # print(cB)
            # print("AB = ")
            # print(AB)
            # print("b = ")
            # print(b)
            # print("Done", pivot_count, "pivots")
            print("optimal")
            for item in optimal_value: print(item)
            # print(optimal_value)
            for i in range(var_num):
                print(X[i][0], end=" ")
            print()
            return 0, B, N
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
        delta_XB = np.linalg.solve(AB, Aj)

        # delta_XB = np.matmul(AB_inverse, Aj)
        # print(delta_XB)

                
        is_unbounded = True
        for item in delta_XB:
            if item > 0:
                is_unbounded = False
        if is_unbounded:
            print("unbounded")
            return -1, B, N
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
        # print(XB) 
        # print(enter_j, end="")
        # print(" Entering ",end="")  
        # print(leave_i, end="")
        # print(" Leaving ")  
        X[B] = np.subtract(X[B], t* delta_XB)
        # X[B][i][0] = t
        # print(X[B])
        # print(t)
        # print(leave_i)
        # print(X.T[0][leave_i])
        temp_x = X.T
        temp_x[0][enter_j] = t
        # print("B = ", end="")
        # print(B)
        # print(temp_x.T[B])
        X = temp_x.T
        B.append(enter_j)
        B.remove(leave_i)
        B.sort()
        pivot_count += 1
        N.append(leave_i)
        N.remove(enter_j)
        N.sort()
        
        
def dual_simplex(A, b, c, B, N, var_num, is_dual_feasible):
    #compute inital value of X
    AB = get_matrix_A(A,B)
    AN = get_matrix_A(A,N)
    #calculate Xb and X
    #revised method
    v = np.linalg.solve(np.transpose(AB), c[B])
    ZN = np.subtract(np.matmul(np.transpose(AN), v), c[N])
    ZN_count = 0
    Z = []
    # print(ZN)
    for n in range(len(N)+ len(B)):
        if n in N:
            Z.append(ZN[ZN_count])
            ZN_count += 1
        if n in B:
            Z.append(0)
    Z = np.transpose(Z)
    # print(Z[B])
    #check if initial feasible
    # print(Z)
    for item in ZN:
        if item < 0:
            print("Dual infeasible")
            return -2, B, N
        
    pivot_count = 0
    while True:
        AB = get_matrix_A(A,B)
        AN = get_matrix_A(A,N)        
        XB = np.linalg.solve(AB,b)
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
        # print(X)
        is_optimal = True
        # print("XB =", X[B])
        for item in X[B]:
           if item < 0:
               is_optimal = False
        if is_optimal:
            if not is_dual_feasible:
                return 1, B, N
            v = np.linalg.solve(AB,b)
            optimal_value = np.matmul(np.transpose(c[B]), v)
            print("optimal")
            for item in optimal_value: print(item)
            # print(optimal_value)
            for i in range(var_num):
                print(X[i][0], end=" ")
            print()
            return 0, B, N
        #choose entering variable
        enter_i = 0
        # print(N)
        # print(X[B])
        Zi = 0
        for i in range(len(X[B])):
            if X[B][i] < 0:
                Zi = i
                enter_i = B[i]
                break
        #choose leaving variable
        # print(AB)
        U = []
        for k in range(len(Z[B])):
            if k == Zi:
                U.append(1)
            else:
                U.append(0)
                
        v = np.linalg.solve(np.transpose(AB), U)
        delta_ZN = np.matmul(-np.transpose(AN), v)
        
        # print(delta_ZN)
        is_unbounded = True
        for item in delta_ZN:
            if item >= 0:
                is_unbounded = False
        if is_unbounded:
            print("infeasible")
            return -3, B, N
        s = 0
        count_leaving_var = 0
        leave_j = 0
        #choose leaving variable
        # print(XB)
        for n in range(len(Z[N])):
            if(delta_ZN[n] > 0):
              temp_s = Z[N][n]/delta_ZN[n]
            #   print(temp_s)
            #   print(delta_XB[n])
            #   print(n)
              if count_leaving_var == 0:
                s = temp_s
                # i = n
                leave_j = N[n]
                count_leaving_var += 1
              else:
                  if s > temp_s:
                    s = temp_s
                    # i = n
                    leave_j = N[n]
        # print("s = ", s)
        Z[N] = np.subtract(Z[N], s* delta_ZN)
        # print("Z =", Z)
        Z[enter_i] = s
        # print("Z =", Z)
        # print(enter_i ,"entering")
        # print(leave_j ,"leaving")
        B.append(leave_j)
        B.remove(enter_i)
        B.sort()
        pivot_count += 1
        N.append(enter_i)
        N.remove(leave_j)
        N.sort()
        # print("B =", B)
        # print("N =", N)
        # print("-----------------------------------------")
        # return 0
            
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