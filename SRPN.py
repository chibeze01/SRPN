operand = list() # this is the number stack 
operator_buffer = list() # this is called a buffer not a stack becaue it hold one value for less than 0.5 seconds at any given time
operator = ['d','-','+','*','/','%', '^'] # this is the precedence order with d[0] at the buttom and powers at the top[6]
r = [ 1804289383,846930886,1681692777,1714636915,1957747793,424238335,719885386,1649760492,596516649,1189641421,1025202362,1350490027,783368690,1102520059,2044897763,1967513926,1365180540,1540383426,304089172,1303455736,35005211,521595368] # this is the seeded rand num list.
index = 0 # here i initalise a glabal variable used to traverse the list r
comment = False #here i initalise a glabal boolean variable 
stop = False
# for my solution i have desided to convert infix to postfix. so i only have one calculator, which is below:
def postfix_calculator (): # procedure calculates the postfix inputs and push onto the operand stack.
  global stop
  while len (operator_buffer) != 0  : # if the operator_buffer is empty -> stop.
    result= 0 # result varriable 
    num1 ,num2, operator= operand.pop(), operand.pop(), operator_buffer.pop() # pops the operand and operator_buffer to get the values.
    if num1 == 0 and operator =="/": # check for divide by zero situations
      print ("Divided by 0"),operand.append(num2) , operand.append(num1); break # displays suitable message and pushes the valuse onto the operand stack and breaks out the while loop
    elif operator == "^": # handle negative power situations
      if num1 < 0 : # checks if the power numnber is less than 0
        print("Negative power."), operand.append(num2) , operand.append(num1); break # displays suitable message and pushes the valuse onto the operand stack and breaks out the while loop
      elif num2 < 0 and num1%2==0: # handle situation where power number is divisible by two and base is negative
        result= eval(str(num2)+operator+str(num1))*-1 # eval() returns -4 for -2^2 calculation os this check is necessary 
      elif num2 < 0 and isinstance(num1,float): # handle situation where power number is a fraction and base is negative
         result = -2147483648 # result is the floor of the saturation range
      else:
        operator = "**"; result= eval(str(num2)+operator+str(num1)) # eval does not recognise ^ so i convert to **
    elif operator == "%" and num1 == 0: # checks if operator is "%" and the divisor is 0. for situations like 6%0
      for i in r: # the srpn crashes in this situation
        print ("bash: ",i,": command not found"); stop = True # displays these things and tells the program to stop
      break # i do this because srpn prints these things and then stops the program 
    else:# if operator not "/" or "^" 
      result= eval(str(num2)+operator+str(num1)) # calculate result with eval.
    if result > 2147483647 : # checks if the input is greater than 2147483648 
      operand.append(2147483647) # push celling of saturation onto the operand stack 
    elif result < -2147483648: # checks if the input is less than -2147483648
      operand.append(-2147483648) # push floor of saturation onto the operand stack 
    else:
      operand.append(result) # whilst appending the new number (result) to the number list.
  pass
#----------------------------------------------------------------------------
def octtodec (numop:str): # function when the input is a octal number
  try : # try - except is a error handler. it tries to perform the operation below, if the number is not a octal number (i.e. 9) then then code below produces an error
    operand.append(int(numop, 8)) # inbuilt python converter int(input, 8) produces error when input contains 8 or 9. pushes the converted value onto the stack
  except ValueError : # if there an error the do this code below. so no crashes 
    if len(numop.replace("8", ""))>1 or len(numop.replace("9", "")) > 1 : # removes non octal values from the input and calculates the lenght of the input  
      pass # srpn does not push "019" on stack only pushes "09" or "08" on to the operand stack 
    else:
      operand.append(int(numop)) # converts "09" or "08" to "8" or "9"
#-------------------------------------------------------------------------
def rand(): #This is the random number generator, in this function i traverse the list in a circle:
  global index # gets the glabal varriable index 
  if len(operand)  == 23 : # checks if the operand stack is full 
    print ("Stack Overflow.")
  elif index > 21: #checks if index point to the end of the list r. understand that 0 -21 ==22 and in srpn [r] has seed range of 22 
    index = 0; operand.append(r[index]); index = index + 1 # go back to the front [index = 0] push front value onto the operand stack and incrament the index by 1 
  else: 
      operand.append(r[index]); index = index + 1 # push value onto the operand stack and incrament the index by 1
