import csv
import sys

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
        self.PatientID = None
        self.AgeInMonths = None
        self.Sex = None
        self.WeightInKg = None
        self.SurgeryStatus = None
        self.SurgeryChosen = None

        self.CrossSectionalArea_TVC        = None
        self.CrossSectionalArea_Subglottis = None
        self.CrossSectionalArea_MidTrachea = None
        self.CrossSectionalArea_Ratio      = None
        self.CrossSectionalArea_AtlasScore = None
        self.CrossSectionalArea_RatioScore = None

        self.HydraulicDiameter_TVC         = None
        self.HydraulicDiameter_Subglottis  = None
        self.HydraulicDiameter_MidTrachea  = None
        self.HydraulicDiameter_Ratio       = None
        self.HydraulicDiameter_AtlasScore  = None
        self.HydraulicDiameter_RatioScore  = None

    def Print(self):
        for pair in PatientRecord.ColumnToMemberList:
            member = pair[1]
            print member, ":", getattr(self, member)
        
###################################################################

###################################################################
class PatientRecordList:

    def __init__(self, rows):
        self.patientRecords = []
        for row in rows[1:]:
            self.patientRecords.append(PatientRecord())

        columnToMemberMap = { 'PatientId'          : 'PatientID',
                              'Age (months)'       : 'AgeInMonths',
                              'Sex'                : 'Sex',
                              'Weight (kg)'        : 'WeightInKg',
                              'Pre or PostSurgery' : 'SurgeryStatus',
                              'Surgery?'           : 'SurgeryChosen',
                              'XA_TVC'             : 'CrossSectionalArea_TVC',
                              'XA_Subglottis'      : 'CrossSectionalArea_Subglottis',
                              'XA_MidTrachea'      : 'CrossSectionalArea_MidTrachea',
                              'XA_Ratio'           : 'CrossSectionalArea_Ratio',
                              'XA_Atlas_Score'     : 'CrossSectionalArea_AtlasScore',
                              'XA_Ratio_Score'     : 'CrossSectionalArea_RatioScore',
                              'HD_TVC'             : 'HydraulicDiameter_TVC',
                              'HD_Subglottis'      : 'HydraulicDiameter_Subglottis',
                              'HD_MidTrachea'      : 'HydraulicDiameter_MidTrachea',
                              'HD_Ratio'           : 'HydraulicDiameter_Ratio',
                              'HD_Atlas_Score'     : 'HydraulicDiameter_AtlasScore',
                              'HD_Ratio_Score'     : 'HydraulicDiameter_RatioScore' }

        for pair in PatientRecord.ColumnToMemberList:
            columnName = pair[0]
            memberName = pair[1]
            columnIndex = rows[0].index(columnName)
            for pr, row in zip(self.patientRecords, rows[1:]):
                setattr(pr, memberName, row[columnIndex])

    def Print(self):
        for pr in self.patientRecords:
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
patientRecords.Print()
