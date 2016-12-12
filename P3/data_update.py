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

import data_audit

def update_street_tags(name):
    '''
        Updates problematic street names
        
        Args:
            Street name tags
        Returns:
            Updated street name tags
    ''' 
    
    # Updates street types
    m = street_type_re.search(name)
    if m:
        st_type = m.group()
        if st_type in street_mapping:
            name = re.sub(street_type_re, street_mapping[st_type], name)
    units = name.split()
    
    # Updates unusual street name terms and abbreviated directions
    for u in range(len(units)):
        if units[u] in direction_unusual_mapping:
            if units[u].lower() not in ['#', 'suite', 'ste.', 'ste']: 
                units[u] = direction_unusual_mapping[units[u]]
                name = " ".join(units)
    
    # Updates entire unusual street names
    if "CA" in name or "PM" in name:
        name = name_mapping[name]
        
    return name


def update_zip_code(zipcode):
    '''
        Updates problematic zip/post codes
        
        Args:
            Zip/post codes
        Returns:
            Updated zip/post codes
    '''
    
    zipcode = zipcode.strip()
    match = post_code_re.search(zipcode)
    all_chars_zip = all_chars_re.match(zipcode)
    ca_in_zipcode = ca_in_zipcode_re.search(zipcode)
    
    # Return as-is if not in problematic set
    if match:
        return zipcode
    
    # Update if term 'CA' found
    elif ca_in_zipcode:        
        return zipcode[3:8]
    
    # Update if length >5 and has no chars
    elif (len(zipcode) > 5 and 
          not all_chars_zip):
        zipcode = zipcode[0:5]
        return str(zipcode)
    
    else:
        return None
