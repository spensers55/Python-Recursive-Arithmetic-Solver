# Recursive Arithmetic Solver   Python test program

#   --------REQUIREMENTS/SOLUTIONS/NOTES--------

# Need to check full statement outside of recursion
#	seperate method to validate the whole statement
#       check that no letters are present, that opening and closing parenthesis match, check that numbers are in the right place
# follow PEMDAS: must account for ^ and () symbols (modulus division not included for now)
#   other methods for calculating different substrings of the equation
#       maybe recursively solving in PEMDAS order

listOfOperators = {'+', '-', '*', '/', '^'}
listOfNumbers = {'1','2','3','4','5','6','7','8','9','0'}

# this function validates that the equation entered by the user is solvable by this program
def validate(equation):
    touchingOperator = False    # check to ensure two operators are not touching
    negOperator = False         # final check to make sure negative numbers are allowed and operators do not touch
    numOfOperators = 0          # counter for number of operators
    numUnresolvedPT = 0         # counter for unresolved pairs of parenthesis
    numOfNums = 0               # counter for number of digits
    i = 0
    try:
        while i < len(equation):          # run through whole equation
            if equation[i] in listOfNumbers: # ensure operator touch-checking works by checking for numbeers
                touchingOperator = False
                negOperator = False
                numOfNums += 1
            elif equation[i] in listOfOperators: # check for operators (if operators touching, invalidate)
                if touchingOperator == True:
                    if equation[i] == '-' and negOperator == False:
                        negOperator = True
                    else:
                        print("Error: operators touching")
                        return False
                else:
                    touchingOperator = True
                    numOfOperators += 1 # increment number of operators
            elif equation[i] == '(': # check for opening parenthesis
                numUnresolvedPT +=1 # add 1 to number of unresolved parenthesis
            elif equation[i] == ')': # check for closing parenthesis
                if numUnresolvedPT == 0: # if too many closing parenthesis, return invalid
                    return False
                else:
                    numUnresolvedPT -= 1 # else, decrement unresolved parenthesis
            else:
                print("Unknown character entered: error, line 38")
                return False
            i += 1
    except ValueError:
        print("Please enter numbers and operators only")
        return False
    if numUnresolvedPT > 0 or touchingOperator == True:
        print("Unresolved parenthesis or ending operator. Please try again")
        return False
    
    return True # if all conditions met, validated
# end function

# this function is the final step in the logic of the recursion.
def solve(equation): # when no more operators exist, it returns to the previous layer and passes the equation to here.

    operatorLoc = -1
    # locate operator
    operatorLoc = equation.find('^')
    if operatorLoc == -1:
        operatorLoc = equation.find('*')
    if operatorLoc == -1:
        operatorLoc = equation.find('/')
    if operatorLoc == -1:
        operatorLoc = equation.find('+')
    if operatorLoc == -1:
        operatorLoc = equation.find('-') # '-' is last in case of negative numbers

    # capture operator
    operator = equation[operatorLoc]

    # capture numbers
    firstNum = equation[0, operatorLoc]
    secondNum = equation[operatorLoc+1, len(equation)]

    # parse to int
    firstNum = int(firstNum)
    secondNum = int(secondNum)

    # calculate result
    if operator == "+":
        result = firstNum + secondNum
    elif operator == "-":
        result = firstNum - secondNum
    elif operator == "*":
        result = firstNum * secondNum
    elif operator == "/":
        result = firstNum / secondNum
    elif operator == "^":
        result = 1
        i = 0
        while i < secondNum:
            result *= firstNum
            i+=1

    # returning solution
    return result
# end function

def RecursiveSolve(equation): #note probe for o/c parenthesis then recur on contents. replace parenthesis with solution
    # this is a recursive function: the base case is no more operators at the end. This function divides the equation
    # this function must also play by the rules of PEMDAS
    # ------PARENTHESIS------
    oPT = -1 # open parenthesis location
    cPT = -1 # close parenthesis location
    i = '' # captures values at index locations
    index = 0 # index keeps track how far through the equation we are
    mismatch = 0 # to make sure internal parenthesis don't screw anything up
    for i in equation:
        if i == '(' and oPT != -1: # changes mismatch if 2nd pair of parenthesis
            mismatch += 1
        elif i == '(' and oPT == -1:
            oPT = equation[index] # captures opening parenthesis
        elif i == ')' and mismatch == 0:
            cPT = equation[index] # captures matching ending parenthesis
            break
        elif i == ')' and mismatch > 0:
            mismatch -= 1 # reduces mismatch from closing internal parenthesis
        index += 1
    if oPT != -1:
        result = RecursiveSolve(equation[oPT, cPT])
        beg = equation[0, oPT+1]
        end = equation[cPT, len(equation)]
        equation = beg + result + end
    # ------END PARENTHESIS------

    # ------TODO: finish rest of recursive class------

def main(): # driver to run the application
    while True: # rerun forever
        while True: # run until valid
            equation = input("Enter an arithmetic equation (no spaces, no letters): ")
            vdated = validate(equation) # function call to validate
            if vdated == True:
                break # when valid, break
        print("validation good")
        RecursiveSolve(equation) # function call to solve
# end main function

main() # function call to start program