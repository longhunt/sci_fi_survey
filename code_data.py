#! /usr/bin/env python2
# -*- coding: utf-8 -*-

''' Cleans up downloaded CSV from Google Forms 
	Released by Creative Minority Productions 
	under the terms of the Gnu Public License 2.0 '''

import csv
#from my_statistics import mean, stddev, p5_fit


def sumproduct(*lists):   ## FIXME TEst this!!!
    return sum([x*y for x,y in zip(*lists)])

class zipCodeStuff:
    ''' Validates zip codes '''

    zipDB = []

    def __init__(self):
        with open ("zip_code_database.csv", "r") as f:
            fc = csv.reader(f)
            for c in fc:
                self.zipDB.append(c)

    def test(self, zip):
        '''find out if a particular zip is in the database '''

        return (str(zip) in [z[0] for z in self.zipDB]) 


class surveyVar:
    ''' Data object for each particular variable '''

    surveyValues = []

    def __init__(self, dFrame, column):
        self.surveyValues = [d[column] for d in dFrame]


    def values(self):
        return self.surveyValues

    def code(self, codeBook, nonResponseValue):
        ''' codes the data into numbers.  codeBook is a list of tuples '''

        retList = []
        for s in self.surveyValues:

            try:
                for c in codeBook:
                    if s == c[0] :
                        retList.append(c[1])
            except:
                retList.append(nonResponseValue)

        return(retList)


def suckInFile(file):
    ''' Brings in data from the CSV '''

    with open(file, "r") as f:
        fc = csv.reader(f)

        csvData = [c for c in fc if c.count("") < 27]

    csvData = csvData[1:]
    return (csvData)

dFrame = suckInFile ("prelimSurveyDump.csv")

v_timeStamp = surveyVar(dFrame, 0).values()

v_libraryCard = surveyVar(dFrame, 1).code([('Yes', 2), ('No', 1), ("I don't remember", 0), ('', -1)], -1)


v_libraryVisits = surveyVar(dFrame, 2).code([("1-3 times per year", 1), 
                        ("11-20 times per year", 3), ("21 or more times per year", 4), 
                        ("4-10 times per year", 2), ("Less than once per year", 0), ("", -1)], -1)



v_itemsYear = surveyVar(dFrame, 3).code([("2-5 items", 1), 
                                ("21-50 items", 3),
                                ("6-20 items", 2),
                                ("More than fifty items", 4),
                                ("One or fewer items", 0),
                                ("", -1)], -1)


v_scifiYear = surveyVar(dFrame, 4).code([("2-5 items", 1), ("21-50 items", 3),
                                ("6-20 items", 2),
                                ("More than fifty items", 4),
                                ("One or fewer items", 0),
                                ("", -1)], -1)


v_DoULike_temp = surveyVar(dFrame, 5).values()
v_DoULike_Novel = [int("Adult Novels" in v) for v in v_DoULike_temp]
v_DoULike_YA = [int("Young Adult Novels" in v) for v in v_DoULike_temp]
v_DoULike_SS = [int("Short Fiction" in v) for v in v_DoULike_temp]
v_DoULike_Audio = [int("Audiobooks" in v) for v in v_DoULike_temp]


v_printVsE = surveyVar(dFrame, 6).code([('1',1),('2',2),('3',3),('4',4),('5', 5), ('6',6), ('7',7), ('',-1)], -1)


v_bookChoice = [None for x in range(12)]
for i in range(12):
    v_bookChoice[i] = surveyVar(dFrame, i+7).code([("Extremely Important", 5),
                                ("Moderately Important", 3),
                                ("Not At All Important", 1),
                                ("Not Very Important", 2),
                                ("Very Important", 4),
                                ("", -1)], -1)


v_bookChoiceOthr = surveyVar(dFrame, 20).values()

v_DescribU_temp = surveyVar(dFrame, 21).values()
v_pro = [x != "" for x in v_DescribU_temp]
v_DescribU_IndProf = [int("Entertainment Industry Professional" in v) for v in v_DescribU_temp]
v_DescribU_Academic = [int("Humanities Scholar or Academic Librarian" in v) for v in v_DescribU_temp]
v_DescribU_ProWriter = [int("Professional Writer" in v) for v in v_DescribU_temp]
v_DescribU_Teacher = [int("Teacher" in v) for v in v_DescribU_temp]
v_DescribU_Librarian = [int("Public Librarian" in v) for v in v_DescribU_temp]



