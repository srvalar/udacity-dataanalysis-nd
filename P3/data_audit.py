import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import cerberus
import os
from collections import defaultdict
import copy
import sqlite3

# ------------------------------------
#           Regular Expressions
# ------------------------------------

''' Check for lower-case tags '''
LOWER = re.compile(r'^([a-z]|_)*$')

''' Check for lower-case tags that include a colon (:)'''
LOWER_COLON = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')

''' Check for problematic characters'''
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

''' Check for street types'''
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

''' Check for post codes'''
post_code_re = re.compile(r'^\d{5}(?:[-\s]\d{4})?$')

''' Check for characters only (no numbers)'''
all_chars_re = re.compile(r'^[a-zA-Z]+$')

''' Check for term 'CA' in the post codes'''
ca_in_zipcode_re = re.compile(r'^CA(.*)')

# ------------------------------------
#           Mappings
# ------------------------------------

# List of expected street types
expected = ["Avenue", "Boulevard", "Circle", "Commons", "Court", "Drive", "Expressway",
            "Highway", "Lane", "Loop", "Parkway", "Place", "Plaza", "Real", "Road",
            "Row", "Square", "Street", "Terrace", "Walk", "Way"]

# Mapping of non-expected: expected street types
street_mapping = { "Ave": "Avenue", "ave": "Avenue", "Blvd": "Boulevard",
            "Boulevard": "Boulevard", "Boulvevard": "Boulevard",
            "Cir": "Circle", "Ct": "Court", "court": "Court",
            "Dr": "Drive", "Hwy": "Highway", "Ln": "Lane", 
            "Mt.": "Mount", "Mt": "Mount","Rd": "Road",  "Rd.": "Road",
            "Sq": "Square", "st": "Street", "street": "Street", "St": "Street", 
            "ste": "Suite", "ste.": "Suite", "Ste.": "Suite", "Ste": "Suite",
            "square": "Square", "parkway": "Parkway"
          }

# Mapping of non-expected: expected directions & terms in street names
direction_unusual_mapping = {"E": "East", "E.": "East", "N": "North", "N.": "North",
            "S": "South", "S.": "South", "W": "West", "W.": "West",
            "Pkwy": "Parkway", "Ste": "Suite", "Ave": "Avenue", "Rd":"Road",
            "Mt": "Mount", "Mt.":"Mount", "rio":"Rio", "robles": "Robles"
            }

# Mapping of entire street names that are to be replaced
name_mapping = {"Zanker Rd., San Jose, CA": "Zanker Road", "Zanker Road, San Jose, CA": "Zanker Road",
    "Ala 680 PM 0.1": "Interstate-680", "Hwy 17 PM 7.1": "Highway 17"
}

# ------------------------------------
#           Audit Functions
# ------------------------------------

def audit_street_type(street_types, street_name):
    '''
        Adds to dictionary of problematic street types
        
        Args:
          Street type
          Street name
        
        Returns:
          Appends to a dictionary of problematic street types
    '''
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    '''
        Checks whether tag address element is a street
        
        Args:
          Tag element
        
        Returns:
          Bool indicating whether tag element is a street or not
    '''
    return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
    '''
        Audits the input file for street name issues
        
        Args:
          Input OSM file
        
        Returns:
          Prints out problematic street names
    '''
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def audit_postcode(osmfile):
    '''
        Audits the input file for postcode issues
        
        Args:
          Input OSM file
        Returns:
          Prints out problematic postcodes.
    '''
    post_file = open(osmfile, "r")
    zip_codes = []
    for event, elem in ET.iterparse(post_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == 'addr:postcode':
                    post_code = tag.attrib['v'].strip()
                    m = post_code_re.match(post_code)
                    # print zip codes that are not properly formatted
                    if not m:
                        print post_code
                        zip_codes.append(post_code)
    post_file.close()
    return zip_codes



if __name__ == '__main__':
  sample = "sj_sample.osm"
  street_types = audit(sample)
  pprint.pprint(dict(street_types))
  postcodes = audit_postcode(sample)