#--------------------------------------------------------------
def input_verification(numop:str): # verifies the input and processes different input states.
  global comment # this is a global boolean for comment input state
  if not comment : # if the input is not a coment then dont ignore it
    if numop == "d" : # checks if input is "d" 
      if len(operand) == 0: # checks if the operand sack is empty
        print (-2147483647) # if TRUE then print floor of saturation
      else:
        for i in operand : # if FALSE then for elements in the operand stack
          print (int(i)) # display each element as intergers
    
    elif numop == "r": # check if input is "r"
      rand() # if TRUE call the rand function; rand = random 
    
    elif len(numop) > 1 and numop[0] == "0" and numop[1] != "0" : # checks if input is "013", where only the fisrt digit is 0
      octtodec(numop) # calls the oct to dec procedure
    
    elif len(numop) > 2 and numop[0] == "-" and numop[1] == "0" and numop[2] != "0" : # checks if the input is a negative octal number 
      octtodec(numop) # calls the oct to dec procedure
    
    elif numop.isnumeric() : # here check if the input is numeric
      if len(operand) < 22: # checks if the stack is not full
        operand.append(int(numop)) # if not full push the input onto the stack
      else:
        print ("Stack Overflow.") # if stack full display Stack over flow.
    
    elif len(numop) > 1 and numop[0] == "-" and numop[1].isnumeric() : # here i check if it is a negative input 
      if len(operand) < 22: # check if the stack is not full
        operand.append(int(numop)) # if not full push the input onto the stack
      else:
        print ("Stack Overflow.") # if stack full display Stack over flow.
    
    elif numop in operator : # checks if the input is an operator
      if len(operand) < 2: # checks if the operand stack has less than 2 values 
        print ("Stack underflow.") # if it does display stack underflow.
      else:
        operator_buffer.append(numop) # append this to the operator buffer.
        postfix_calculator() #calls the postfix calculator
    
    elif numop == "=" : # checks if the input is an equal sign 
      if len(operand ) == 0: # checks if the stack is empty
        print ("Stack empty.") # if it is empty displays stack empty.
      else:
        print (int(operand[-1])) # if it isn't then display the top of the stack 

    else: # after all the checks 
      for i in numop: # display for each character in the input 
        print('Unrecognised operator or operand "',i,'".')
  else: # the comment is on then
    pass # the program does nothing
#-----------------------------------------------------------
def infixtopostfix (expr:list): # this function converts infix to postfix
  stack = list() # created a stack 
  postfix = list() # created a list
  for i in range (0,len(expr)): # for loop till the end of the list expr
    if expr[i].isnumeric() or expr [i] =="r": # if the index in expr is numeric or "r"
      postfix.append(expr[i]) # then append this to the postfix list 
    elif expr[i] in operator: # checks if the index is an operation, if it is then 
      while len(stack) != 0 and (operator.index(stack[-1]) >= operator.index(expr[i])): # while the stack is not empty and the operator has lower or equal precedence to the operator at the top of the stack
        postfix.append(stack.pop()) # pop all that is on the stack
      if expr[i] =="d": # checks if its a "d"
        postfix.append(expr[i]) # if so put it in the list 
      else: 
        stack.append(expr[i]) # push the current operator onto stack 
    else:
      postfix.append(expr[i]) # if it is not an opeator or an operand put it in the list
  while len(stack)!= 0 : # after we gone through the expr there is still operators on the stack
    postfix.append(stack.pop()) # so pop the stack until it is empty
  return postfix # return the list in postfix order
#-------------------------------------------------------------------------
def infix_spliter(numop:str):           # this section splits any infix input i.e. 2+3 is split to 2 + 3
  global comment                        # global boolean for comment states
  expr = ""                             # empty str, where expr = expression 
  isdigit =  False                      # boolean var. will be used for sign handling
  for i in range (0, len(list(numop))): # here i loop through the character in string (numop)
    if numop[i].isnumeric():            # checks if the character is numeric
      expr = expr + numop[i]            # concatenates the character to the expr
      isdigit =  True                   # it is a digit
    elif numop == "#":                  #check if the numop itself is "#", becaue in the main we split the input with spaces 
      if comment == False:              # checks if the comment state is off 
        comment = True                  # if it is off then turn it on
      else:
        comment = False                 # else turn it off
    else:                               # here i handle non positive numeric and non "#" inputs 
      if numop[i] == "-":               # checks if the first character is a minus 
        if isdigit:                     # if the previous character was a digit
          expr = expr + " "+numop[i] +" " # concatenats the operator with spaces on either side
          isdigit = False               # it is not a digit 
        else:                           # the previous character was not a digit 
          expr = expr +  numop[i]       # concatenate the operator with no spaces
          isdigit=False                 # it is not a digit
      else:                             # if it does not int, # or "-" then 
        expr = expr + " " + numop[i] +" " # concatenate with spaces on either side of it 
        isdigit = False                 # is digit is false
  return expr                           # returns the expression
#--------------------------------------------------------------------------
if __name__ == "__main__": # this is the main. The code is executed from here 
  print ("You can now start interacting with the SRPN calculator")
  while True :
    numop = input () # get user input numop = number or operation 
    numop = numop.split() # to handle the spaces in the input between each number and operator. makes a list
    for i in numop: # gose through the list numop = list()
      for z in infixtopostfix( infix_spliter(i).split()): # here i call multiple functions. i split the expr with the spaces to make a list, and call the infixtopostfix function to convert the list into postfix form.
        # z is an indivudual operation or operand from the list infixtopostfix( infix_spliter(i).split()).
        input_verification(z) # here i call the verification function to verify each input in the list. 
    if stop : # here checks if stop is true 
      break# stops the program
    
