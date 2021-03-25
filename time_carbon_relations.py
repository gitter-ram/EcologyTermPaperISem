import csv
import matplotlib.pyplot as plt
import numpy as np
import mathaux

# Step 1: Extract the climate info and paste it in buffer
carbon5 = []
yrs = []
with open("carbon.csv") as ifs:
    reader  = csv.reader(ifs)
    buff5 = []
    lines = 1
    pomodoro = 1
    for k in reader:
        if lines <= 58:
            lines += 1
            continue
        buff5.append(float(k[4]))
        pomodoro += 1
        if pomodoro % 12 == 0: # On every twelveth month... take the average.
            carbon5.append(sum(buff5)/12)
            buff5 = []
            yrs.append(int(k[0]))
# Neglect 2021 and 1958
yrs = yrs[1:-1]
carbon5 = carbon5[1:-1]
# Neglect 1964 due to insufficient data
target = yrs.index(1964)
del yrs[target]
del carbon5[target]

# Step 2: Extract the Temperatures
temp_avg = []
yrs_clim = []
with open("climate.csv") as src:
    reader = csv.reader(src)
    line = 1
    for k in reader:
        if(line <= 2 or k[15] == "***"): # Ignore the first two lines.
            line += 1
            continue
        if(line == 3):
            D = float(k[12]) # Store the December Temperature of the previous yr
            line += 1
            continue
        line += 1
        yrs_clim.append(int(k[0]))
        avg = 0.0
        # Find the average Temperature for the year
        for i in range(1, 13):
            avg += float(k[i])
        avg = avg / 12
        temp_avg.append(avg)
start = yrs_clim.index(yrs[0])
end = yrs_clim.index(yrs[-1])
fyrs = yrs_clim[start:(end + 1)]
temp_avg = temp_avg[start:(end + 1)]

# Remove the year 1964
tfyrs = fyrs.index(1964)
del fyrs[tfyrs]
del temp_avg[tfyrs]

# Step 3 Plot:

print("-"*10)
print("Maximum CO2 Concentration:", max(carbon5), "Year:", fyrs[carbon5.index(max(carbon5))])
print("Minimum CO2 Concentration:", min(carbon5), "Year:", fyrs[carbon5.index(min(carbon5))])
print("-"*10)

degC = 2
X = np.array(fyrs) - 1959 # Subtract the base year
Yc = np.array(carbon5) # No scaling in the carbon dioxide concentrations.
cvt = np.polyfit(X, Yc, degC)
resC = np.array([mathaux.evalPoly(cvt, k) for k in X])
cPoly = np.array([0.0131, 0.7934, 315.616])
cResC = np.array([mathaux.evalPoly(cPoly, k) for k in X])

plt.plot(fyrs, np.array(carbon5), color="green", linestyle="-", label="Original Data") # Original Data
plt.plot(fyrs, resC, color="red", linestyle="-.", label="The Best Fit Curve") # The best fit curve
plt.plot(fyrs, cResC, color="black", linestyle=":", label="The Curve with rounded coefficients") # Rounded Coefficients curve.
plt.legend(loc="upper left")
plt.title("CO2 levels in the atmosphere vs Time")
plt.xlabel("Time (in Years)")
plt.ylabel("Carbon dioxide concentrations (in ppm)")
plt.show()
print("-----------------------")
print("Relation between time (x) and CO2 Conventration (C):\n\tC = ")
mathaux.printPoly(cvt)
print("----------------------")
errC = mathaux.errorPoly(carbon5, cvt, X, 0, 0)
errC = errC / (max(carbon5) - min(carbon5)) * 100
print("Error in Emperical Relation w.r.t observed values:")
print(errC, "%")
print("-------------------------")
