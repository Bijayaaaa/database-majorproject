NO_TEACHERS = 6 #26    # assuming total of 26 teachers
NO_SUBJECTS = 6    # assuming total of 48 subjects 6 each sem.
NO_SEMS = 8         # no. of classes
NO_SUBS_PER_DAY = 4 

TIMES = ['t'+str(i) for i in range(NO_SUBS_PER_DAY)]
TEACHERS = ['T' + str(i) for i in range(NO_TEACHERS)]
SUBJECTS = ['S'+str(i) for i in range(NO_SUBJECTS)]

routine = [] #
for sub in SUBJECTS:
    for time in TIMES:
        routine.append({'time':time, 'sub':sub})

print(len(routine))
