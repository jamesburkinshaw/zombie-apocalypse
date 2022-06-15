import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as ani

def createPopulation(n, xOffset, yOffset, infected):
    print("Hello from a function")

#Set variables
#TODO: generate populations based on these variables
popSizes = [10, 10]
popOffsetsXY = [[3,0],[-3,0]]
initialInfections = [1,0]

pop1Size = 10
pop2Size = 10

initialInfections = 1

#initialise population data frames
popAIndex = list(range(0,pop1Size))
pop1df = pd.DataFrame(np.random.normal(loc=-3, size=(pop1Size, 1)), index=popAIndex, columns=['x']) #x coordinates
pop1df['y'] = np.random.normal(size=(pop1Size, 1)) #y coordinates
pop1df['pop'] = 1

popBIndex = list(range(0,pop2Size))
pop2df = pd.DataFrame(np.random.normal(loc=3, size=(pop2Size, 1)), index=popAIndex, columns=['x']) #x coordinates
pop2df['y'] = np.random.normal(size=(pop2Size, 1)) #y coordinates
pop2df['pop'] = 2

#infect n people form pop 1
initialZombies = pop1df.sample(n=initialInfections).index.values
#print(initialZombies)
pop1df.loc[initialZombies, 'pop'] = 3

#combine populations
popdf = pd.concat([pop1df, pop2df], ignore_index=True)

figure, ax = plt.subplots()
popPlot = ax.scatter(popdf['x'], popdf['y'], c=popdf['pop'], cmap='Dark2')
#plt.show()

#print(popdf)

#random walk
#1 = up, 2 = down, 3 = left, 4 = right
directions = [1, 2, 3, 4]
for i in range(1):
    
    print('Total Infected: ' + str(popdf['pop'][popdf['pop'] == 3].count()))

    popdf['direction'] = np.random.choice(directions, size=len(popdf), replace=True)

    popdf['y'] = popdf.apply(lambda row: row.y+1 if row.direction==1 else row.y, axis=1)
    popdf['y'] = popdf.apply(lambda row: row.y-1 if row.direction==2 else row.y, axis=1)
    popdf['x'] = popdf.apply(lambda row: row.x-1 if row.direction==3 else row.x, axis=1)
    popdf['x'] = popdf.apply(lambda row: row.x+1 if row.direction==4 else row.x, axis=1)
 
