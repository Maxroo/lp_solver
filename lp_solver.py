#! /usr/bin/python
import sys
from tkinter.messagebox import YES
import numpy as np
import fileinput
 
#np.__version__

tolerance_var = 7e-3

def main():
    """
    A = constrain function, b = constrains, c = objective function, var_num = the number of basic variables
    """
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
    Return Value:   -2 Infeasible
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
    AB = get_matrix_A(A,B)
    #calculate Xb and X
    #revised method
    XB = np.linalg.solve(AB,b)
    for item in (XB):
        if (item[0] >= -tolerance_var and  item[0] <= tolerance_var):
            item[0] = 0
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
            is_dual_feasible = True
            for item in c:
                if item > 0:
                    is_dual_feasible = False
            if is_dual_feasible:
                return dual_simplex(A, b, c , B, N, var_num, is_dual_feasible)
            zero_c = []
            for n in range(len(c)):
                if n in N:
                    zero_c.append(-1)
                else:
                    zero_c.append(0)
            zero_c = np.array(zero_c)

            return dual_simplex(A, b, zero_c , B, N, var_num, is_dual_feasible)

    #counter for pivoting
    pivot_count = 0
    
    #pivot steps until return one states.
    while True:
        #compute z and check for optimality 
        ZB = 0
        AB = get_matrix_A(A,B)

        AN = get_matrix_A(A,N)
 
        cB = c[B]
        cN = c[N]

        v = np.linalg.solve(np.transpose(AB), cB)
        ZN = np.subtract(np.matmul(np.transpose(AN), v), cN)
        for i in range(len(ZN)):
            if ( ZN[i] >= -tolerance_var and  ZN[i] <= tolerance_var):
                 ZN[i] = 0
        ZN_count = 0
        Z = []
        for n in range(len(N)+ len(B)):
            if n in N:
                Z.append(ZN[ZN_count])
                ZN_count += 1
            if n in B:
                Z.append(0)
        Z = np.array(Z)
        is_optimal = True
        for item in ZN:
            if item < 0:
                is_optimal = False
        if is_optimal:
            v = np.linalg.solve(AB,b)
            optimal_value = np.matmul(np.transpose(cB), v)
            sys.stdout.write("optimal\n")
            for item in optimal_value: sys.stdout.write("%g\n"% item)
            for i in range(var_num):
                sys.stdout.write("%g " % (X[i][0]))
            sys.stdout.write("\n")
            return 0, B, N

        enter_j = 0

        for i in range(len(Z[N])):
            if Z[N][i] < 0:
                enter_j = N[i]
                break
        #choose leaving variable
        Aj = get_matrix_A(A,enter_j)
        delta_XB = np.linalg.solve(AB, Aj)
        for i in range(len(delta_XB)):
            if ( delta_XB[i] >= -tolerance_var and  delta_XB[i] <= tolerance_var):
                delta_XB[i] = 0
        
        is_unbounded = True
        for item in delta_XB:
            if item > 0:
                is_unbounded = False
        if is_unbounded:
            sys.stdout.write("unbounded\n")
            return -1, B, N
        t = 0
        count_leaving_var = 0
        leave_i = 0
        #choose leaving variable

        for n in range(len(X[B])):
            if(delta_XB[n] > 0):
              temp_t = X[B][n]/delta_XB[n]

              if count_leaving_var == 0:
                t = temp_t
                leave_i = B[n]
                count_leaving_var += 1
              else:
                  if t > temp_t:
                    t = temp_t
                    leave_i = B[n]
                    
        X[B] = np.subtract(X[B], t* delta_XB)
        temp_x = X.T
        temp_x[0][enter_j] = t
        for i in range(len(temp_x[0])):
            if ( temp_x[0][i] >= -tolerance_var and  temp_x[0][i] <= tolerance_var):
                temp_x[0][i] = 0

        X = temp_x.T
        B.append(enter_j)
        B.remove(leave_i)
        B.sort()
        pivot_count += 1
        N.append(leave_i)
        N.remove(enter_j)
        N.sort()
        # if(pivot_count%100 == 0):
        #     print(pivot_count) 

        
        
