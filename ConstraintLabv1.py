#!/usr/bin/env python
# coding: utf-8

# ### Constraint Satisfaction Lab
# 
# <span style="color:red">Your name here: Jordan Gropper</span>
# 
# <span style="color:red">THIS LAB IS COMPLETE</span>
# 
# Notice that you are delivering four functions, but your submitted notebook does not call the functions.  Please do "Restart Kernel and Clear Output" prior to submitting.  If I then "Run All" on your notebook, I should see *no* output.  I will put the code to run your functions at the end of the notebook when I grade it.

# #### Map Coloring
# 
# * There a N locations, each with a name
# * There are k colors
# * There is a set of adjacency relationships between the locations
# * The goal is to assign a color to each locations such that no two adjacent locations have the same color
# 

# Use the constraint library to solve this problem:
# 
# ![test](mapColorWesternUS.GIF)
# 
# Your solution should be in a function solveWesternStates(), and it should produce a single solution if one exists, delivered as a dictionary mapping a state name to its assigned color.  For example the picture above is a solution which would look like:
# ```
# {'WA': 'green', 'OR': 'yellow', 'ID': 'red', 'CA': 'blue', 'NV', 'green', 
#  'UT': 'blue', 'AZ': 'red', 'CO': 'yellow', 'NM': 'blue'}
# ```
# Your function does not need to return that solution -- if there is more than one solution, your function may return any of them.  Your function should return ```None``` if there is no solution (but of course there is a solution because the diagram shows one!).  Still, add the code checking for no solutions, just to be tidy.

# In[1]:


colors = ["green", "yellow", "blue", "red"]
conflicts = {'WA':['OR', 'ID'],
             'OR':['WA', 'ID', 'NV', 'CA'],
             'ID':['WA', 'OR', 'NV', 'UT'],
             'NV':['OR', 'ID', 'UT', 'CA', 'AZ'], 
             'UT':['CO', 'AZ', 'NV', 'ID'],
             'CA':['OR', 'NV', 'AZ'],
             'AZ':['CA', 'NV', 'UT', 'NM'], # NV?
             'NM':['CO', 'AZ'],
             'CO':['UT', 'NM']           
            }

## Jordan: Setting up these conflicts was relatively straight forward, no more info needed.


# In[2]:


#  Your definition of the function ```solveWesternStates()``` in this cell.  Notice this is a function, your
#  notebook should not call the function, just define it.
from constraint import *

colors = ["green", "yellow", "blue", "red"]
conflicts = {'WA':['OR', 'ID'],
             'OR':['WA', 'ID', 'NV', 'CA'],
             'ID':['WA', 'OR', 'NV', 'UT'],
             'NV':['OR', 'ID', 'UT', 'CA', 'AZ'], 
             'UT':['CO', 'AZ', 'NV', 'ID'],
             'CA':['OR', 'NV', 'AZ'],
             'AZ':['CA', 'NV', 'UT', 'NM'], # NV?
             'NM':['CO', 'AZ'],
             'CO':['UT', 'NM']           
            }


def solveWesterStates(colors, conflicts):
    #
    problem = Problem()

    for state in conflicts.keys():
        problem.addVariable(state, colors) # every state can initially be any color
    
    for state in conflicts.keys():
        for conflictingState in conflicts[state]:
            problem.addConstraint(lambda a, b: a != b, [state, conflictingState])
            
    solutions = problem.getSolutions()
    if solutions == []:
        print('None')
        return None
    else:
        return solutions[0] # to get just the first single dictionary solution
    
## Jordan: Setting this up was almost exactly as the examples, very reasonable.


# In[3]:


#solveWesterStates(colors, conflicts) # tons of solutions
# graying this out so it doesn't run, as instructed in the lecture. 
# OUTPUT:
#{'NV': 'red',
# 'AZ': 'blue',
# 'UT': 'yellow',
# 'ID': 'blue',
# 'OR': 'yellow',
# 'CA': 'green',
# 'WA': 'red',
# 'CO': 'red',
# 'NM': 'yellow'}


# What is the minimum number of colors required to color this map?  Write a function ```westernStatesMinColors()``` that returns the minimum number of colors required to color the map.
# THE ANSWER IS 4

# In[4]:


##  Your definition of the function ```westernStatesMinColors()``` in this cell.  Notice this is a function, your
##  notebook should not call the function, just define it.
from constraint import *

colors = ["green", "yellow", "blue", "red"]
conflicts = {'WA':['OR', 'ID'],
             'OR':['WA', 'ID', 'NV', 'CA'],
             'ID':['WA', 'OR', 'NV', 'UT'],
             'NV':['OR', 'ID', 'UT', 'CA', 'AZ'], 
             'UT':['CO', 'AZ', 'NV', 'ID'],
             'CA':['OR', 'NV', 'AZ'],
             'AZ':['CA', 'NV', 'UT', 'NM'], # NV?
             'NM':['CO', 'AZ'],
             'CO':['UT', 'NM']           
            }


