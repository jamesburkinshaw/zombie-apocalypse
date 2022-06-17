import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as ani

#Set variables
popSizes = [10, 5]
popOffsetsXY = [[0,0],[0,0]]
initialInfections = [10,0]

def createPopulation(ns, offsets, infections):
    popDf = pd.DataFrame()
    
    for i in range(0,len(ns)):
        popIndex = list(range(0,ns[i]))
        popI = pd.DataFrame(np.random.normal(loc=offsets[i][0], size=(ns[i], 1)).round(decimals = 0), index=popIndex, columns=['x']) #x coordinates
        popI['y'] = np.random.normal(loc = offsets[i][1], size=(ns[i], 1)).round(decimals = 0) #y coordinates
        popI['ID'] = list(range(0,ns[i]))
        popI['pop'] = i+1

        #Create Initial Zombies
        if infections[i] > 0:
            initialZombies = popI.sample(n=infections[i]).index.values
            popI.loc[initialZombies, 'pop'] = -1

        popDf = pd.concat([popDf, popI], ignore_index=True)

    return popDf

def printInfected (df):
    print('Total Infected: ' + str(df['pop'][df['pop'] == -1].count()))

#initialise population data frame
#popdf = createPopulation(popSizes, popOffsetsXY, initialInfections)

#test data
popdf = pd.DataFrame(
   {
      "x": [0,0,0,0],
      "y": [1,0,1,0],
      'pop': [1,-1,2,2],
      'ID': [0,1,2,3]
   }
)

printInfected(popdf)

#figure, ax = plt.subplots()
#popPlot = ax.scatter(popdf['x'], popdf['y'], c=popdf['pop'], cmap='Dark2')
#plt.show()

#TODO: Move this to a function + add neighbouring coordinates to zombie locations
zombieLocations = popdf.loc[popdf['pop'] == -1].drop(['pop', 'ID'], axis=1)
infections = popdf.stack().isin(zombieLocations.stack().values).unstack().query('x==True & y==True').index.values
popdf.iloc[infections, popdf.columns.get_loc('pop')] = -1

#random walk
#1 = up, 2 = down, 3 = left, 4 = right
directions = [1, 2, 3, 4]
for i in range(1):
    
    printInfected(popdf)

    #TODO: Move this to a function
    popdf['direction'] = np.random.choice(directions, size=len(popdf), replace=True)

    popdf['y'] = popdf.apply(lambda row: row.y+0.001 if row.direction==1 else row.y, axis=1)
    popdf['y'] = popdf.apply(lambda row: row.y-0.001 if row.direction==2 else row.y, axis=1)
    popdf['x'] = popdf.apply(lambda row: row.x-0.001 if row.direction==3 else row.x, axis=1)
    popdf['x'] = popdf.apply(lambda row: row.x+0.001 if row.direction==4 else row.x, axis=1)


 
