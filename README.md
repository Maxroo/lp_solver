# lp_solver

## Description 
The file LP_solver.py contains a solver for linear programming using *Revised simplex method*. (Avoid the inverses)

## Requirements
- To get this project running on your machine, please install:
>python 3
>
>numpy
- A txt file contains LP in standard form 

## Test
Then use command with the following format to run the code:
<p>python3 lp_solver.py < file_name.txt<p>
                    or
<p>python lp_solver.py < file_name.txt<p>

## Solver architecture
This solver used Algebraic method to solve the LP under following procedure:
The solver uses *bland rule* only as pivot rule
1. read the LP in standard form.
2. convert the LP into equational form, with A = constrain function, b = constrains, c = objective function
3. init the B and N, B = basis variables, N = non-basis variables and pass them into primal simplex method.
4. to cehck if the LP is optimal, solver go through ZN(calculated using AN CN AB) check if all the objective function value is less 0
    - If it is optimal, calculate and return optimal value 
5. to check the lp is inital infeasible. It calculates XB which is the values of basis variables and if there is a negative it check if it is initally dual infeasible by check if any value in c is positive.
    - If it is inital dual feasible, the solver will pass all the variable into dual simplex method.
    - If it is not inital dual feasible, the solver init the objective function with all -1 and other remains the same and pass into the dual simplex method to create a 100% initally dual feasible dictionary, solving the dual dictionary save B and N variables, call the primal simplex method with dual optimal B and N variables.
6. if the LP is initally feasible, it gonna find a entering variable base on previous selected pivot rule. And check unboundness by checking if the basis varable under the selected pivot is less than 0. If the lp is primal unbounded, retrun unbounded If the LP is in dual simplex method, unboundedness means the lp is fully infeasible.
7. If the LP is not unbounded, the solver find the min value of by Xi/deltaXi. i will be the leaving variable.
8. perform the pivot. go to step 4 and repeat until the solver turns feasible, infeasible or unbounded.

## Revised simplex method
To avoid and replace matrix inversions:
In gerenal, the function solve under numpy.linalg is used to solve the matrix and avoid inverses
1. Under Primal Simplex Method:
> used *numpy.linalg.solve(AB,b)* instead of *xB = (AB^−1)b* to calculate the value of XB
>
> used *v = np.linalg.solve(np.transpose(AB), cB)* calculated V to obtain v = ((AB^-1)^T)CB
>     *ZN = np.subtract(np.matmul(np.transpose(AN), v), cN)* instead of *xB = (Ab^-1An)^T Cb - Cn* to calculate the value of Zn
>
> used *v = np.linalg.solve(AB,b)*
>     *optimal_value = np.matmul(np.transpose(cB), v)* instead of *xB = ((Cb)^T)AB^-1b* to calculate the value of optimal value
>
> used *numpy.linalg.solve(AB,Aj)* instead of *xB = (AB^−1)Aj* to calculate the value of delta_XB

2. Similarly Under Dual Simplex Method:
> used *numpy.linalg.solve(AB,b)* instead of *xB = (AB^−1)b* to calculate the value of XB
>
> used *v = np.linalg.solve(np.transpose(AB), cB)*
>     *ZN = np.subtract(np.matmul(np.transpose(AN), v), cN)* instead of *xB = (Ab^-1An)^T Cb - Cn* to calculate the value of Zn
>
> used *v = np.linalg.solve(AB,b)*
>     *optimal_value = np.matmul(np.transpose(cB), v)* instead of *xB = ((Cb)^T)AB^-1b* to calculate the value of optimal value
>
> used *v = np.linalg.solve(np.transpose(AB), U)* calculated V to obtain v = ((Ab^T)^-1)u
        *delta_ZN = np.matmul(-np.transpose(AN), v)* instead of *delta_ZN = -An^T(AB^T)^-1u* to calculate the value of delta_ZN
