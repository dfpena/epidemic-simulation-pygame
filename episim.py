
#!/usr/bin/env python
from decorator import decorator

import random
import numpy as np
import pygame.gfxdraw as gfx
import pickle
import pygame as pg


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

 
def remap(narray,resolution):
    x = np.interp(narray[0],[-1,1],[15,resolution[0]-15])
    y = np.interp(narray[1],[-1,1],[50,resolution[1]- 15])
    return np.array([int(x),int(y)])


@on_start
def simLoop1(*args, **kwargs):
############################## EDIT THESE PARAMETERS ########################
    inflength = 8
    mortality = 0.0015
    rnaught = 2
    infprob = 0
#############################################################################

    if infprob == 0:
        infprob = rnaught/(kwargs['Settings']['NetworkX']['k']*inflength)
    if rnaught == 0:
        rnaught = infprob*kwargs['Settings']['NetworkX']['k']*inflength
    
    pos = kwargs['Settings']['NetworkX']['Pos']
    G = kwargs['Data']
    screensize = (800,800)
    G.graph['colors'] = {"Naive":(99, 7, 238),"Infected":(145, 238, 7),"Immune":(255, 235, 59),"Dead":(239, 99, 7)}
    G.graph['disease'] = {"Infection Probability" : infprob, "Infection Length" : inflength, "Mortality": mortality}
    # Add Parameters to Nodegraph
    for nid in G:
        G.nodes[nid]['Status'] = 'Naive'
        G.nodes[nid]['Day'] = 0
    # Remap -1 1 square to  pygame resolution
    for nid in pos:
        pos[nid] = remap(pos[nid],screensize) 
    G.nodes[0]['Status'] = 'Infected'
    # initialize the pygame module
    pg.init()
    # load and set the logo
    #logo = pg.image.load("logo.png")
    #pg.display.set_icon(logo)
    pg.display.set_caption("Normal Flu")
    legend = pg.image.load('legend.png')
     
    # create a surface on screen that has the size of 240 x 180
    screen = pg.display.set_mode(screensize)
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((236, 239, 241))
    
    green = (255, 255, 255) 
    deaths = 0
    infected = 1
    infday = 0 
    font = pg.font.Font(pg.font.match_font('lato'), 20)
    text = font.render('R0: {0}'.format(rnaught), True, green)
    textinfected = font.render('Infected: {0}'.format(infected), True, green)
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        infected = 0
        if infday == 366:
            running = False
        screen.blit(background, (0, 0))
        pg.draw.rect(background,(74,20,140),(0,0,screensize[0],80),0)
        screen.blit(text, (10,10))
        textdeath = font.render('Deaths: {}'.format(deaths), True, green)
        screen.blit(textdeath, (10,40))
        textdays = font.render('Epidemic Day: {}'.format(infday), True, green)
        screen.blit(textdays, ((screensize[0]/2)-40,10))
        for nid in pos:
            for e in G.edges(nid):
                cnode= e[1]
                gfx.line(screen,pos[nid][0],pos[nid][1],pos[cnode][0],pos[cnode][1],(120,144,156))
        for nid in pos:
            color = G.graph['colors'][G.nodes[nid]['Status']]
            gfx.aacircle(screen, pos[nid][0],pos[nid][1], 6, color)
            gfx.filled_circle(screen, pos[nid][0],pos[nid][1], 6, color)
            if G.nodes[nid]['Status'] == "Infected":
                infected = infected+1
                if G.nodes[nid]['Day'] == G.graph['disease']["Infection Length"]:
                    roll = random.random()
                    if roll >= G.graph['disease']['Mortality']:
                        G.nodes[nid]['Status'] = "Immune"
                    if roll < G.graph['disease']['Mortality']:
                        G.nodes[nid]['Status'] = "Dead"
                        deaths=deaths+1
                G.nodes[nid]['Day'] = G.nodes[nid]['Day'] + 1
                for e in G.edges(nid):
                    cnode = e[1]
                    if G.nodes[cnode]['Status'] != "Dead": 
                        if G.nodes[cnode]['Status'] != "Immune":
                            roll = random.random()
                            if roll < G.graph['disease']['Infection Probability']:
                                G.nodes[cnode]['Status'] = 'Infected'
                
    # event handling, gets all event from the event queue
        for event in pg.event.get():
    # only do something if the event is of type QUIT
            if event.type == pg.QUIT:
    # change the value to False, to exit the main loop
                running = False
        infday = infday + 1
        screen.blit(legend,(625,-15))
        pg.display.flip()
    return kwargs
 
 
@on_start
def loadPickle2(*args,**kwargs):
    kwargs = pickle.load(open("nodegraph.pkl","rb"))
    kwargs['Threads'] = []

    return kwargs
 


class StremeNode:
    def __init__(self):
        pass

    def run(self,*args,**kwargs):
        self.kwargs=simLoop1(**loadPickle2(**kwargs))
        return (self.kwargs)

class liveprocess:
    def __init__(self):
        self.status="pending"
    def run(self,expname):
        self.response=simLoop1(**loadPickle2(**start()))
        self.status="completed"
        return(self.status)

if __name__ == '__main__':
    process = liveprocess()
    process.run('Local')
    