v_Age = surveyVar(dFrame, 22).code([("Under 12", 1),
                                    ("12-17", 2),
                                    ("18-24", 3),
                                    ("25-34", 4),
                                    ("35-54", 5),
                                    ("55-64", 6),
                                    ("Over 64", 7),
                                    ("", -1)], -1)


v_Education = surveyVar(dFrame, 23).code([("6th grade or lower", 1),
                                            ("Some junior high or high school", 2),
                                            ("High school diploma or GED", 3),
                                            ("Some College", 4),
                                            ("Two year degree and/or trade apprenticeship", 5),
                                            ("Bachelors degree", 6),
                                            ("Masters Degree and/or professional license", 7),
                                            ("Doctorate", 8),
                                            ("", -1)], -1)

v_Gender = surveyVar(dFrame, 24).code([("Female", 1), ("Male", 2), ("Fluxfluid", 3), 
                                            ("nonbinary", 4), ("Prefer not to say", -1), ("", -1)], -1)

v_HHPeeps = surveyVar(dFrame, 25).code([("",-1), ("One", 1), ("2-3", 2), ("4-6", 3), ("More than 6", 4)], -1)

v_HHIncome = surveyVar(dFrame, 26).code([("Don't know or prefer not to say", -1),
                                        ("", -1),
                                        ("Under $20,000", 1),
                                        ("$20,000 to $50,000", 2),
                                        ("$50,001 to $100,000", 3),
                                        ("$101,000 to $250,000", 4),
                                        ("$250,001 to $500,000", 5),
                                        ("Over $500,000", 6)], -1)


v_Zip = surveyVar(dFrame, 27).values()

zippers = zipCodeStuff()
for i in range(len(v_Zip)):
    if not zippers.test(v_Zip[i]):
        v_Zip[i] = -1


with open("prelimDumpClean.csv", "w") as f:
    csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    row = ["v_timeStamp", "v_libraryCard", "v_libraryVisits", "v_itemsYear", "v_scifiYear", "v_DoULike_Novel",
                "v_DoULike_YA", "v_DoULike_SS", "v_DoULike_Audio", "v_printVsE",
                "v_bookChoice[0]", "v_bookChoice[1]", "v_bookChoice[2]", "v_bookChoice[3]",
                "v_bookChoice[4]", "v_bookChoice[5]", "v_bookChoice[6]", "v_bookChoice[7]",
                "v_bookChoice[8]", "v_bookChoice[9]", "v_bookChoice[10]", "v_bookChoice[11]",
                "v_bookChoiceOthr", "v_DescribU_IndProf", "v_DescribU_Academic", "v_DescribU_ProWriter",
                "v_DescribU_Teacher", "v_DescribU_Librarian",
                "v_Age", "v_Education", "v_Gender", "v_HHPeeps", "v_HHIncome", "v_Zip"]
    csv_writer.writerow(row)


    for i in range(len(v_timeStamp)):
        row = [v_timeStamp[i], v_libraryCard[i], v_libraryVisits[i], v_itemsYear[i], v_scifiYear[i], v_DoULike_Novel[i],
                v_DoULike_YA[i], v_DoULike_SS[i], v_DoULike_Audio[i], v_printVsE[i],
                v_bookChoice[0][i], v_bookChoice[1][i], v_bookChoice[2][i], v_bookChoice[3][i],
                v_bookChoice[4][i], v_bookChoice[5][i], v_bookChoice[6][i], v_bookChoice[7][i],
                v_bookChoice[8][i], v_bookChoice[9][i], v_bookChoice[10][i], v_bookChoice[11][i],
                v_bookChoiceOthr[i], v_DescribU_IndProf[i], v_DescribU_Academic[i], v_DescribU_ProWriter[i],
                v_DescribU_Teacher[i], v_DescribU_Librarian[i],
                v_Age[i], 
                v_Education[i], 
                v_Gender[i], 
                v_HHPeeps[i], 
                v_HHIncome[i], 
                v_Zip[i]]


        csv_writer.writerow(row)


# Now print a little report of low-hanging fruit type statistics

print "\033[H\033[J"   # VT100 escape sequence to clear the screen

# # 1. Do you have a library card?

# n = float(len([x for x in v_libraryCard if x != -1]))

# print "Q1: Do you have a library card?"
# print "n=", n
# print "response rate = %2.2f"%(100. * n / float(len(v_libraryCard))), "%\n"
# print "              ", "π (%)\t 95% CI (%)"

