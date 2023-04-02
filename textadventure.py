import json
import sys
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
        
        def opening_dialogue(self) :
            self.name = self.mapp[self.roomid]['name'] # string

            self.desc = self.mapp[self.roomid]['desc'] # String   

            self.exits = self.mapp[self.roomid]['exits'] # Dictionary
            try:
                self.items = self.mapp[self.roomid]['items'] # List

            except:
                self.items = []
                    
            if self.items != [] : 
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
            if self.inv_string == []:
                print("You're not carrying anything.")
            else :
                print(self.inv_string)

            Verbs.playerinput(self)
            return

        def get(self) :
            if len(self.pclist) == 2 :
                if self.pclist[1] in self.items :

                    self.inv.append(self.pclist[1])
                    self.inv_string = "Inventory: \n" + "\n".join(self.inv)
                    self.items.remove(self.pclist[1])
                    print("You have picked up the "+ self.pclist[1])
                else:
                    print(f"There's no {self.pclist[1]} anywhere.")

            else:
                print(self.pclist)
                print("Sorry, you need to 'get' something.")
            Verbs.playerinput(self)
            return    

        def quit(self) :
            print("Goodbye!")

        def action(self):
            if "go" in self.playerchoice :
                Verbs.go(self)
            elif "look" in self.playerchoice :
                Verbs.look(self)
            elif "inventory" in self.playerchoice :
                Verbs.inventory(self)
            elif "get" in self.playerchoice :
                Verbs.get(self)
            elif "quit" in self.playerchoice :
                Verbs.quit(self)    



        def playerinput(self) :        
            self.playerchoice = input("What would you like to do? ").lower()
            self.pclist = self.playerchoice.split(" ")
            Verbs.action(self)
            

    v = Verbs()
    v.opening_dialogue()
    v.playerinput()

        
except EOFError:
    print("Use 'quit' to exit.")
    v.playerinput()






