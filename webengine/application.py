
class Root(object):
                        
    def index(self):
        return 'Hello World! '+str(self.value)


    
    index.exposed = True
