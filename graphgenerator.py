
#!/usr/bin/env python
from decorator import decorator

import matplotlib.pyplot as plt
import pickle
import networkx as nx


@decorator
def on_start(func,*args, **kwargs):
    if kwargs !={}:
        try:
            if kwargs['Start']:
                if 'Verbose' in kwargs['Settings']:
                    if kwargs['Settings']['Verbose']:
                        print(func)
                        pass
                response= func(*args,**kwargs)
                return response
            else:
                kwargs['Start'] = False
                print(func,"DID NOT START")
                return(kwargs)
        except Exception as e:
            print('NODE ERROR OCCURED TRYING TO START NODE FUNCTION:')
            print('===========================================')
            print(func,e)
            print('===========================================')
            print('LAST STATE SET TO:')
            print('===========================================')
            print('ekwargs')
            print('===========================================')
            print('LAST NODE FUNCTION SET TO:')
            print('===========================================')
            print('efunc')
            print('===========================================')
            global ekwargs
            global efunc
            ekwargs = kwargs
            efunc = func
            print('HALTING')
            raise
    else:
        print('Empty kwargs')
        return ()



def start():
    return {'Start':True,'Settings':{'Verbose':True},'Status':{},'Threads':[]}

 
@on_start
def nodeGraph(*args,**kwargs):
    nodes = 8000
    k = 20
    prob = 0.1
    G = nx.newman_watts_strogatz_graph(nodes, k, prob)
    kwargs['Settings']['NetworkX']={"nodes":nodes, "k":k,"prob":prob}
    pos = nx.spring_layout(G)
    kwargs['Settings']['NetworkX']['Pos']= pos
    #nx.draw(G, with_labels=True, font_weight='bold',pos=pos)
    #plt.show()
    
    kwargs['Data'] = G
    return kwargs
 
@on_start
def data2Pickle_node_12(*args,**kwargs):
    pickle.dump(kwargs,open("nodegraph8000.pkl","wb"))
    return kwargs
 


class StremeNode:
    def __init__(self):
        pass

    def run(self,*args,**kwargs):
        self.kwargs=data2Pickle_node_12(**nodeGraph(**kwargs))
        return (self.kwargs)

class liveprocess:
    def __init__(self):
        pass
        
    def run(self,expname="Local"):
        self.response=data2Pickle_node_12(**nodeGraph(**start()))
        return(self.response)

if __name__ == '__main__':
    process = liveprocess()
    process.run()
    