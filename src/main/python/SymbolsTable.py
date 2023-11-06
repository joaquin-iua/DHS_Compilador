from Context import Context
from ID import ID

class SymbolsTable:
    __instance = None
    context_list = None

    @staticmethod
    def get_symbols_table():
         if SymbolsTable.__instance == None:
            SymbolsTable()
         return SymbolsTable.__instance
    
    def __init__(self):
      if SymbolsTable.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         SymbolsTable.__instance = self
         SymbolsTable.context_list = [Context()]

    def create_context(self):
        self.context_list.append(Context())

    def delete_context(self):
        if len(self.context_list) > 1:
            self.context_list.pop()

    def get_last_context(self):
        return self.context_list[-1]        

    def find_in_last_Context(self, name):
        last_context = self.context_list[-1]
        found_id = last_context.find(last_context, name)
        return found_id
        
    def find_global(self, name):
         for context in reversed(self.context_list):
             found_id = context.find(context, name)
            
             if(found_id != None):
                 return found_id
             
         return None
                 
    def add_id(self, id):
        last_context = self.context_list[-1]
        last_context.add_id(id)

    def last_context_to_string(self):
        last_context = self.context_list[-1]
        last_context.to_string()

if __name__ == "__main__":
    st = SymbolsTable.get_symbols_table()

    #st.create_context()
    context = st.get_last_context()
    id_a = ID("a", "int")
    context.add_id(id_a)
    print(context.to_string())

    print(st.last_context_to_string())
