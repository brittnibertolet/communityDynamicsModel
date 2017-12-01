#import packages
import os
import numpy as np
import pandas as pd
import scipy
import sklearn
import scipy.integrate as spint
from plotnine import *
import matplotlib.pyplot as plt

#Define a custom function for Lotka Volterra model
def LVSim(y,t0,b,a,e,s):
    #unpack state variables from list y
    H=y[0]
    P=y[1]
    #calculate changes in state variables
    dHdt=(b*H)-(a*P*H)
    dPdt=(e*a*P*H)-(s*P)
    #return lists containing changes in state variables with time
    return [dHdt,dPdt]
    
#Define initial values for state variables
H0=25
P0=5
N0=[H0,P0]

#Define parameters in dataframe
##define intial values make lists
b=0.5
a=0.02
e=0.1
s=0.2
##define multiple to reduce/increase parameters
m=1.5

#Make list of each parameter and whether or not it changes
b=[b,b/m,b*m,b,b,b,b,b,b]
a=[a,a,a,a/m,a*m,a,a,a,a]
e=[e,e,e,e,e,e/m,e*m,e,e]
s=[s,s,s,s,s,s,s,s/m,s*m]
##Lists to data frame and rearrange order of columns and make to list
parameters=pd.DataFrame({'b':b, 'a':a, 'e':e, 's':s})
parameters=parameters[['b','a','e','s']]
parameters=parameters.values.tolist()

#Define time steps
times=np.arange(0,75,0.1)

#Create data frame for function output and fill with time values in first column
modelH_Output=pd.DataFrame(columns=["t", "H", "bHlow", "bHhigh", "aHlow", "aHhigh", "eHlow", "eHhigh", "sHlow", "sHhigh"])
modelP_Output=pd.DataFrame(columns=["t", "P", "bPlow", "bPhigh", "aPlow", "aPhigh", "ePlow", "ePhigh", "sPlow", "sPhigh"])
modelH_Output.t=times
modelP_Output.t=times

#Simulate the model
i=1
for i in range(0,len(parameters)):
    #set paramters for the iteration
    params=parameters[i]
    #run siumulation with odeint
    modelSim=spint.odeint(func=LVSim,y0=N0,t=times,args=tuple(params))
    #convert output from array to data frame
    modelSim=pd.DataFrame(data=modelSim)
    #add results to model output data frame
    modelH_Output.iloc[:, i+1]=modelSim[0]
    modelP_Output.iloc[:, i+1]=modelSim[1]

#Graph results manually from model output 
##plot of prey counts vs time, in which only paramter b is changing -- solid: initial b value, dotted: lower b value, dashed: higher b value
plot_Hb=ggplot(modelH_Output,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="bHlow"), color='blue', linetype='dotted')+geom_line(aes(y="bHhigh"), color='blue', linetype='dashed')+ggtitle("Different b values")+ylab("Prey counts")+xlab("Time")+theme_bw()
##plot of predator counts vs time, in which only paramter b is changing -- solid: initial b value, dotted: lower b value, dashed: higher b value
plot_Pb=ggplot(modelP_Output,aes(x="t"))+geom_line(aes(y="P"), color='red')+geom_line(aes(y="bPlow"), color='red', linetype='dotted')+geom_line(aes(y="bPhigh"), color='red', linetype='dashed')+ggtitle("Different b values")+ylab("Predator counts")+xlab("Time")+theme_bw()

###same as above, now only parameter a is changing
plot_Ha=ggplot(modelH_Output,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="aHlow"), color='blue', linetype='dotted')+geom_line(aes(y="aHhigh"), color='blue', linetype='dashed')+ggtitle("Different a values")+ylab("Prey counts")+xlab("Time")+theme_bw()
plot_Pa=ggplot(modelP_Output,aes(x="t"))+geom_line(aes(y="P"), color='red')+geom_line(aes(y="aPlow"), color='red', linetype='dotted')+geom_line(aes(y="aPhigh"), color='red', linetype='dashed')+ggtitle("Different a values")+ylab("Predator counts")+xlab("Time")+theme_bw()
###same as above, now only parameter e is changing
plot_He=ggplot(modelH_Output,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="eHlow"), color='blue', linetype='dotted')+geom_line(aes(y="eHhigh"), color='blue', linetype='dashed')+ggtitle("Different e values")+ylab("Prey counts")+xlab("Time")+theme_bw()
plot_Pe=ggplot(modelP_Output,aes(x="t"))+geom_line(aes(y="P"), color='red')+geom_line(aes(y="ePlow"), color='red', linetype='dotted')+geom_line(aes(y="ePhigh"), color='red', linetype='dashed')+ggtitle("Different e values")+ylab("Predator counts")+xlab("Time")+theme_bw()
###same as above, now only parameter s is changing
plot_Hs=ggplot(modelH_Output,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="sHlow"), color='blue', linetype='dotted')+geom_line(aes(y="sHhigh"), color='blue', linetype='dashed')+ggtitle("Different s values")+ylab("Prey counts")+xlab("Time")+theme_bw()
plot_Ps=ggplot(modelP_Output,aes(x="t"))+geom_line(aes(y="P"), color='red')+geom_line(aes(y="sPlow"), color='red', linetype='dotted')+geom_line(aes(y="sPhigh"), color='red', linetype='dashed')+ggtitle("Different s values")+ylab("Predator counts")+xlab("Time")+theme_bw()

#Show all plots
print(plot_Hb)
print(plot_Pb)
print(plot_Ha)
print(plot_Pa)
print(plot_He)
print(plot_Pe)
print(plot_Hs)
print(plot_Ps)



