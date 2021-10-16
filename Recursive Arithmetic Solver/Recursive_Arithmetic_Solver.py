# Recursive Arithmetic Solver   Python test program

#   --------REQUIREMENTS/SOLUTIONS/NOTES--------

# Need to check full statement outside of recursion
#	seperate method to validate the whole statement
#       check that no letters are present, that opening and closing parenthesis match, check that numbers are in the right place
# follow PEMDAS: must account for ^ and () symbols (modulus division not included for now)
#   other methods for calculating different substrings of the equation
#       maybe recursively solving in PEMDAS order

listOfOperators = {'+', '-', '*', '/', '^'}
listOfNumbers = {'1','2','3','4','5','6','7','8','9','0','.'}

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
    firstNumStr = equation[0:operatorLoc]
    secondNumStr = equation[operatorLoc+1:len(equation)]

    # parse to int
    firstNum = float(firstNumStr)
    secondNum = float(secondNumStr)

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

def RecursiveParenthesis(equation): #note probe for o/c parenthesis then recur on contents. replace parenthesis with solution
    # this is a recursive function: the base case is no more operators at the end. This function divides the equation
    # this function must also play by the rules of PEMDAS
    # ------PARENTHESIS------
    while True: # loop to ensure all outer parenthesis are solved
        oPT = -1 # open parenthesis location
        cPT = -1 # close parenthesis location
        i = '' # captures values at index locations
        index = 0 # index keeps track how far through the equation we are
        mismatch = 0 # to make sure internal parenthesis don't screw anything up
        for i in equation:
            if i == '(' and oPT != -1: # changes mismatch if 2nd pair of parenthesis
                mismatch += 1 # bad
            elif i == '(' and oPT == -1:
                oPT = index # captures opening parenthesis
            elif i == ')' and mismatch == 0:
                cPT = index+1 # captures matching ending parenthesis
                break
            elif i == ')' and mismatch > 0:
                mismatch -= 1 # reduces mismatch from closing internal parenthesis
            index += 1
        if oPT != -1:
            substring = equation[oPT:cPT] # slice out parenthesised section (including parenthesis)
            substring = substring[1:len(substring)-1] # slice out parenthesis
            result = RecursiveParenthesis(substring) # recur to check for nested parenthesis
            beg = equation[0:oPT] # beginning
            end = equation[cPT:len(equation)] # end
            equation = beg + str(result) + end # reassign
        else: # if no parenthesis detected
            return exponents(equation)
        return exponents(equation)  # pass to exponents regardless of presence of parenthesis

    # ------END PARENTHESIS------

def exponents(equation):
# ------EXPONENTS------
    index = -1 # start at -1 due to pre-adding
    while index < len(equation)-1: # range check at -1 due to pre-adding
        index += 1
        if equation[index] == '^': # check for exponents entered
            equation = completeOperation(equation, index) # send to get solved
    return multiplication(equation)

    # ------END EXPONENTS------

def multiplication(equation):
    # ------MULTIPLICATION------
    index = -1
    while index < len(equation)-1:
        index += 1
        if equation[index] == '*': # check for multiplications entered
            equation = completeOperation(equation, index)
    return division(equation)
    # ------END MULTIPLICATION------

def division(equation):
    # ------DIVISION------
    index = -1
    while index < len(equation)-1:
        index += 1
        if equation[index] == '/': # check for division entered
            equation = completeOperation(equation, index)
    return addition(equation)
    # ------END DIVISION------

def addition(equation):
    # ------ADDITION------
    index = -1
    while index < len(equation)-1:
        index += 1
        if equation[index] == '+': # check for addition entered
            equation = completeOperation(equation, index)
    return subtraction(equation)
    # ------END ADDITION------

def subtraction(equation):
    # ------SUBTRACTION------
    index = -1
    while index < len(equation)-1:
        index += 1
        if equation[index] == '-': # check for subtraction entered
            equation = completeOperation(equation, index)
    return equation
    # ------END SUBTRACTION------



def completeOperation(equation, index):
    counter = 1     # counts distance from the operator
    begOf1st = -1   # locates the beginning of the first number involved in the operation
    endOf2nd = -1   # locates the end of the 2nd number involved in the operation

    while True: # while loop to increment counter and find numbers
        # when either counter finds an operator, the if statement knows it's found the beginning/end of the number
        if (index-counter <= 0 or equation[index-counter] in listOfOperators) and begOf1st == -1:
            begOf1st = index-counter  # store location of beginning
        if (index+counter >= len(equation) or equation[index+counter] in listOfOperators) and endOf2nd == -1:
            endOf2nd = index+counter    # store location of end
        counter += 1    # increment counter
        if begOf1st != -1 and endOf2nd != -1:
            break   # if found both beginning and end, break and return
    result = solve(equation[begOf1st:endOf2nd])    # run solve function, get mathematical result
    return equation[0:begOf1st] + str(result) + equation[endOf2nd:len(equation)] # replace operation with result, return for passing


def main(): # driver to run the application
    while True: # rerun forever
        while True: # run until valid
            equation = input("Enter an arithmetic equation (no spaces, no letters): ")
            vdated = validate(equation) # function call to validate
            if vdated == True:
                print(RecursiveParenthesis(equation)) # function call to solve
                break # when valid, break
             
# end main function

main() # function call to start program