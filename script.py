
# Net class: Contains the name of the net and the faults that are associated with it
class Net:
    all = []  # List of all instances
    def __init__(self,name,type = None ,level = None,Gate = None,Gate_inputs = None):
        self.name = int(name)
        self.type = type
        self.faults = ["sa0","sa1"]  # Default faults: Fault Population
        self.level = level
        self.Gate = Gate
        self.Gate_inputs = Gate_inputs
        Net.all.append(self)         # Add instance to list of all instances
        
    def __repr__(self):
        return f"Net_{self.name}" 
    
    def disp_attributes(self):
        # To display all attributes of the instance
        print("-----------------------------------------")
        print(f"Net_{self.name} :")
        print(f"name = {self.name}")
        print(f"type = {self.type}")
        print(f"faults = {self.faults}")
        print(f"level = {self.level}")
        print(f"Gate = {self.Gate}")
        print(f"Gate_inputs = {self.Gate_inputs}")
        print("-----------------------------------------")
    
    @classmethod
    def get_instance(cls,name):
        for instance in cls.all:
            if instance.name == name:
                return instance
        return None
    
    @classmethod
    def check_instance(cls,name):
        for instance in cls.all:
            if instance.name == name:
                return True
        return False



def Levelisation(netlist):

    output_list = []
    input_list = []
    primary_inputs = []
    primary_output = []



    for item in netlist:
        if item[0] == "INPUT":
            for node in item[1:]:
                if Net.check_instance(int(node)):
                    n = Net.get_instance(int(node))
                    n.type = "PrimaryInput"
                    n.level = 0
                else :
                    Net(node,"PrimaryInput",0)
                primary_inputs.append(node)
            

        elif item[0] == "OUTPUT":
            if Net.check_instance(int(item[1])):
                n = Net.get_instance(int(item[1]))
                n.type = "PrimaryOutput"
            else:
                Net(item[1],"PrimaryOutput")

            primary_output.append(item[1])
        

        elif item[0] == "FANOUT":
            for node in item[2:]:
                if Net.check_instance(int(node)):
                    n = Net.get_instance(int(node))
                    n.type = "FanoutWire"
                else:
                    Net(node,"FanoutWire")



        elif item[0] in ["AND","OR","NAND","NOR","NOT"]:

            output_list.append(item[1])

            # Handling output node 
            if Net.check_instance(int(item[1])):
                n = Net.get_instance(int(item[1]))
                if n.type == "PrimaryOutput":
                    pass
            else:
                Net(item[1],"wire")
            Net.get_instance(int(item[1])).Gate_inputs = item[2:]
            Net.get_instance(int(item[1])).Gate = item[0]

            # Handling input nodes
            for node in item[2:]:
                if Net.check_instance(int(node)):
                    n = Net.get_instance(int(node))
                    if n.type in ["FanoutWire","PrimaryInput"]:
                        pass
                else:
                    Net(node,"wire")

            
                input_list.append(node)
    

    input_list = [ node for node in input_list if node not in primary_inputs]


    count = int(max(primary_inputs))+1
    curr_level = 0

    while count <= int(primary_output[0]):
        if str(count) not in output_list:
            obj = Net.get_instance(count)
            obj.level = curr_level
            count += 1
        else:
            obj = Net.get_instance(count)
            inp = obj.Gate_inputs
            inp = [int(x) for x in inp]
            inp_objects = [Net.get_instance(x) for x in inp]
            inp_obj_levels = [x.level for x in inp_objects]
            obj.level = max(inp_obj_levels)+1
            curr_level = obj.level
            count += 1




