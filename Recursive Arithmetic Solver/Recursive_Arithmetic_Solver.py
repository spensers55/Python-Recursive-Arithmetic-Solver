# Recursive Arithmetic Solver   Python test program

#   --------REQUIREMENTS/SOLUTIONS/NOTES--------

# Need to check full statement outside of recursion
#	seperate method to validate the whole statement
#       check that no letters are present, that opening and closing parenthesis match, check that numbers are in the right place
# follow PEMDAS: must account for ^ and () symbols (modulus division not included for now)
#   other methods for calculating different substrings of the equation
#       maybe recursively solving in PEMDAS order
# THIS PROJECT IS A WORK IN PROJECT. In it's current form, it is usable. More updates are expected.
# This project was done using Pair Programming (for help when stuck and for sanity) with Justin Chikosky @ justin.chikosky@gmail.com

import tkinter
import threading

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
                        popup("Error: operators touching")
                        return False
                else:
                    touchingOperator = True
                    numOfOperators += 1 # increment number of operators
            elif equation[i] == '(': # check for opening parenthesis
                numUnresolvedPT +=1 # add 1 to number of unresolved parenthesis
            elif equation[i] == ')': # check for closing parenthesis
                if numUnresolvedPT == 0: # if too many closing parenthesis, return invalid
                    numUnresolvedPT -= 1 # else, decrement unresolved parenthesis
            else:
                popup("Unknown character entered: error")
                return False
            i += 1
    except ValueError:
        popup("Please enter numbers and operators only")
        return False
    if numUnresolvedPT != 0 or touchingOperator == True:
        popup("Unresolved parenthesis or ending operator. Please try again")
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
        if operatorLoc == 0:
            operatorLoc = equation[1:len(equation)].find('-') # if there is a negative number

    # capture operator
    operator = equation[operatorLoc]

    # capture numbers
    firstNumStr = equation[0:operatorLoc]
    secondNumStr = equation[operatorLoc+1:len(equation)]

    # parse to float
    firstNum = float(firstNumStr)
    secondNum = float(secondNumStr)

    # calculate result
    if operator == "+":
        result = float(float(firstNum) + float(secondNum))
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
            if(index-counter==0):
                begOf1st = 0
            elif equation[index-counter] == '-':
                if equation[index-counter-1] in listOfOperators:
                    begOf1st = index-counter
                else:
                    begOf1st = index-counter+1
            else:
                begOf1st = index-counter+1
        if (index+counter >= len(equation) or equation[index+counter] in listOfOperators) and endOf2nd == -1:
            if(counter == 1 and equation[counter+index] == '-'):    # if it's a negative number
                pass
            else:
                endOf2nd = index+counter    # store location of end
        counter += 1    # increment counter
        if begOf1st != -1 and endOf2nd != -1:
            break   # if found both beginning and end, break and return
    result = solve(equation[begOf1st:endOf2nd])    # run solve function, get mathematical result
    return equation[0:begOf1st] + str(result) + equation[endOf2nd:len(equation)] # replace operation with result, return for passing

def popup(message):     # a general tkinter function to send a message to a tkinter popup
    popupScene = tkinter.Tk()
    popupMessage = tkinter.Label(popupScene, text=message)
    popupMessage.grid(row=0,column=0)
    quitButton = tkinter.Button(popupScene, text="Quit", command=lambda:quitTK(popupScene))
    quitButton.grid(row=2,column=1)


def quitTK(quitScene):  # a general tkinter function to destroy the scene (close the window) passed in.
    quitScene.destroy()

def RecursiveSpark(expression, entryBox): # this function is required due to how threads behave and the nature of recursive logic
    # here, we must call the recursiveParenthesis function and call the popup function using the results
    RecursiveParenthesis(expression)
    insertVal = tkinter.StringVar # INCOMPLETE
    

def start(expressionEntry1, expressionEntry2, expressionEntry3):
    expression1 = expressionEntry1.get()
    expression2 = expressionEntry2.get()
    expression3 = expressionEntry3.get()
    if validate(expression1):
        t1 = threading.Thread(target=RecursiveSpark, args=(expression1,expressionEntry1,))
        t1.start()
    if validate(expression2):
        t2 = threading.Thread(target=RecursiveSpark, args=(expression2,expressionEntry2,))
        t2.start()
    if validate(expression3):
        t3 = threading.Thread(target=RecursiveSpark, args=(expression3,expressionEntry3,))
        t3.start()
    try: # try/catch block required in case validation fails
        t1.join()
    except(UnboundLocalError):
        popup("Expression 1 is invalid")
    try:
        t2.join()
    except(UnboundLocalError):
        popup("Expression 2 is invalid")
    try:
        t3.join()
    except(UnboundLocalError):
        popup("Expression 3 is invalid")
    pass

def main(): # driver to run the application
    scene = tkinter.Tk()
    topLabel = tkinter.Label(scene, text="Enter an arithmetic expression to solve it. Do not use spaces or algebraic terms.")
    topLabel.grid(row=0,column=0,columnspan=4)
    expressionInput1 = tkinter.Entry(scene)
    expressionInput1.grid(row=1,column=0)
    expressionInput2 = tkinter.Entry(scene)
    expressionInput2.grid(row=1,column=1,columnspan=2)
    expressionInput3 = tkinter.Entry(scene)
    expressionInput3.grid(row=1,column=3)
    enterButton = tkinter.Button(scene, text="Enter", command=lambda:start(expressionInput1, expressionInput2, expressionInput3))
    enterButton.grid(row=2,column=1)
    #expressionInput.bind('<Return>', lambda expressionInput:start(expressionInput))
    quitButton = tkinter.Button(scene, text="Quit", command=lambda:quitTK(scene))
    quitButton.grid(row=2,column=2)
    scene.mainloop()
             
# end main function

main() # function call to start program