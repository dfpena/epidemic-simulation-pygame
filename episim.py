
#!/usr/bin/env python
from decorator import decorator

import pandas as pd
import random
import numpy as np
import pickle
import time
import seaborn as sns
import pygame.gfxdraw as gfx
import matplotlib.pyplot as plt
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

 
@on_start
def loadPickle_node_27(*args,**kwargs):
    kwargs = pickle.load(open("nodegraph40000.pkl","rb"))
    kwargs['Threads'] = []

    return kwargs
 
def remap(narray,resolution):
    x = np.interp(narray[0],[-1,1],[15,resolution[0]-15])
    y = np.interp(narray[1],[-1,1],[50,resolution[1]- 15])
    return np.array([int(x),int(y)])


@on_start
def simLoop_node_28(*args, **kwargs):
############################## EDIT THESE PARAMETERS ########################
    inflength = 20
    mortality = 0.16
    rnaught = 0
    infprob = 0.08
    infincubation=5
    infdetected = 10
#############################################################################

    if infprob == 0:
        infprob = rnaught/(kwargs['Settings']['NetworkX']['k']*inflength)
    if rnaught == 0:
        rnaught = infprob*kwargs['Settings']['NetworkX']['k']*inflength
    
    pos = kwargs['Settings']['NetworkX']['Pos']
    #rng = default_rng()
    #initialinf = rng.choice(21*2, size=21, replace=False)
    initialinf = random.sample(range(21*2),21)

    G = kwargs['Data']
    screensize = (800,800)
    G.graph['colors'] = {"Naive":(99, 7, 238),"Infected Symptomatic":(145, 238, 7),"Infected Asymptomatic":(159, 190, 126),"Immune":(255, 235, 59),"Dead":(239, 99, 7)}
    G.graph['disease'] = {"Infection Probability" : infprob,"Infection Detection":infdetected, "Infection Length" : inflength, "Incubation Length":infincubation, "Mortality": mortality}
    # Add Parameters to Nodegraph
    for nid in G:
        G.nodes[nid]['Status'] = 'Naive'
        G.nodes[nid]['Day'] = 0
    # Remap -1 1 square to  pygame resolution
    for nid in pos:
        pos[nid] = remap(pos[nid],screensize) 
    for nid in initialinf:
        G.nodes[nid]['Status'] = 'Infected Asymptomatic'
    # initialize the pygame module
    pg.init()
    # load and set the logo
    #logo = pg.image.load("logo.png")
    #pg.display.set_icon(logo)
    pg.display.set_caption("Novel coronavirus (2019-nCoV) Wuhan Virus China")
    legend = pg.image.load('legend.png')
     
    # create a surface on screen that has the size of 240 x 180
    screen = pg.display.set_mode(screensize)
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((236, 239, 241))
    
    green = (255, 255, 255) 
    deaths = 0
    infected = 21
    asymptomatic=21
    symptomatic=0 
    willdie=0
    infday = 0 
    detected = 0
    immune = 0 
    datacontainer={"Day":[],"Deaths":[],"Cumulative Infections":[],"Detected Infections":[],"Current Asymptomatic Infections":[],"Current Infectious Carriers":[]}
    font = pg.font.Font(pg.font.match_font('lato'), 20)
    text = font.render('R0: {0}'.format(rnaught), True, green)
    textinfected = font.render('Infected: {0}'.format(infected), True, green)
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        #infected = 0
############################### STOP CRITERIA ########################################################
#        if infday >= 6:
#            running = False
#        totaldetected = infected - (asymptomatic+immune+deaths)
#        if detected >= 2:
#            running = False
        if deaths >=56:
            running = False
            
