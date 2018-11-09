#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 6 14:23:33 2017

@author: chuntley

A utility for extracting Fairfield U course data from HTML files scraped from Banner Web.
"""

import re
import csv
import json
from bs4 import BeautifulSoup

# conda install beautifulsoup4

banner_cols = {
    'CRN':1,
    'Subj':2,
    'Crse':3,
    'Sec':4,
    'Cmp':5,
    'Cred':6,
    'Title':7,
    'Days':8,
    'Time':9,
    'Instructor':16,
    'Date':17,
    'Location':18
}

def scrape_banner_course_schedule(filename):
    '''Uses Beautiful Soup to parse an HTML file exported from Banner Web'''

    with open(filename) as fp:
        course_specs = []
        soup = BeautifulSoup(fp,'html.parser')
        data_display_table_rows = soup.find('table',class_='datadisplaytable').find_all('tr')

        #read the table one row at a time, skipping things we don't need
        for row in data_display_table_rows:
            cols = row.select("td.dddefault")
            if (cols):
                crn_raw = str(cols[banner_cols['CRN']].string).strip('\xa0')
                timecode = str(cols[banner_cols['Days']].string)+" "+str(cols[banner_cols['Time']].string+" "+str(cols[banner_cols['Date']].string))
                timecode = timecode.replace(' pm','pm')
                timecode = timecode.replace(' am','am')
                timecode = timecode.replace(':','')

                if crn_raw:
                    # the normal case, not a continuation of the previous row with more timecodes
                    course_spec = {}
                    course_spec['crn']=int(crn_raw)
                    course_spec['catalogid'] = str(cols[banner_cols['Subj']].string)+" "+ str(cols[banner_cols['Crse']].string)
                    course_spec['section'] = str(cols[banner_cols['Sec']].string)
                    course_spec['credits'] = str(cols[banner_cols['Cred']].string)
                    course_spec['title'] = str(cols[banner_cols['Title']].string)
                    course_spec['timecodes'] = [timecode.strip('\xa0')]
                    course_spec['instructor'] = cols[banner_cols['Instructor']].get_text()[:-4]
                    course_specs += [course_spec]
                else:
                    # extra timecodes
                    course_specs[-1]['timecodes'] += [timecode.strip('\xa0')]

    return course_specs;


def json_dump(data, filename):
    ''' A utility to dump data into a JSON file '''
    f = open(filename,"w")
    json.dump(data,f)

# scrape_banner_course_schedule('Spring2018GradClassSchedule.html')
# course_offerings =  scrape_banner_course_schedule('Spring2018ClassSchedules.html')
# print(course_offerings)
# json_dump(course_offerings,"FairfieldUniversitySpring2018.json")
