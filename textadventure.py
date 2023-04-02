import json
import sys
import inspect
from pprint import pprint
data = json.load(open(sys.argv[1]))
try:
    class Game(object) :
        
        def __init__(self) -> None:
            
            self.roomid = 0
            self.mapp = data
            self.inv = []
            self.playerchoice = ''
            self.name = ''
            self.desc =''
            self.exits = {}
            self.items = []
            self.items_string = ''
            self.exits_string = ''
            self.prompt = ''
            self.inv_string = ''
            self.locked = {}
        def opening_dialogue(self) :

            self.name = self.mapp[self.roomid]['name'] # string

            self.desc = self.mapp[self.roomid]['desc'] # String   

            self.exits = self.mapp[self.roomid]['exits'] # Dictionary
            
            try:
                
                self.items = self.mapp[self.roomid]['items'] # List
                
                
            except:
                self.mapp[self.roomid]['items'] = []
                
                self.items = self.mapp[self.roomid]['items']
                
            try:
                self.locked = self.mapp[self.roomid]['locked'] 
            except:
                self.mapp[self.roomid]['locked'] = {}
                self.locked = self.mapp[self.roomid]['locked']

            if len(self.items) != 0 : 
                
                self.items_string = "Items: " + " ".join(self.items)  +"\n\n"  
            else :
                
                self.items_string = ''
                


            self.exits_string = "Exits: " + " ".join(self.exits.keys())
            
            self.prompt = "> " + self.name + "\n\n" + self.desc + "\n\n" + self.items_string + self.exits_string +"\n"
            print(self.prompt)
            return
        

    class Verbs(Game) :
        def __init__(self) -> None:
            super().__init__()
            self.pclist = []
            self.directions = ['north','south', 'east', 'west', 'nw','ne' ,'se', 'sw','northwest','northeast', 'southeast','southwest']
        

        def go(self):
            if len(self.pclist) == 2 :
                if self.pclist[1] in self.exits.keys() :


                    print("You " + self.playerchoice)
                    self.roomid = self.exits[self.pclist[1]]
                    Game.opening_dialogue(self)
                else:
                    print(f"There's no way to go {self.pclist[1]}.")
            else:
                print(self.pclist)
                print("Sorry, you need to 'go' somewhere.")
            Verbs.playerinput(self)
            return
        
        def look(self) :
            Game.opening_dialogue(self)
            Verbs.playerinput(self)
            return
        
        def inventory(self) :
            if self.inv_string == '':
                print("You're not carrying anything.")
                
            else :
                print(self.inv)
                print(self.inv_string)

            Verbs.playerinput(self)
            return

        def get(self) :
            if len(self.pclist) == 2 :
                if self.pclist[1] in self.items :

                    self.inv.append(self.pclist[1])
                    self.inv_string = "Inventory: \n" + "\n".join(self.inv)
                    self.items.remove(self.pclist[1])
                    # print(self.items)
                    # self.items_string =
                    print("You pick up the "+ self.pclist[1])
                else:
                    print(f"There's no {self.pclist[1]} anywhere.")
            
            elif len(self.pclist) == 1 :

                    print("Sorry, you need to 'get' something.")

            else:
                if self.playerchoice[4:] in self.items:
                    self.inv.append(self.playerchoice[4:])
                    self.inv_string = "Inventory: \n" + "\n".join(self.inv)
                    self.items.remove(self.playerchoice[4:])
                    # print(self.items)
                    # self.items_string =
                    print("You pick up the "+ self.playerchoice[4:])
                else :
                    print(f"There's no {self.playerchoice[4:]} anywhere.")

                
            Verbs.playerinput(self)
            return    
        def drop(self) :
            if len(self.pclist) == 2:
                if self.pclist[1] in self.inv :
                    self.inv.remove(self.pclist[1])
                    
                    self.items.append(self.pclist[1])
                    if self.inv == [] :
                        self.inv_string = ''
                        
                    else :
                        print(self.inv)
                        self.inv_string = "Inventory: \n" + "\n".join(self.inv)
                    print("You drop the "+ self.pclist[1])
                else:
                    print(f"You don't have the {self.pclist[1]} in your inventory")
            
            elif len(self.pclist) == 1 :


                    print("Sorry, you need to 'drop' something.")

            else:

                if self.playerchoice[5:] in self.inv :
                    self.inv.remove(self.playerchoice[5:])
                    
                    self.items.append(self.playerchoice[5:])
                    if self.inv == [] :
                        self.inv_string = ''
                        
                    else :
                        print(self.inv)
                        self.inv_string = "Inventory: \n" + "\n".join(self.inv)
                    print("You drop the "+ self.playerchoice[5:])
                else:
                    print("entered else no item in inventory")
                    print(f"You don't have the {self.playerchoice[5:]} in your inventory")
                
            Verbs.playerinput(self)
            return

        def quit(self) :
            print("Goodbye!")
            return
        

        def action(self):
            self.pclist = self.playerchoice.split(" ")
            if "go" in self.playerchoice :
                Verbs.is_locked(self)
            elif "look" in self.playerchoice :
                Verbs.look(self)
            elif "inventory" in self.playerchoice :
                Verbs.inventory(self)
            elif "get" in self.playerchoice :
                Verbs.get(self)
            elif "quit" in self.playerchoice :
                Verbs.quit(self)    
            elif "drop" in self.playerchoice :
                Verbs.drop(self)
            elif self.playerchoice in self.directions :
                Verbs.abbrev(self)

            
            
        def is_locked(self) :

            if self.pclist[1] in self.locked :
                print(f"\nThe Exit is locked.\n\nYou need {self.locked[self.pclist[1]]} to unlock the exit\n")
                print("Checking your inventory...\n")
                if self.locked[self.pclist[1]] in self.inv :
                    print(f"You have the {self.locked[self.pclist[1]]}\n")
                    print("The exit is unlocked.\n")
                    del self.locked[self.pclist[1]]
                    Verbs.go(self)
                else:
                    print(f"You don't have the {self.locked[self.pclist[1]]}")
                    print(f"Visit next time when you have the {self.locked[self.pclist[1]]}")
                    Verbs.playerinput(self)
            else:
                Verbs.go(self)

            return
 
            


        def playerinput(self) :        
            self.playerchoice = input("What would you like to do? ").lower().strip()
            
            Verbs.action(self)

        def abbrev(self) :
            if self.playerchoice == "north" :
                self.playerchoice = "go north"
            elif self.playerchoice == "south" :
                self.playerchoice = "go south"
            elif self.playerchoice == "west" :
                self.playerchoice = "go west"
            elif self.playerchoice == "east" :
                self.playerchoice = "go east"
            elif self.playerchoice == "nw" or self.playerchoice == "northwest" :
                self.playerchoice = "go northwest"
            elif self.playerchoice == "ne" or self.playerchoice == "northeast":
                self.playerchoice = "go northeast"
            elif self.playerchoice == "se" or self.playerchoice == "southeast":
                self.playerchoice = "go southeast"
            elif self.playerchoice == "sw" or self.playerchoice == "southwest" :
                self.playerchoice = "go southwest"
            

            Verbs.action(self)


    v = Verbs()
    v.opening_dialogue()
    v.playerinput()

        
except EOFError:
    print("Use 'quit' to exit.")
    v.playerinput()