def solveWesterStates(colors, conflicts):
    #
    problem = Problem()

    for state in conflicts.keys():
        problem.addVariable(state, colors) # every state can initially be any color
    
    for state in conflicts.keys():
        for conflictingState in conflicts[state]:
            problem.addConstraint(lambda a, b: a != b, [state, conflictingState])
            
    solutions = problem.getSolutions()
    if solutions == []:
        print('None')
        return None
    else:
        return solutions[0]


def westernStatesMinColors(colors, conflicts):
    for i in range(len(colors)):
        #print(colors[i:])
        new_colors = colors[i:]
        len_new_colors = len(new_colors)
        answer = solveWesterStates(new_colors, conflicts)
        if answer == None:
            print('The minimum number of colors is:', (len(new_colors)+1))
            return (len(new_colors)+1)
        
## Jordan: I see that the solution has a VERY clever route of calculting the minimum number that
## is slightly more efficient than mine, but it is the same concept. Maybe tell the students
## to utilize what they have already built (as a hint), as I tried to rebuild the wheel on this one
## before realizing a better option. 


# In[5]:


#westernStatesMinColors(colors, conflicts) OUTPUTS 4!
# graying this out so it doesn't run, as instructed in the lecture. 


# ----------------------------------------------------------------------

# #### Simple Job-Shop Scheduling
# 
# * Job 1 has two tasks:  polishing and drilling
# * Job 2 has two tasks: painting and drilling
# * Painting has to be done before drilling for any given part
# * Polishing and drilling can be done in either order
# * You cannot do two operations of the same job at the same time
# * Painting requires the painting machine and an attendant
# * Polishing requires the polishing machine and an attendant
# * There is only one attendant
# * If the shop starts at time 0 and each task takes 1 time unit, at what times should the tasks begin?
# 
# Your function will be ```solveJobShop()``` which will return a dictionary with the times at which each task should be begun.  The tasks will be named ```'polishing1', 'drilling1', 'painting2' and 'drilling2'```.  Here is an example dictionary, just to illustrate the format of the solution.  It is not a valid solution so don't try to duplicate this output!
# ```
# {'polishing1': 0,  'drilling1': 1, 'drilling2': 1, 'painting2': 2}
# ```

# In[6]:


#  Your definition of the function ```solveJobShop()``` in this cell.  Notice this is a function, your
#  notebook should not call the function, just define it.
from constraint import *
times = [0,1]#,2,3,4,5,6,7,8,9,10]  # barely any periods needed

tasks = ['polishing1', 'drilling1', 'drilling2', 'painting2']

#conflicts = {'polishing1': ['painting2'], # polishing cannot be done at the same time as painting
#            'drilling1': [], # can be done in any order
#            'drilling2': [], # can be done in any order
#            'painting2': ['drilling1', 'drilling2']}


def solveJobShop(tasks, conflicts, times):
    problem = Problem()
    
    
    for tas in tasks:
            problem.addVariable(tas, times)

    #for tas in tasks:
     #   for conflictingTasks in conflicts[tas]:
     #       if conflicts[tas] != []:
     #           problem.addConstraint(lambda a, b: a < b, [tas, conflictingTasks]) 
                # a must come before b
    conflicts = {"polishing1":"drilling1",
                "painting2":"drilling2"
                }
    for i in conflicts.keys():
        print(i)
        problem.addConstraint(lambda a, b: a != b, [i, conflicts[i]])
        
    problem.addConstraint(lambda a, b: a < b, ["painting2", "drilling2"])
    for p in [("painting2", "polishing1"), ("drilling1", "drilling2")]:
        problem.addConstraint(lambda a, b: a != b, p)
    
    
    soln = problem.getSolutions()
    return problem.getSolutions() # soln[0] # to get only 1 response
    
## Jordan: This one is slightly more difficult, but still really cool. I would recommend letting the 
## students know that they can still iterate through the conflicts, but that the "before" and
## the attendant restriction add another layer that should be plainly type out. Additionally,
## Giving the hint that these 4 tasks can be done in less periods than 4 would also be helpful


# In[7]:


#solveJobShop(tasks, conflicts, times)
# graying this out so it doesn't run, as instructed in the lecture. 


# ----------------------------------------------------------------------