def dual_simplex(A, b, c, B, N, var_num, is_dual_feasible):
    #compute inital value of X
    AB = get_matrix_A(A,B)
    AN = get_matrix_A(A,N)
    #calculate Xb and X
    #revised method
    v = np.linalg.solve(np.transpose(AB), c[B])
    ZN = np.subtract(np.matmul(np.transpose(AN), v), c[N])
    for i in range(len(ZN)):
        if ( ZN[i] >= -tolerance_var and  ZN[i] <= tolerance_var):
            ZN[i] = 0
    ZN_count = 0
    Z = []
    for n in range(len(N)+ len(B)):
        if n in N:
            Z.append(ZN[ZN_count])
            ZN_count += 1
        if n in B:
            Z.append(0)
    Z = np.transpose(Z)
    #check if initial feasible
    for item in ZN:
        if item < 0:
            sys.stdout.write("infeasible")
            return -2, B, N
        
    pivot_count = 0
    while True:
        AB = get_matrix_A(A,B)
        AN = get_matrix_A(A,N)        
        XB = np.linalg.solve(AB,b)
        for item in (XB):
            if (item[0] >= -tolerance_var and  item[0] <= tolerance_var):
                item[0] = 0

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
        is_optimal = True
        for item in X[B]:
           if item < 0:
               is_optimal = False
        if is_optimal:
            if not is_dual_feasible:
                
                return 1, B, N
            v = np.linalg.solve(AB,b)
            optimal_value = np.matmul(np.transpose(c[B]), v)
            sys.stdout.write("optimal\n")
            for item in optimal_value: sys.stdout.write("%g\n" % item)
            for i in range(var_num):
                sys.stdout.write("%g " % (X[i][0]))
            sys.stdout.write("\n")
            return 0, B, N
        #choose entering variable
        enter_i = 0
        Zi = 0
        for i in range(len(X[B])):
            if X[B][i] < 0:
                Zi = i
                enter_i = B[i]
                break
        #choose leaving variable
        U = []
        U = np.zeros_like(Z[B])
        U[Zi] = 1
        v = np.linalg.solve(np.transpose(AB), U)
        delta_ZN = np.matmul(-np.transpose(AN), v)
        for i in range(len(delta_ZN)):
            if ( delta_ZN[i] >= -tolerance_var and  delta_ZN[i] <= tolerance_var):
                delta_ZN[i] = 0
        is_unbounded = True
        for item in delta_ZN:
            if item > 0:
                is_unbounded = False
        if is_unbounded:
            sys.stdout.write("infeasible\n")
            return -2, B, N
        s = 0
        count_leaving_var = 0
        leave_j = 0
        #choose leaving variable

        for n in range(len(Z[N])):
            if(delta_ZN[n] > 0):
              temp_s = Z[N][n]/delta_ZN[n]

              if count_leaving_var == 0:
                s = temp_s
                leave_j = N[n]
                count_leaving_var += 1
              else:
                  if s > temp_s:
                    s = temp_s
                    leave_j = N[n]
        
        if count_leaving_var == 0:
            sys.stdout.write("infeasible")
            return -2, B, N
        Z[N] = np.subtract(Z[N], s* delta_ZN)
        temp_zn = Z[N]
        for i in range(len(temp_zn)):
            if ( temp_zn[i] >= -tolerance_var and temp_zn[i] <= tolerance_var):
                temp_zn[i] = 0
        Z[N] = temp_zn
        Z[enter_i] = s
        pivot_count += 1
        # if(pivot_count%100 == 0):
        #     print(pivot_count) 
        B.append(leave_j)
        B.remove(enter_i)
        B.sort()
        N.append(enter_i)
        N.remove(leave_j)
        N.sort()



            
def get_matrix_A(A, vector):
    A_x = []
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