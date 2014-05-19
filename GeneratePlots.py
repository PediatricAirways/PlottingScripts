import csv
import sys
import matplotlib

if (len(sys.argv) < 2):
    print 'Usage: ', sys.argv[0], '<input CSV file>'
    sys.exit(-1)

###################################################################
class PatientRecord:
    """Simple storage class for patient records."""

    ColumnToMemberList = [ ('PatientId',           'PatientID'),
                           ('Age (months)',        'AgeInMonths'),
                           ('Sex',                 'Sex'),
                           ('Weight (kg)',         'WeightInKg'),
                           ('Pre or PostSurgery',  'SurgeryStatus'),
                           ('Surgery?',            'SurgeryChosen'),
                           ('XA_TVC',              'CrossSectionalArea_TVC'),
                           ('XA_Subglottis',       'CrossSectionalArea_Subglottis'),
                           ('XA_MidTrachea',       'CrossSectionalArea_MidTrachea'),
                           ('XA_Ratio',            'CrossSectionalArea_Ratio'),
                           ('XA_Atlas_Score',      'CrossSectionalArea_AtlasScore'),
                           ('XA_Ratio_Score',      'CrossSectionalArea_RatioScore'),
                           ('HD_TVC',              'HydraulicDiameter_TVC'),
                           ('HD_Subglottis',       'HydraulicDiameter_Subglottis'),
                           ('HD_MidTrachea',       'HydraulicDiameter_MidTrachea'),
                           ('HD_Ratio',            'HydraulicDiameter_Ratio'),
                           ('HD_Atlas_Score',      'HydraulicDiameter_AtlasScore'),
                           ('HD_Ratio_Score',      'HydraulicDiameter_RatioScore') ]

    def __init__(self):
        for pair in PatientRecord.ColumnToMemberList:
            setattr(self, pair[1], None)

    def Print(self):
        for pair in PatientRecord.ColumnToMemberList:
            member = pair[1]
            print member, ":", getattr(self, member)
        
###################################################################

###################################################################
def is_float(value):
    try:
        float(value)
    except ValueError:
        return False
    return True
###################################################################

###################################################################
class PatientRecordList:

    def __init__(self, rows):
        self.PatientRecords = []
        if (len(rows) > 1):
            for row in rows[1:]:
                self.PatientRecords.append(PatientRecord())

                for pair in PatientRecord.ColumnToMemberList:
                    columnName = pair[0]
                    memberName = pair[1]
                    columnIndex = rows[0].index(columnName)
                    for pr, row in zip(self.PatientRecords, rows[1:]):
                        columnValue = row[columnIndex]
                        if (is_float(columnValue)):
                            setattr(pr, memberName, float(columnValue))
                        else:
                            setattr(pr, memberName, columnValue)

    def AddPatientRecord(self, patientRecord):
        self.PatientRecords.append(patientRecord)

    def GetNumberOfRecords(self):
        return len(self.PatientRecords)

    def Filter(self, queryList):
        # A query is a triplet ('MemberName', 'operator', 'comparisonValue')
        # All queries are implicitly "and-ed"
        newPatientRecordList = PatientRecordList([])
        for pr in self.PatientRecords:
            keep = True
            for query in queryList:
                memberName      = query[0]
                operator        = query[1]
                comparisonValue = query[2]
                value = getattr(pr, memberName, None)
                if (operator == '=='):
                    keep = keep and (value == comparisonValue)
                elif (operator == '!='):
                    keep = keep and (value != comparisonValue)
                elif (operator == '<'):
                    keep = keep and (value < comparisonValue)
                elif (operator == '<='):
                    keep = keep and (value <= comparisonValue)
                elif (operator == '>'):
                    keep = keep and (value > comparisonValue)
                elif (operator == '>='):
                    keep = keep and (value >= comparisonValue)

            if (keep):
                newPatientRecordList.AddPatientRecord(pr)

        return newPatientRecordList

    def GetArraysOfMembers(self, memberList):
        arrayDict = {}
        for memberName in memberList:
            memberArray = []
            for pr in self.PatientRecords:
                memberArray.append(getattr(pr, memberName))
            arrayDict[memberName] = memberArray

        return arrayDict

    def Print(self):
        for pr in self.PatientRecords:
            pr.Print()
            print

###################################################################
# Script entry point
###################################################################
rows = []
with open(sys.argv[1], 'rb') as csvfile:

    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        rows.append(row)

patientRecords = PatientRecordList(rows)

controlCases = patientRecords.Filter( [('PatientID', '<', 2000)] )
print controlCases.GetNumberOfRecords(), "controls"

surgeryCases = patientRecords.Filter( [('SurgeryChosen', '==', 'N'), ('PatientID', '>=', 2000)] )
#surgeryCases.Print()
print surgeryCases.GetNumberOfRecords(), "surgery cases"

noSurgeryCases = patientRecords.Filter( [('SurgeryChosen', '==', 'Y'), ('PatientID', '>=', 2000)] )
print noSurgeryCases.GetNumberOfRecords(), "no surgery cases"


