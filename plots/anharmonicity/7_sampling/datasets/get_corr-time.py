from __future__ import print_function
import sys
import os
from scipy import signal
import numpy as np

print()

threshold = 0.02
# Check syntax
if len(sys.argv) != 3:
    print("")
    print("You have provided an incorrect syntax.")
    print("The correct syntax is:")
    print('python get_corr-time.py "filename" "skip" ')
    print("Example:  python get_corr-time.py ipi-output 500 ")
    print()
    sys.exit()
else:
    input_name = sys.argv[1]
    skip = sys.argv[2]

# Try to open file
exists = os.path.isfile(input_name)
if not exists:
    print("We can't find the file '{}'.".format(input_name))
    print("")
    sys.exit()
else:
    data = np.loadtxt(input_name)[int(skip) :]
    print("We have skipped the first {} lines".format(skip))
    print("We have {} data points".format(data.size))

# Compute normalized correlation function
mean = np.mean(data)
data -= mean
data = data.reshape(-1, 1)

data2 = np.concatenate((data, np.zeros((data.size, 1))))
acf = signal.correlate(data2, data, mode="valid")
acf = np.divide(acf.flatten(), np.flip(np.arange(1, acf.size + 1), axis=0))

std2 = np.mean(data ** 2)
acf /= std2

tau = np.where(acf.flatten() < threshold)[0][0]

# Print
print("The correlation time is approx. {} ".format(tau))
print()
print(
    "You can check the correlation function in the file: {}".format(
        "corr" + "_" + input_name
    )
)
print()
np.savetxt("corr" + "_" + input_name, acf)
