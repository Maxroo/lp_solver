#! /usr/bin/python
import sys
import numpy as np
#np.__version__


def main():
    objective_function,constrain_f,constrain, var_num = read_file()
    objective_value = 0
    # print (objective_function)
    # print (constrain_f)
    # print (constrain)
    entering, leaving, increase = bland_rule(objective_function, constrain_f, constrain)
    objective_value = objective_function[entering]* increase
    constrain[leaving] = increase
    constrain_f[leaving][entering] = 1/constrain_f[leaving][entering]
    for n in range(len(constrain_f[leaving])):
        if (n != entering):
            constrain_f[leaving][n] = constrain_f[leaving][n]*constrain_f[leaving][entering]
        
    for i in range(len(constrain_f)):
        original_value = constrain_f[i][entering]
        if(i != leaving):
            constrain[i] = constrain[i] - constrain_f[i][leaving] * constrain[leaving]
        for n in range(len(constrain_f[i])):
            if(i != leaving):
                if(n == entering):
                    constrain_f[i][n] = original_value * -constrain_f[leaving][entering]
                else:
                    constrain_f[i][n] = original_value* constrain_f[leaving][n] + constrain_f[i][n]

    original_value =  objective_function[entering]
    for i in range(len(objective_function)):
        if i == entering:
            objective_function[i] = -constrain_f[leaving][i] * objective_function[i]
        else:
            objective_function[i] = - original_value * constrain_f[leaving][i] + objective_function[i]
            
    # print (objective_function)

    
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

    f.close()
    return objective_list, constrain_function_list, constrain_value, var_num

def bland_rule(objective_function, constrain_f, constrain):
    lowest_number = 999.0
    entering = -1
    leaving = -1
    for i in range(len(objective_function)):
        if objective_function[i] > 0:
            entering = i
            for n in range(len(constrain_f)):
                if constrain_f[n][i] > 0:
                    if lowest_number > (constrain[n]/constrain_f[n][i]):
                        lowest_number = constrain[n]/constrain_f[n][i]
                        leaving = n
        if lowest_number >= 0:
            break
    return entering, leaving, lowest_number
    
if __name__ == "__main__":
    main()