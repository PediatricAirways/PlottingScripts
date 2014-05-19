import csv
import sys
import matplotlib.pyplot as plt
from PatientRecord import *
import numpy as np

if (len(sys.argv) < 2):
    print 'Usage: ', sys.argv[0], '<input CSV file>'
    sys.exit(-1)

###################################################################
# Script entry point
###################################################################
rows = []
with open(sys.argv[1], 'rb') as csvfile:

    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        rows.append(row)

patientRecords = PatientRecordList(rows)

arrayNames = ['AgeInMonths',
              'WeightInKg',
              'CrossSectionalArea_TVC',
              'CrossSectionalArea_Subglottis',
              'CrossSectionalArea_MidTrachea',
              'CrossSectionalArea_Ratio',
              'CrossSectionalArea_AtlasScore',
              'CrossSectionalArea_RatioScore',
              'HydraulicDiameter_TVC',
              'HydraulicDiameter_Subglottis',
              'HydraulicDiameter_MidTrachea',
              'HydraulicDiameter_Ratio',
              'HydraulicDiameter_AtlasScore',
              'HydraulicDiameter_RatioScore']

controlCases = patientRecords.Filter( [('PatientID', '<', 2000)] )
print controlCases.GetNumberOfRecords(), "controls"
controlArrays = controlCases.GetArraysOfMembers(arrayNames);

surgeryCases = patientRecords.Filter( [('SurgeryChosen', '==', 'N'), ('PatientID', '>=', 2000)] )
print surgeryCases.GetNumberOfRecords(), "surgery cases"
surgeryArrays = surgeryCases.GetArraysOfMembers(arrayNames);

noSurgeryCases = patientRecords.Filter( [('SurgeryChosen', '==', 'Y'), ('PatientID', '>=', 2000)] )
print noSurgeryCases.GetNumberOfRecords(), "no surgery cases"
noSurgeryArrays = noSurgeryCases.GetArraysOfMembers(arrayNames);

plt.title('TVC Cross-sectional Area by Age')
axes = plt.axes()
axes.set_xlabel('Age')
axes.set_ylabel('TVC Cross-sectional Area')
axes.set_frame_on(True)
plt.hold('on')

plt.plot(controlArrays['AgeInMonths'],
         controlArrays['CrossSectionalArea_TVC'], 'gx')
plt.plot(surgeryArrays['AgeInMonths'],
         surgeryArrays['CrossSectionalArea_TVC'], 'r^')
plt.plot(noSurgeryArrays['AgeInMonths'],
         noSurgeryArrays['CrossSectionalArea_TVC'], 'bo')

plt.legend(('CRL', 'Surgery', 'No Surgery'), numpoints=1)

plt.hold('off')
plt.show()
