import numpy as np
import pandas as pd
from matplotlib import pyplot
from scipy import optimize as op
import math

#Pre Process the Data

df = pd.read_csv('./data/04_cricket_1999to2011.csv')
df = df[df['Innings']==1]
df.Over=50-df.Over
req_col=['Over','Innings.Total.Runs','Total.Runs','Wickets.in.Hand']
df = df.filter(items=req_col)
rows=len(df)

def loss(Z,df):
    L=Z[10]
    mse=0
    for w in range(1,11):
        df2 = df[df['Wickets.in.Hand']==w]
        Run = df2['Innings.Total.Runs']-df2['Total.Runs']
        
        z = Z[w-1]*np.subtract(1,np.exp(np.multiply(-1*L/Z[w-1],df2['Over'])))
        mse+=np.sum(np.square(np.subtract(Run,z)))
    mse=mse/rows
    return mse

def DLS():
    x0=[11.6664,26.8078,50.6184,78.5794,103.9465,137.6539,168.8422,207.5715,239.1373,284.2157,10.8822]
    mse = 0
    a=op.minimize(loss,x0=x0,args=(df))
    Z = a.x[0:10]
    L = a.x[10]
    for w in range(1,11):
        df2 = df[df['Wickets.in.Hand']==w]
        Run = df2['Innings.Total.Runs']-df2['Total.Runs']
        z = Z[w-1]*np.subtract(1,np.exp(np.multiply(-1*L/Z[w-1],df2['Over'])))
        mse=np.sum(np.square(np.subtract(Run,z)))
        
    mse=mse/rows
    return Z,L,mse,a.fun

def plot(Z,L):
    y=np.zeros((10,51))
    for w in range(0,10):
        x = range(0,51)
        
        for u in range(0,51):
            y[w][u]= Z[w]*(1-math.exp(-1*L*u/Z[w]))
        
    for w in range(0,10):
        pyplot.plot(x,y[w],label=f"w={w+1}")
        pyplot.xlabel('Overs Remaining')
        pyplot.ylabel("Runs")
        pyplot.legend()
    pyplot.show()

if __name__ == '__main__':
    Z0,L,mse,e = DLS()
    plot(Z0,L)
    print('Wickets in Hand\t\tZ0')
    for i in range(10):
        print(f'{i+1}\t\t\t{Z0[i]:.4f}')
        
    print(f'\n\nL: {L:.4f}\t\t Normalized Error: {mse:.4f}')
    