#######################################################################################################

        screen.blit(background, (0, 0))
        pg.draw.rect(background,(74,20,140),(0,0,screensize[0],120),0)

        textdeath = font.render('Deaths: {}'.format(deaths), True, green)
        screen.blit(textdeath, (10,10))
        textinfected = font.render('Cumulative Infections: {}'.format(infected), True, green)
        screen.blit(textinfected, (10,25))
        
        textinfected = font.render('Recoveries: {}'.format(immune), True, green)
        screen.blit(textinfected, (10,55))
        textinfected = font.render('Naive: {}'.format(kwargs['Settings']['NetworkX']['nodes']-infected), True, green)
        screen.blit(textinfected, (10,40))
        #totaldetected = infected - (asymptomatic+immune+deaths)
        textsymptomatic = font.render('Cumulative Detected Infections: {}'.format(detected), True, green)
        screen.blit(textsymptomatic, (10,70))
        
        textasymptomatic = font.render('Current Asymptomatic Infections: {}'.format(asymptomatic), True, green)
        screen.blit(textasymptomatic, (10,85))
        carriers = infected-asymptomatic-detected
        textcarriers = font.render('Current Infectious Carriers: {}'.format(carriers), True, green)
        screen.blit(textcarriers, (10,100))
        
        textdays = font.render('Epidemic Day: {}'.format(infday), True, green)
        screen.blit(textdays, ((screensize[0]/2)-40,10))
        textrnaught = font.render('R0: {}'.format(rnaught), True, green)
        screen.blit(textrnaught, ((screensize[0]/2)-40,25))
        
        textmortality = font.render('Mortality Rate: {} %'.format(mortality*100), True, green)
        screen.blit(textmortality, ((screensize[0]/2)+40,25))
        datacontainer['Day'].append(infday)
        datacontainer['Deaths'].append(deaths)
        datacontainer['Cumulative Infections'].append(infected)
        datacontainer['Detected Infections'].append(detected)
        datacontainer['Current Asymptomatic Infections'].append(asymptomatic)
        datacontainer['Current Infectious Carriers'].append(carriers)
        
        for nid in pos:
            for e in G.edges(nid):
                cnode= e[1]
                gfx.line(screen,pos[nid][0],pos[nid][1],pos[cnode][0],pos[cnode][1],(120,144,156))
        for nid in pos:
            color = G.graph['colors'][G.nodes[nid]['Status']]
            gfx.aacircle(screen, pos[nid][0],pos[nid][1], 6, color)
            gfx.filled_circle(screen, pos[nid][0],pos[nid][1], 6, color)
            
            if G.nodes[nid]['Day'] == G.graph['disease']['Infection Detection']:
                detected = detected + 1    
            if G.nodes[nid]['Status'] == "Infected Symptomatic":
                if G.nodes[nid]['Day'] == G.graph['disease']["Infection Length"]:
                    roll = random.random()
                    if roll >= G.graph['disease']['Mortality']:
                        G.nodes[nid]['Status'] = "Immune"
                        immune = immune+1
                        symptomatic = symptomatic-1
                    if roll < G.graph['disease']['Mortality']:
                        G.nodes[nid]['Status'] = "Dead"
                        symptomatic = symptomatic-1
                        deaths=deaths+1
                G.nodes[nid]['Day'] = G.nodes[nid]['Day'] + 1
                for e in G.edges(nid):
                    cnode = e[1]
                    if G.nodes[cnode]['Status'] != "Dead": 
                        if G.nodes[cnode]['Status'] != "Immune":
                            if G.nodes[cnode]['Status'] != "Infected Asymptomatic":
                                if G.nodes[cnode]['Status'] != "Infected Symptomatic":
                                    roll = random.random()
                                    
                                    if roll < G.graph['disease']['Infection Probability']:
                                        G.nodes[cnode]['Status'] = 'Infected Asymptomatic'
                                        infected = infected+1
                                        asymptomatic = asymptomatic+1
                                
                                
            if G.nodes[nid]['Status'] == "Infected Asymptomatic":
                if G.nodes[nid]['Day'] >= G.graph['disease']["Incubation Length"]:
                    asymptomatic = asymptomatic-1
                    symptomatic = symptomatic+1
                    G.nodes[nid]['Status'] = "Infected Symptomatic"
                G.nodes[nid]['Day'] = G.nodes[nid]['Day'] + 1 
        
    # event handling, gets all event from the event queue
        for event in pg.event.get():
    # only do something if the event is of type QUIT
            if event.type == pg.QUIT:
    # change the value to False, to exit the main loop
                running = False
        infday = infday + 1
        
        screen.blit(legend,(625,-15))
        pg.display.flip()
    time.sleep(10)
    df=pd.DataFrame(datacontainer)
    print(df)
    df = df[['Deaths','Detected Infections','Cumulative Infections','Current Asymptomatic Infections','Current Infectious Carriers']].rolling(1).sum()
    #sns.barplot(x = 'Day', y = 'Cumulative Infections', data = df)
    #sns.barplot(x = 'Day', y = 'Detected Infections', palette = 'magma', data = df)
    sns.lineplot(data=df, linewidth=2)


    plt.show()
    df.to_excel('summarydataChina.xlsx')
    kwargs['Data'] = df
    return kwargs
 
 


class StremeNode:
    def __init__(self):
        pass

    def run(self,*args,**kwargs):
        self.kwargs=simLoop_node_28(**loadPickle_node_27(**kwargs))
        return (self.kwargs)

class liveprocess:
    def __init__(self):
        pass
        
    def run(self,expname="Local"):
        self.response=simLoop_node_28(**loadPickle_node_27(**start()))
        return(self.response)

if __name__ == '__main__':
    process = liveprocess()
    process.run()
    