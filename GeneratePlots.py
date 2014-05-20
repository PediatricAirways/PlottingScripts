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

arrayNames = ['Age',
              'Weight',
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

surgeryCases = patientRecords.Filter( [('SurgeryChosen', '==', 'Y'),
                                       ('PatientID', '>=', 2000)] )
print surgeryCases.GetNumberOfRecords(), "surgery cases"
surgeryArrays = surgeryCases.GetArraysOfMembers(arrayNames);

noSurgeryCases = patientRecords.Filter( [('SurgeryChosen', '==', 'N'),
                                         ('PatientID', '>=', 2000)] )
print noSurgeryCases.GetNumberOfRecords(), "no surgery cases"
noSurgeryArrays = noSurgeryCases.GetArraysOfMembers(arrayNames);

for abcissaName in ['Age', 'Weight']:
    for ordinateName in arrayNames[2:]:

        fig = Figure()
        canvas = FigureCanvas(fig)
        axes = fig.add_subplot(111)

        xLabel = abcissaName
        xLabel = xLabel.replace('Age', 'Age (months)')
        xLabel = xLabel.replace('Weight', 'Weight (kg)')
        axes.set_xlabel(xLabel)

        yLabel = ordinateName.replace('_', ' - ')
        yLabel = yLabel.replace('CrossSectionalArea', 'Cross-Sectional Area')
        yLabel = yLabel.replace('HydraulicDiameter', 'Hydraulic Diameter')
        yLabel = yLabel.replace('Mid', 'Mid-')
        yLabel = yLabel.replace('AtlasScore', 'Atlas Score')
        yLabel = yLabel.replace('RatioScore', 'Ratio Score')
        axes.set_ylabel(yLabel)

        title = '{0} vs. {1}'.format(yLabel, abcissaName)
        axes.set_title(title)

        axes.hold('on')

        axes.plot(controlArrays[abcissaName],
                  controlArrays[ordinateName], 'gx', label='Control')
        axes.plot(surgeryArrays[abcissaName],
                  surgeryArrays[ordinateName], color='yellow', marker='^',
                  linestyle='None', label='SGS - Surgery')
        axes.plot(noSurgeryArrays[abcissaName],
                  noSurgeryArrays[ordinateName], 'bo', label='SGS - No Surgery')

        axes.legend(numpoints=1)

        axes.hold('off')
        fig.savefig('images/{0}-vs-{1}.png'.format(ordinateName, abcissaName))

