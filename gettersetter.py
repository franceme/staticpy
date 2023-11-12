#!/usr/bin/env python3

import os,sys
# Function to print getter and setter methods
# for variables according to Java
def getArgs():
	import argparse
	parser = argparse.ArgumentParser("Getter/Setter/Adder?")
	parser.add_argument("-n","--name", help="Name of the function",nargs='*', default=None)
	parser.add_argument("-t","--dataType", help="The Data Type",nargs='*', default=None)
	return parser.parse_args()

def print_getter_setter(variables, datatypes):
  
    # List to store getVariable
    getters = []
  
    # List to store setVariable
    setters = []
  
    # Iterate for every variable
    for var in variables:
  
        # Prepend "get" in every variable and change
        # the first character to uppercase
        getter = "get" + var[0].capitalize() + var[1:]
        getters.append(getter)
  
        # Prepend "set" in every variable and change
        # the first character to uppercase
        setter = "set" + var[0].capitalize() + var[1:]
        setters.append(setter)
  
      
    for i in range(len(variables)):
        
        current_getter = getters[i];
        current_setter = setters[i];
        current_var = variables[i];
        current_type = datatypes[i];

        if True:
            # Print the getter method
            print(f"""public function {current_getter}() returns {current_type} {{
    return self.{current_var};
}}""")

        if True:
            # Print the setter method
            print(f"""public function {current_setter}({current_type} {current_var}) {{
    self.{current_var} = {current_var};
}}""")

        if "[]" in current_type:
            if True:
                print(f"""public function add{current_var}({current_type.replace('[','').replace(']','')} sample){{
 self.{current_var}.push(sample);
}}""")
            if True:
                print(f"""public function addAll{current_var}({current_type} sample){{
    sample.forEach(self.add{current_var});
}}""")
 
# Driver function
if __name__=="__main__":
    args = getArgs()
    print_getter_setter(args.name, args.dataType)