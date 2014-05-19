import csv
import sys
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

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

surgeryCases = patientRecords.Filter( [('SurgeryChosen', '==', 'Y'), ('PatientID', '>=', 2000)] )
print surgeryCases.GetNumberOfRecords(), "surgery cases"
surgeryArrays = surgeryCases.GetArraysOfMembers(arrayNames);

noSurgeryCases = patientRecords.Filter( [('SurgeryChosen', '==', 'N'), ('PatientID', '>=', 2000)] )
print noSurgeryCases.GetNumberOfRecords(), "no surgery cases"
noSurgeryArrays = noSurgeryCases.GetArraysOfMembers(arrayNames);

for abcissaName in ['AgeInMonths', 'WeightInKg']:
    for ordinateName in arrayNames[2:]:

        fig = Figure()
        canvas = FigureCanvas(fig)
        axes = fig.add_subplot(111)
        axes.set_title(ordinateName)
        axes.set_xlabel(abcissaName)
        axes.set_ylabel(ordinateName)

        axes.hold('on')

        axes.plot(controlArrays[abcissaName],
                  controlArrays[ordinateName], 'gx')
        axes.plot(surgeryArrays[abcissaName],
                  surgeryArrays[ordinateName], 'r^')
        axes.plot(noSurgeryArrays[abcissaName],
                  noSurgeryArrays[ordinateName], 'bo')

        axes.legend(('CRL', 'Surgery', 'No Surgery'), numpoints=1)

        axes.hold('off')
        canvas.print_png('images/{0}-vs-{1}.png'.format(ordinateName, abcissaName))
