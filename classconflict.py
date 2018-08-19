# Copyright 2018 Louis Hong

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from dateutil import parser
from datetime import datetime
from collections import namedtuple
import sys, os
from pathlib import Path

print('Programmed by Louis, used for DigiPen SRS system. Contact me @LouisGameDev for help.\n\n')

if len(sys.argv) != 3:
    print("ERROR: Missing arguements.\n")
    print("Command Help")
    print("=============================")
    print("classconflict <path to class table copied from SRS> <path to a list of your current class IDs>\n")
    print("This outputs to a conflict_result.txt file and you can check your conflicts")
    sys.exit(1)
classInputFile = str(Path(os.path.abspath(sys.argv[1])))
# my_classes = ['ANI101F18-A', 'ANI101F18-B']
my_classes = []
with open(str(Path(os.path.abspath(sys.argv[2]))), 'r') as classes:
    for line in classes:
        my_classes.append(line.rstrip())

Range = namedtuple('Range', ['start', 'end'])

classLines = open(classInputFile, 'r').readlines() # read lines

MAX_CLASS_SCHEDULE = 3
class_names = [] # Names
class_instructors = []
class_locations = []
class_schedule_count = []
# class_schedule_index = []
class_schedules = [] # Schedule list, every third is a new class
class_schedule_ranges = []

def time_to_seconds(t):
    return get_timestamp(parser.parse('1970 1 1 ' + t))

def get_timestamp(dt):
    epoch = datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds()

def parseClass():
    state = 'add'
    for i, line in enumerate(classLines):
        line = line.strip('\n\t')
        if line == 'END':
            break
        if line == 'Add':
            state = 'skip credits'
            continue

        if state == 'skip credits':
            state = 'name'
            continue

        if state == 'name':
            class_names.append(line.strip('\n()'))
            state = 'Add'

    # for name in class_names:
    #     print(name)


    skipper = 0
    state = ''


    for i, line in enumerate(classLines):
        line = line.strip('\n').strip('\t')
        if line == 'END':
            break
        if skipper > 0:
            skipper -= 1
            continue

        if line == 'Add':
            skipper = 2
            state = 'schedule'
            continue
        
        if state == 'schedule':
            if (len(class_schedules) == 501):
                pass

            if classLines[i].find('Independent') >= 0:
                class_schedules.extend(['empty'] * 3)
                state = ''
                continue
            count, next_line = parse_classroom(i)

            while not classLines[i + next_line].startswith('Capacity'):
                if classLines[i + next_line] == '\n':
                    next_line += 1
                    continue
                more_count, more_line = parse_classroom(i + next_line)
                if (more_line == 0):
                    break
                next_line += more_line
                count += more_count
            
            class_schedule_count.append(count)

            for i in range(MAX_CLASS_SCHEDULE - count):
                class_schedules.append("empty")
            state = ''

def parse_classroom(i):
    next_line = 1
    count = 0
    if (i + next_line) > (len(classLines) - 1):
        return 0, 0
    while classLines[i + next_line].startswith('  '):
        class_schedules.append(classLines[i + next_line].strip(' \n\t'))
        count += 1
        next_line += 1
    return count, next_line

def parse_schedule():
    days = {
            'Mondays': 0,
            'Tuesdays' : 24*60*60*1,
            'Wednesdays' : 24*60*60*2,
            'Thursdays' : 24*60*60*3,
            'Fridays' : 24*60*60*4
            }
    for text in class_schedules:
        if text == "empty":
            class_schedule_ranges.append("empty")
            continue
        splited = text.split(' ')
        # day
        day = days[splited[0]]
        # time
        time_split = splited[1].split('-')
        # time start
        time_start = time_to_seconds(time_split[0])
        time_end = time_to_seconds(time_split[1])
        time_range = Range(start=day + time_start, end=day + time_end)
        class_schedule_ranges.append(time_range)





def main():
    parseClass()

def output():
    with open("class_names.txt",'w') as nameFile:
        for name in class_names:
            nameFile.write('%s\n' % name)

    with open("class_instructors.txt",'w') as nameFile:
        for name in class_instructors:
            nameFile.write('%s\n' % name)
        
    with open("class_locations.txt",'w') as nameFile:
        for name in class_locations:
            nameFile.write('%s\n' % name)
        
    with open("class_schedule_count.txt",'w') as nameFile:
        for name in class_schedule_count:
            nameFile.write('%s\n' % name)
        
    with open("class_schedules.txt",'w') as nameFile:
        for name in class_schedules:
            nameFile.write('%s\n' % name)

def get_class_index(name):
    for i, other_name in enumerate(class_names):
        if other_name == name:
            return i
    raise Exception("Can't find picked class in class list")

def find_conflict():
    non_conflicts = list(class_names)
    for current in my_classes:
        class_index  = get_class_index(current)
        schedule_index = class_index * 3
        schedule_count = class_schedule_count[class_index]
        

        for my_i in range(schedule_count - 1):
            my_range = class_schedule_ranges[schedule_index + my_i]

            for schedule_i, other_range in enumerate(class_schedule_ranges):
                if other_range == "empty":
                    continue
                if is_overlapped(my_range, other_range):
                    note = class_names[class_index]
                    if non_conflicts[schedule_i // 3].find(note) < 0:
                        if non_conflicts[schedule_i // 3].find('CONFLICT FOUND:') < 0:
                            non_conflicts[schedule_i // 3] = "{0:<20} CONFLICT FOUND: {1}".format(non_conflicts[schedule_i // 3], note)
                        else:
                            non_conflicts[schedule_i // 3] = "{0:<20}, {1}".format(non_conflicts[schedule_i // 3], note)

    with open("conflict_result.txt",'w') as nameFile:
        for name in non_conflicts:
            if name.find("CONFLICT") >= 0:
                nameFile.write("%s\n" % name)

        for name in non_conflicts:
            if name.find("CONFLICT") < 0:
                nameFile.write("%s\n" % name)

def is_overlapped(a_time, b_time):
    latest_start = max(a_time.start, b_time.start)
    earliest_end = min(a_time.end, b_time.end)
    delta = earliest_end - latest_start
    return delta > 0


main()
# output()
parse_schedule()
find_conflict()
pass