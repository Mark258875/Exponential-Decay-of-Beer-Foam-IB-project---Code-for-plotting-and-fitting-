# **Code for PLOTTING and FITTING the Exponential Decay of Beer Foam (IB project)**

## Usage:

### plotPoints.py 
  An interactive way for plotting the data.

`python plotPoints.py -f beer1.csv beer2.csv beer3.csv`

  If you want the points to be connected, in the code change the     plt.scatter TO plt.plot

### plotSaveGraph.py
  Plots the data - exponential

  `python plotSaveGraph.py -f beer1.csv`
  `python plotSaveGraph.py -f beer1.csv -c`  This option connects the lines

### scaledLNY.py 
  Plots the logaritmically SCALED (ln(y)) original exponential data => can be fitted on the line

  `python scaledLNY.py -f beer1.csv`
  `python scaledLNY.py -f beer1.csv -l "ax+b"`  Option to fit the linear function + show statistics 
  