# p_y = v_libraryCard.count(2) / n
# ci_y_l = p_y - 1.96*(p_y*((1-p_y)/n)**.5)
# ci_y_u = p_y + 1.96*(p_y*((1-p_y)/n)**.5)
# print "           Yes", "%2.2f"%(100. * p_y), "\t", "%2.2f"%(100. * ci_y_l),"%2.2f"%(100. * ci_y_u)

# p_n = v_libraryCard.count(1) / n
# ci_n_l = p_n - 1.96*(p_n*((1-p_n)/n)**.5)
# ci_n_u = p_n + 1.96*(p_n*((1-p_n)/n)**.5)
# print "            No", "%2.2f"%(100. * p_n), "\t", "%2.2f"%(100. * ci_n_l),"%2.2f"%(100. * ci_n_u)

# p_d = v_libraryCard.count(0) / n
# ci_d_l = p_d - 1.96*(p_d*((1-p_d)/n)**.5)
# ci_d_u = p_d + 1.96*(p_d*((1-p_d)/n)**.5)
# print "Don't remember", "%2.2f"%(100. * p_d), "\t", "%2.2f"%(100. * ci_d_l),"%2.2f"%(100. * ci_d_u)

# print "\n"

# print "Q2. About how many times a year do you visit a public library?"

# r_libraryVisits = [x for x in v_libraryVisits if x != -1]
# n = float(len(r_libraryVisits))

# print "ENTIRE SAMPLE"
# print "n=", n
# print "response rate = %2.2f"%(100. * n / float(len(v_libraryVisits))), "%"
# print "raw mean=%2.3f\t"%mean(r_libraryVisits),

# print "raw std_dev=%2.3f\t"%stddev(r_libraryVisits, ddof=1)

# rCI_l = mean(r_libraryVisits) - 1.96*(stddev(r_libraryVisits, ddof=1)/n)**.5
# rCI_u = mean(r_libraryVisits) + 1.96*(stddev(r_libraryVisits, ddof=1)/n)**.5
# print "95% CI=", "[%2.3f,"%rCI_l,"%2.3f]"%rCI_u 

# f_interp = p5_fit([(10**(-16),10**(-16)), (1,2), (2,7), (3,15.5), (3.5,21)])
# print "interpolated mean= %2.1f"%f_interp(mean(r_libraryVisits)), "visits per year"

# print "\n"

# r_libraryVisits = [v_libraryVisits[i] for i in range(len(v_libraryVisits)) if v_pro[i] == False and 
                    # v_libraryVisits[i] != -1]

# n = float(len(r_libraryVisits))

# print "NON-PROFESSIONALS"
# print "n=", n
# print "raw mean=%2.3f\t"%mean(r_libraryVisits),

# print "raw std_dev=%2.3f\t"%stddev(r_libraryVisits, ddof=1)

# rCI_l = mean(r_libraryVisits) - 1.96*(stddev(r_libraryVisits, ddof=1)/n)**.5
# rCI_u = mean(r_libraryVisits) + 1.96*(stddev(r_libraryVisits, ddof=1)/n)**.5
# print "95% CI=", "[%2.3f,"%rCI_l,"%2.3f]"%rCI_u 

# f_interp = p5_fit([(10**(-16),10**(-16)), (1,2), (2,7), (3,15.5), (3.5,21)])
# print "interpolated mean= %2.1f"%f_interp(mean(r_libraryVisits)), "visits per year"

print "\n"


l_ChoiceFact = ['[High rating online (e.g. on Goodreads or Amazon)]', 
                '[I recognize the author.]', 
                '[It is the first book in a series.]', 
                '[I am a big fan of this sub-genre.]', 
                '[I have read other books in this series.]', 
                '[The library has several other books in this series.]', 
                '[This book ties in with or is related to a movie or TV show that I like. ]', 
                '[The book is on the "new books" shelf or has a "new" sticker.]', 
                '[I read a review of this book.]', 
                '[I\'ve heard this book is a "classic".]', 
                '[A library employee recommended this book.]', 
                '[This book won a reward.]', 
                '[Other (please write in below)]']

print "FACTORS IN BOOK CHOICE\n"

c_factors = range(12)
c_factors.sort(key=lambda i: sum([x for x in v_bookChoice[i] if x != -1])/float(len([x for x in v_bookChoice[i] if x != -1])))
c_factors.reverse()

for i in c_factors:
    print l_ChoiceFact[i].rjust(76) + "\t", 
    print "%.3f" % float(sum([x for x in v_bookChoice[i] if x != -1])/float(len([x for x in v_bookChoice[i] if x != -1])))

print "\nOTHER FACTORS\n"
for v in v_bookChoiceOthr:
    if v != "":
        print v