def DominanceCollapsing(obj):

    if obj.Gate == "AND":

        if "sa0" in obj.faults:
            obj.faults.remove("sa0")
        if "sa1" in obj.faults:
            obj.faults.remove("sa1")

        inp_obj = []    
        inps = obj.Gate_inputs

        for inp in inps:
            inp_obj.append(Net.get_instance(int(inp)))

            # Getting wire that is attached to a gate : Retain faults only for this gate 
        retain_fault_obj = [obj for obj in inp_obj if obj.type == "wire"]


        
        # if more gate are inputs: retain first one and remove faults from others
        

        if len(retain_fault_obj) != 0:
            retain_fault_obj = retain_fault_obj[0]
            inp_obj.remove(retain_fault_obj)
        else:
            inp_obj.remove(inp_obj[0])

        # Now collapse the faults of the remaining objects
        for obj in inp_obj:
            if "sa0" in obj.faults:
                obj.faults.remove("sa0")

    
    if obj.Gate == "OR":
        if "sa0" in obj.faults:
            obj.faults.remove("sa0")
        if "sa1" in obj.faults:
            obj.faults.remove("sa1")

        inp_obj = []    
        inps = obj.Gate_inputs

        for inp in inps:
            inp_obj.append(Net.get_instance(int(inp)))

            # Getting wire that is attached to a gate : Retain faults only for this gate 
        retain_fault_obj = [obj for obj in inp_obj if obj.type == "wire"]


        
        # if more gate are inputs: retain first one and remove faults from others
        


        if len(retain_fault_obj) != 0:
            retain_fault_obj = retain_fault_obj[0]
            inp_obj.remove(retain_fault_obj)
        else:
            inp_obj.remove(inp_obj[0])

        # Now collapse the faults of the remaining objects
        for obj in inp_obj:
            if "sa1" in obj.faults:
                obj.faults.remove("sa1")

    
    if obj.Gate == "NAND":
        
        if "sa0" in obj.faults:
            obj.faults.remove("sa0")
        if "sa1" in obj.faults:
            obj.faults.remove("sa1")

        inp_obj = []    
        inps = obj.Gate_inputs

        for inp in inps:
            inp_obj.append(Net.get_instance(int(inp)))

            # Getting wire that is attached to a gate : Retain faults only for this gate 
        retain_fault_obj = [obj for obj in inp_obj if obj.type == "wire"]
  
        # if more gate are inputs: retain first one and remove faults from others

        if len(retain_fault_obj) != 0:
            retain_fault_obj = retain_fault_obj[0]
            inp_obj.remove(retain_fault_obj)
        else:
            inp_obj.remove(inp_obj[0])

        # Now collapse the faults of the remaining objects
        for obj in inp_obj:
            if "sa0" in obj.faults:
                obj.faults.remove("sa0")



    if obj.Gate == "NOR":
        if "sa" in obj.faults:
            obj.faults.remove("sa0")
        if "sa1" in obj.faults:
            obj.faults.remove("sa1")

        inp_obj = []    
        inps = obj.Gate_inputs

        for inp in inps:
            inp_obj.append(Net.get_instance(int(inp)))

            # Getting wire that is attached to a gate : Retain faults only for this gate 
        retain_fault_obj = [obj for obj in inp_obj if obj.type == "wire"]


        
        # if more gate are inputs: retain first one and remove faults from others
        


        if len(retain_fault_obj) != 0:
            retain_fault_obj = retain_fault_obj[0]
            inp_obj.remove(retain_fault_obj)
        else:
            inp_obj.remove(inp_obj[0])

        # Now collapse the faults of the remaining objects
        for obj in inp_obj:
            if "sa1" in obj.faults:
                obj.faults.remove("sa1")


    if obj.Gate == "NOT":
        if "sa" in obj.faults:
            obj.faults.remove("sa0")
        if "sa1" in obj.faults:
            obj.faults.remove("sa1")

        # No input collapsing for NOT gate



def main():

    with open("netlist.txt") as f:
        netlist = f.readlines()

    # Cleaning the netlist
    for i in range(len(netlist)):
        netlist[i] = netlist[i].split()
        netlist[i] = [x for x in netlist[i] if x != '']

    # Create Net objects and Levelise the Ckt

    Levelisation(netlist)
    print("\nPopulated Fault list for each node :")

    levelList = sorted(Net.all, key=lambda obj: obj.level,reverse=True)

    for net in levelList:
        print(f"Net : {net.name}, Faults: {net.faults}")

    TotalFaultBeforeCollapsing =  len(Net.all)*2


    print(f"\nTotal Faults before Collapsing :{TotalFaultBeforeCollapsing}")
    print("------------------------------------")


    # Fault collapsing
    for obj in levelList:
        DominanceCollapsing(obj)


    print("Fault list after Dominance Fault Collapsing :\n")

    NumFaultsAfterCollapsing = 0

    for net in Net.all:
        print(f"Net :{net.name},  Faults: {net.faults}")
        NumFaultsAfterCollapsing += len(net.faults)

    print("------------------------------------")   
    print(f"Collapse Ratio :{NumFaultsAfterCollapsing}/{TotalFaultBeforeCollapsing}")
    print("------------------------------------") 




if __name__ == "__main__":
    main()