# #### The Zoo in Killian Court
# 
# (This is from an old MIT problem set.)
# 
# MIT has decided to open a new zoo in Killian Court. They have obtained seven
# animals and built four enclosures. Because there are more animals than enclosures, some animals
# have to be in the same enclosures as others. However, the animals are very picky about who they live
# with. The MIT administration is having trouble assigning animals to enclosures, just as they often have
# trouble assigning students to residences. They have asked you to plan where
# each animal goes.
# 
# The animals chosen are a LION, ANTELOPE, HYENA, EVIL LION, HORNBILL, MEERKAT, and BOAR.
# 
# ![Zoo](zoo.GIF)
# 
# Each numbered area is a zoo enclosure. Multiple animals can go into the same enclosure, and not all
# enclosures have to be filled.
# 
# Each animal has restrictions about where it can be placed.
# 
# 1. The LION and the EVIL LION hate each other, and do not want to be in the same enclosure.
# 1. The MEERKAT and BOAR are best friends, and have to be in the same enclosure.
# 1. The HYENA smells bad. Only the EVIL LION will share his enclosure.
# 1. The EVIL LION wants to eat the MEERKAT, BOAR, and HORNBILL.
# 1. The LION and the EVIL LION want to eat the ANTELOPE so badly that the ANTELOPE cannot be
# in either the same enclosure or in an enclosure adjacent to the LION or EVIL LION.
# 1. The LION annoys the HORNBILL, so the HORNBILL doesn't want to be in the LION's enclosure.
# 1. The LION is king, so he wants to be in enclosure 1.
# 
# Write a function ```solveZoo()``` that produces a dictionary assigning animals to enclosures.  It should return just 1 solution, and None if no solution exists.  The animal names are defined below.  Enclosure numbers are 1, 2, 3, 4.

# In[8]:


animals = ["Lion", "Antelope", "Hyena", "EvilLion", "Hornbill", "Meerkat", "Boar"]


# In[9]:


##  Your definition of the function ```solveZoo()``` in this cell.  Notice this is a function, your
##  notebook should not call the function, just define it.
from constraint import *

animals = ["Lion", "Antelope", "Hyena", "EvilLion", "Hornbill", "Meerkat", "Boar"]

enclosures = [1, 2, 3, 4]
adjacent_enclosures = [(1,2), (2,1), (2,3), (3,2), (3,4), (4,3)]

haveToBeWith = {"Meerkat":["Boar"],
                "Boar":["Meerkat"],
                "Hyena":["EvilLion"],
                "EvilLion":["Hyena"]
            }

conflicts = {"Lion": ["EvilLion", "Hornbill", "Hyena"],
            "Antelope": ["Hyena"],
            "Hyena": ["Lion", "Antelope", "Hyena", "Hornbill", "Meerkat", "Boar"],
            "EvilLion": ["Lion", "Meerkat", "Boar", "Hornbill"],
            "Hornbill": ["Lion","Hyena", "EvilLion"],
            "Meerkat": ["Hyena", "EvilLion"],
            "Boar":["Hyena", '', "EvilLion"],
            }

initials = {"Lion": 1} #

# need to combine the ClassProf example with  solveMagicSquare

def solveZoo(animals, enclosures, haveToBeWith, conflicts, initials):
    problem = Problem() 
    
    def mustShare(animal):
        #print('must share', animal)
        #print([p for p in haveToBeWith.keys() if animal in haveToBeWith[p]])
        return [p for p in haveToBeWith.keys() if animal in haveToBeWith[p]]
    
    
    for animal in animals:
        if animal in initials.keys():
            problem.addVariable(animal, [initials[animal]])            
        else:
            problem.addVariable(animal, enclosures)
    
    problem.addConstraint(lambda a,b: (a,b) not in adjacent_enclosures, ["Lion", "Antelope"] )
    problem.addConstraint(lambda a,b: (a,b) not in adjacent_enclosures, ["EvilLion", "Antelope"] )
    problem.addConstraint(lambda a,b:  a != b, ["Lion", "Antelope"] )
    problem.addConstraint(lambda a,b:  a != b, ["EvilLion", "Antelope"] )
    
    for animal in animals:
        for conflictingAnimals in conflicts[animal]:
            if mustShare(animal) != []:
                problem.addConstraint(lambda a, b: a == b, [animal, mustShare(animal)[0]])
                print(animal, 'must =', mustShare(animal)[0])
            else:
                print(animal, 'cant =', conflictingAnimals)
                problem.addConstraint(lambda a, b: a != b, [animal, conflictingAnimals])
    solution = problem.getSolutions()
    return solution[0]

## Jordan: I did not think to add an adjacencies object to make this problem easier to solve.
## I would definitely hint that "giving the function an item that recognizes which enclosures
## are next to is very useful". Beyond that, I was able to use the same loop system I had intended,
## which sorted through the conflicgtgs. But it may be worth noting that looping isn't necessary,
## and students can just spell it out line by line 


# In[10]:


#solveZoo(animals, enclosures, haveToBeWith, conflicts, initials)
# graying this out so it doesn't run, as instructed in the lecture. 

