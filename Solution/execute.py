from solution import *
from provisionalInputs import *
import pprint

def run():
    daysDivided = divideDaysByDate(firstTestInput)
    weekDivided = divideWeekByDate(daysDivided)

    dataDay = knowTopFromDay(daysDivided)
    dataWeek = sortStatsWeek(getStatsWeek(weekDivided))

    allData = [dataDay, dataWeek]

    pprint.pprint(allData)

run()