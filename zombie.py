import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime

#Set variables
popSizes = [500,500,500]
popOffsetsXY = [[3,0],[-3,0],[0,3]]
xyscale = [10,10]
initialInfections = [1,0,0]

savePlot = False

def createPopulation(ns, offsets, xyscale, infections):
    popDf = pd.DataFrame()
    
    #create N populations with specified offsets
    for i in range(0,len(ns)):
        popIndex = list(range(0,ns[i]))
        xoffset = offsets[i][0]
        yoffset = offsets[i][1]
        popI = pd.DataFrame((np.random.normal(loc=offsets[i][0], size=(ns[i], 1))*xyscale[0]).round(decimals = 0), index=popIndex, columns=['x']) #x coordinates
        popI['y'] = (np.random.normal(loc = offsets[i][1], size=(ns[i], 1))*xyscale[1]).round(decimals = 0) #y coordinates
        popI['ID'] = list(range(0,ns[i]))
        popI['pop'] = i+1

        #Create Initial Zombies
        if infections[i] > 0:
            initialZombies = popI.sample(n=infections[i]).index.values
            popI.loc[initialZombies, 'pop'] = -1

        popDf = pd.concat([popDf, popI], ignore_index=True)

    return popDf

def printInfected(df):
    print('Total Infected: ' + str(df['pop'][df['pop'] == -1].count()))

def getInfected(df):
    #getExisting zombie locations
    zombieLocations = df.loc[df['pop'] == -1].drop(['pop', 'ID'], axis=1)

    #Get adjacent coordinates
    #       |1|4|6|
    #       |2|X|7|
    #       |3|5|8|
    zombiesCopy = zombieLocations.copy()
    for i in range(1,9):
        adjacentCoords = zombiesCopy.copy()
        #adjacent coords where x changes
        if i == 1 or i == 2 or i == 3:
            adjacentCoords.loc[0:,'x'] = adjacentCoords['x'] -1
        elif i == 6 or i == 7 or i == 8:
            adjacentCoords.loc[0:,'x'] = adjacentCoords['x'] +1
        #adjacent coords where y changes
        if i == 1 or i == 4 or i == 6:
            adjacentCoords.loc[0:,'y'] = adjacentCoords['y'] +1
        elif i == 3 or i == 5 or i == 8:
            adjacentCoords.loc[0:,'y'] = adjacentCoords['y'] -1
        zombieLocations = pd.concat([zombieLocations, adjacentCoords], ignore_index=True)
    zombieLocations = zombieLocations.drop_duplicates(ignore_index = True)

    #find people at the locations where they can be infected and update the population
    infections = df.copy().drop(['pop', 'ID'], axis=1)
    infections = infections.merge(zombieLocations.assign(infected = True),how='left').fillna(False).query('infected == True').index.values
    df.iloc[infections, df.columns.get_loc('pop')] = -1
    
    return df

def randomStep(df):
    #randomly pick direction to take a step in
    #1 = up, 2 = down, 3 = left, 4 = right
    directions = [1, 2, 3, 4]
    popdf['direction'] = np.random.choice(directions, size=len(popdf), replace=True)

    #take step
    df['y'] = df.apply(lambda row: row.y+1 if row.direction==1 else row.y, axis=1)
    df['y'] = df.apply(lambda row: row.y-1 if row.direction==2 else row.y, axis=1)
    df['x'] = df.apply(lambda row: row.x-1 if row.direction==3 else row.x, axis=1)
    df['x'] = df.apply(lambda row: row.x+1 if row.direction==4 else row.x, axis=1)

    return df.drop('direction', axis=1)

#initialise population data frame
popdf = createPopulation(popSizes, popOffsetsXY, xyscale, initialInfections)
progress = pd.DataFrame(columns=['step', 'infected'])

#test data
#popdf = pd.DataFrame(
#   {
#      "x": [0,4,0,0,4],
#      "y": [1,3,1,0,4],
#      'pop': [1,-1,2,2,-1],
#      'ID': [0,1,2,3,4]
#   }
#)

step = 0
currentProgress= pd.DataFrame(data = {'step':[step], 'infected':[popdf['pop'][popdf['pop'] == -1].count()]})

#initial plot
plt.ion()
figure, ax = plt.subplots(figsize=(10, 10))
scatter = ax.scatter(popdf['x'], popdf['y'], c=popdf['pop'], cmap='jet' )
plt.title('Step ' + str(step) + ' ' + str(popdf['pop'][popdf['pop'] == -1].count()) + ' Infected ')
plt.show()

startTime = datetime.now()

#walk until everyone is zombified
while True:

    print('Step ' + str(step))
    printInfected(popdf)
    
    #check for infected
    popdf = getInfected(popdf)

    #update plot
    plt.pause(0.05)
    ax.cla()
    scatter = ax.scatter(popdf['x'], popdf['y'], c=popdf['pop'], cmap='jet')
    plt.title('Step ' + str(step) + ' ' + str(popdf['pop'][popdf['pop'] == -1].count()) + ' Infected ')
    plt.draw()

    #take a step
    popdf = randomStep(popdf)
    step = step + 1

    if savePlot:
        plt.savefig('C:\\Users\\jzburkinshaw\\Documents\\Zombie Figs\\fig' + str(step) + '.png')
        ax.cla()

    #Python should have do while loops
    if popdf['pop'][popdf['pop'] == -1].count() == len(popdf):
        break

endTime = datetime.now()
duration = endTime - startTime

print('Start Time: ' + str(startTime) + ' End Time: ' + str(endTime) + ' Duration: ' + str(duration))
#print(progress)
