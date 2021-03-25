import csv
import matplotlib.pyplot as plt
import numpy as np
import mathaux


# Step 1: Parsing the data
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
start = yrs_clim.index(1959)
end = yrs_clim.index(2020)
fyrs = yrs_clim[start:(end + 1)]
temp_avg = temp_avg[start:(end + 1)]
# Remove the year 1964
tfyrs = fyrs.index(1964)
del fyrs[tfyrs]
del temp_avg[tfyrs]
# Step 2: Obtain the relations:
degK = 4
offset = min(temp_avg)
sf = 5
Yk = (np.array(temp_avg) - offset) * (10 ** sf) # Scale the temperature
X = np.array(fyrs) - 1959 # Scale the time
kvt = np.polyfit(X, Yk, degK) # Scaled relation
resT = np.array([(mathaux.evalPoly(kvt, k) / (10 ** sf)) + offset for k in X])

statC= input("Do you want to see the statistical data?(Press Enter for Yes, press something and press enter for no.")
if not statC:
    print("Maximum Temperature:", max(temp_avg), "Year:", fyrs[temp_avg.index(max(temp_avg))])
    print("Minimum Temperature:", min(temp_avg), "Year:", fyrs[temp_avg.index(min(temp_avg))])

cust_poly = np.array([0.0395, -5.0125, 224.5691, -2422.1062, 15234.8075]) # The Rounded of Coefficients.
res_cust = np.array([(mathaux.evalPoly(cust_poly, k) / (10 ** sf)) + offset for k in X])

# Step 3 : Plots
plt.plot(fyrs, np.array(temp_avg), color="green", label="Original Data") # Original Data
plt.plot(fyrs, resT, color="red", linestyle="-.", label="The Best Fit Curve") # The estimated curve.
plt.plot(fyrs, res_cust, color="blue", label="Rounded Off Coefficient Curve", linestyle="-.")
plt.legend(loc="upper left")
plt.title("Average Temperature Anomaly vs Time")
plt.xlabel("Time (in Years)")
plt.ylabel("Average Temperature Anomaly (in K)")
plt.show()

# Step 4: Relations:
print("Realtion between time (x) and Temperature Anomaly (T):\n\tT = ")
mathaux.printPoly(kvt)
errT = mathaux.errorPoly(temp_avg, kvt, X, sf, offset)
errCust = mathaux.errorPoly(temp_avg, cust_poly, X, sf, offset)
print("Error in Emperical Relation w.r.t observed values:")
print(errT, "%", "(Original Relations)")
print(errCust, "%", "(Rounded-Off Relations)")
print("-------------------------")
