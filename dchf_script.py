import csv
import os
from pathlib import Path
from datetime import date
import re
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']


def read_csv(file_path):
    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
        reader = csv.reader(file)
        return list(reader)

file_name = f'DCHF-output-{date.today()}.csv'
BaseDir = Path(__file__).resolve().parent
files = os.listdir(BaseDir)
print(files)
input_data = []
all_columns_names = []
for file in files:
    if '.csv' in file and 'output' not in file:
        reader = read_csv(file)
        count = 0
        for oneRow in reader:
            if count == 0:
                count += 1
                for key in oneRow:
                    all_columns_names.append(key)
                continue
            else:
                replacement_dict = {"Ne": "NE", "Se": "SE", "Nw": "NW", "Sw": "SW"}
                capitalize_address_l1 = re.sub(
                    r'\b(Ne|Se|Nw|Sw)\b',
                    lambda x: replacement_dict.get(x.group(0), x.group(0)),
                    oneRow[8],
                )
                input_data.append({all_columns_names[0]: oneRow[0], all_columns_names[1]: oneRow[1],
                                   all_columns_names[2]: oneRow[2],
                                   all_columns_names[3]: oneRow[3], all_columns_names[4]: oneRow[4],
                                   all_columns_names[5]: oneRow[5], all_columns_names[6]: oneRow[6],
                                   all_columns_names[7]: oneRow[7], all_columns_names[8]: capitalize_address_l1,
                                   all_columns_names[9]: oneRow[9], all_columns_names[10]: oneRow[10],
                                   all_columns_names[11]: oneRow[11], all_columns_names[12]: oneRow[12],
                                   all_columns_names[13]: oneRow[13], all_columns_names[14]: oneRow[14],
                                   all_columns_names[15]: oneRow[15], all_columns_names[16]: oneRow[16],
                                   all_columns_names[17]: oneRow[17], all_columns_names[18]: oneRow[18],
                                   all_columns_names[19]: oneRow[19], all_columns_names[20]: oneRow[20],
                                   all_columns_names[21]: oneRow[21], all_columns_names[22]: oneRow[22],
                                   all_columns_names[23]: oneRow[23], all_columns_names[24]: oneRow[24],
                                   all_columns_names[25]: oneRow[25], all_columns_names[26]: oneRow[26],
                                   all_columns_names[27]: oneRow[27], all_columns_names[28]: oneRow[28],
                                   all_columns_names[29]: oneRow[29], all_columns_names[30]: oneRow[30],
                                   all_columns_names[31]: oneRow[31], all_columns_names[32]: oneRow[32],
                                   all_columns_names[33]: oneRow[33]})

print(len(input_data))
all_specialities_set = set()
for row in input_data:
    all_specialities_set.add(row['Specialty'])
print(all_specialities_set)

all_state_set = set()
for row in input_data:
    all_state_set.add(row['State'])
print(all_state_set)

all_country_set = set()
for row in input_data:
    all_country_set.add(row['County'])
print(all_country_set)

# all_address_set = set()
# for row in input_data:
#     all_address_set.add(row['AddressLine1'])
# print(all_address_set)

all_specialities_dict = {}
for speciality in sorted(all_specialities_set):
    all_specialities_dict.update({speciality: []})
    for d in input_data:
        if d['Specialty'] == speciality:
            all_specialities_dict[speciality].append(d)

all_state_sorted_list = {}
for spec, spec_list in all_specialities_dict.items():
    all_state_sorted_list.update({spec: {}})
    count = 1
    for state in sorted(all_state_set):
        all_state_sorted_list[spec][state] = []
        for d in spec_list:
            if d['State'] == state:
                all_state_sorted_list[spec][state].append(d)

all_country_sorted_list = {}
for spec, states in all_state_sorted_list.items():
    all_country_sorted_list.update({spec: {}})
    for state in states.keys():
        all_country_sorted_list[spec].update({state:{}})
        for country in sorted(all_country_set):
            all_country_sorted_list[spec][state][country] = []
            d = all_state_sorted_list[spec][state]
            for m in d:
                if m['County'] == country:
                    all_country_sorted_list[spec][state][country].append(m)

group_name_sorted_list = {}
for spec, states in all_country_sorted_list.items():
    group_name_sorted_list.update({spec: {}})
    for state in states.keys():
        group_name_sorted_list[spec].update({state: {}})
        for countries in states.values():
            for country in countries.keys():
                all_data = all_country_sorted_list[spec][state][country]
                if len(all_data) == 0:
                    continue
                all_group_name_set = set()
                for addr in all_data:
                    all_group_name_set.add(addr['GroupName'])

                group_name_sorted_list[spec][state].update({country: {}})
                for groupname in sorted(all_group_name_set):
                    group_name_sorted_list[spec][state][country][groupname] = []
                    d = all_country_sorted_list[spec][state][country]
                    for m in d:
                        if m['GroupName'] == groupname:
                            group_name_sorted_list[spec][state][country][groupname].append(m)

data_list = []
for k in group_name_sorted_list.keys():
    d = all_state_sorted_list[k]
    for f in d.keys():
        m = group_name_sorted_list[k][f]
        for w in m.keys():
            q = group_name_sorted_list[k][f][w]
            if len(q) == 0:
                continue
            for n in q.keys():
                v = group_name_sorted_list[k][f][w][n]
                for s in v:
                    data_list.append(s.values)
print(len(data_list))

address_sorted_list = {}
for spec, states in group_name_sorted_list.items():
    address_sorted_list.update({spec: {}})
    for state in states.keys():
        if len(group_name_sorted_list[spec][state]) == 0:
            continue
        address_sorted_list[spec].update({state: {}})
        for countries in states.values():
            for country in countries.keys():
                try:
                    if len(group_name_sorted_list[spec][state][country]) == 0:
                        continue
                    address_sorted_list[spec][state].update({country: {}})
                    for group in countries.values():
                        for gr_name in group.keys():
                            if len(group_name_sorted_list[spec][state][country][gr_name]) == 0:
                                continue
                            address_sorted_list[spec][state][country].update({gr_name:{}})
                            all_data = group_name_sorted_list[spec][state][country][gr_name]
                            if len(all_data) == 0:
                                continue
                            all_address_set = set()
                            for addr in all_data:
                                all_address_set.add(addr['AddressLine1'])

                            for gr in group.values():
                                for address in sorted(all_address_set):
                                    address_sorted_list[spec][state][country][gr_name][address] = []
                                    d = group_name_sorted_list[spec][state][country][gr_name]
                                    for m in d:
                                        if m['AddressLine1'] == address:
                                            address_sorted_list[spec][state][country][gr_name][address].append(m)

                except:
                    pass



data_list = []
for k in address_sorted_list.keys():
    d = address_sorted_list[k]
    for f in d.keys():
        m = address_sorted_list[k][f]
        for w in m.keys():
            q = address_sorted_list[k][f][w]
            if len(q) == 0:
                continue
            for n in q.keys():
                v = address_sorted_list[k][f][w][n]
                for s in v.keys():
                    r = address_sorted_list[k][f][w][n][s]
                    for t in r:
                        data_list.append(t.values)
print(len(data_list))



common_spealities = ['Ophthalmology']

dental_provider = ['Clinic/Center - Federally Qualified Health Center (Fqhc)', 'Dental Hygienist - Dental Hygienist',
                   'Dental Public Health', 'Dentist', 'Dentist Anesthesiologist', 'Endodontics', 'General Practice',
                   'Oral And Maxillofacial Surgery', 'Orthodontics And Dentofacial Orthopedics', 'Pediatric Dentistry',
                   'Periodontics']

vision_providers = ['Clinic/Center - Federally Qualified Health Center (Fqhc)',
                    'Eyewear Supplier (Equipment Not The Service) - Eyewear Supplier (Equipment Not The Service)',
                    'Multi-Specialty - Multi-Specialty',
                    'Ophthalmology - Glaucoma Specialist',
                    'Ophthalmology', 'Ophthalmology - Ophthalmology'
                                     'Ophthalmology Ophthalmic Plastic And Reconstructive Surgery',
                    'Ophthalmology Retina Specialist',
                    'Optometrist - Corneal And Contact Management',
                    'Optometrist - Optometrist',
                    'Psychiatry & Neurology - Neurology',
                    'Technician/Technologist - Ocularist',
                    'Technician/Technologist - Optician']

facilities = [
    'Clinic/Center - Federally Qualified Health Center (Fqhc)',
    'Eyewear Supplier (Equipment Not The Service) - Eyewear Supplier (Equipment Not The Service)',
    'Multi-Specialty - Multi-Specialty',
    'Ophthalmology - Glaucoma Specialist',
    'Ophthalmology',
    'Ophthalmology Ophthalmic Plastic And Reconstructive Surgery',
    'Ophthalmology Retina Specialist',
    'Optometrist - Corneal And Contact Management',
    'Optometrist - Optometrist',
    'Psychiatry & Neurology - Neurology',
    'Technician',
    'Technician/Technologist - Optician'
]

#group and address Sorted PCP
exist = False
if os.path.isfile(file_name):
    exist = True
with open(file_name, 'a+', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    for spec in address_sorted_list.keys():
        one_spec_data = address_sorted_list[spec]
        for state in one_spec_data.keys():
            one_state_data = one_spec_data[state]
            for one_county in one_state_data.keys():
                one_country_data = one_state_data[one_county]
                for group in one_country_data.keys():
                    one_group_data = one_country_data[group]
                    if len(one_group_data) == 0:
                        continue
                    for addresses in one_group_data.keys():
                        d = one_group_data[addresses]
                        for data in d:
                            if data['Source'] == 'PCP':
                                if not exist:
                                    writer.writerow(data.keys())
                                    exist = True
                                writer.writerow(data.values())

###PCP county sorted list
# exist = False
# if os.path.isfile(file_name):
#     exist = True
# with open(file_name, 'a+', encoding='utf-8', newline='') as file:
#     writer = csv.writer(file)
#     for spec in all_country_sorted_list.keys():
#         one_spec_data = all_country_sorted_list[spec]
#         for state in one_spec_data.keys():
#             one_state_data = one_spec_data[state]
#             for one_county in one_state_data.keys():
#                 d = one_state_data[one_county]
#                 for data in d:
#                     if data['PCPIndicator'] == 'PCP':
#                         if not exist:
#                             writer.writerow(data.keys())
#                             exist = True
#                         writer.writerow(data.values())

######### state sorted PCP

# exist = False
# if os.path.isfile(file_name):
#     exist = True
# with open(file_name, 'a+', encoding='utf-8', newline='') as file:
#     writer = csv.writer(file)
#     for key in all_state_sorted_list.keys():
#         for st, data in all_state_sorted_list[key].items():
#             for d in data:
#                 if d['PCPIndicator'] == 'PCP':
#                     if not exist:
#                         writer.writerow(d.keys())
#                         exist = True
#                     writer.writerow(d.values())

##################### Specialist
if os.path.isfile(file_name):
    exist = True
with open(file_name, 'a+', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    for spec in address_sorted_list.keys():
        one_spec_data = address_sorted_list[spec]
        for state in one_spec_data.keys():
            one_state_data = one_spec_data[state]
            for one_county in one_state_data.keys():
                one_country_data = one_state_data[one_county]
                for group in one_country_data.keys():
                    one_group_data = one_country_data[group]
                    if len(one_group_data) == 0:
                        continue
                    for addresses in one_group_data.keys():
                        d = one_group_data[addresses]
                        for data in d:
                            if (data['Source'] != 'PCP' and data['Source'] != 'BehavioralHealthSpecialist' and data['Specialty'] not in dental_provider and data[
                                'Specialty'] not in vision_providers and data['Specialty'] not in facilities and data[
                                    'Specialty'] != 'Pharmacy' and data['Source'] != 'NULL' and data['Source'] != 'Facility' and data[
                                    'Source'] != 'Null') or data['Specialty'] in common_spealities:
                                if not exist:
                                    writer.writerow(data.keys())
                                    exist = True
                                writer.writerow(data.values())

##################### Behavioral Specialist
if os.path.isfile(file_name):
    exist = True
with open(file_name, 'a+', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    for spec in address_sorted_list.keys():
        one_spec_data = address_sorted_list[spec]
        for state in one_spec_data.keys():
            one_state_data = one_spec_data[state]
            for one_county in one_state_data.keys():
                one_country_data = one_state_data[one_county]
                for group in one_country_data.keys():
                    one_group_data = one_country_data[group]
                    if len(one_group_data) == 0:
                        continue
                    for addresses in one_group_data.keys():
                        d = one_group_data[addresses]
                        for data in d:
                            if data['Source'] == 'BehavioralHealthSpecialist':
                                if not exist:
                                    writer.writerow(data.keys())
                                    exist = True
                                writer.writerow(data.values())



##################### dental_provider
if os.path.isfile(file_name):
    exist = True
with open(file_name, 'a+', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    for spec in address_sorted_list.keys():
        one_spec_data = address_sorted_list[spec]
        for state in one_spec_data.keys():
            one_state_data = one_spec_data[state]
            for one_county in one_state_data.keys():
                one_country_data = one_state_data[one_county]
                for group in one_country_data.keys():
                    one_group_data = one_country_data[group]
                    if len(one_group_data) == 0:
                        continue
                    for addresses in one_group_data.keys():
                        d = one_group_data[addresses]
                        for data in d:
                            if data['Specialty'] in dental_provider:
                                if not exist:
                                    writer.writerow(data.keys())
                                    exist = True
                                writer.writerow(data.values())

################ vision_providers
if os.path.isfile(file_name):
    exist = True
with open(file_name, 'a+', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    for spec in address_sorted_list.keys():
        one_spec_data = address_sorted_list[spec]
        for state in one_spec_data.keys():
            one_state_data = one_spec_data[state]
            for one_county in one_state_data.keys():
                one_country_data = one_state_data[one_county]
                for group in one_country_data.keys():
                    one_group_data = one_country_data[group]
                    if len(one_group_data) == 0:
                        continue
                    for addresses in one_group_data.keys():
                        d = one_group_data[addresses]
                        for data in d:
                            if data['Specialty'] in vision_providers:
                                if not exist:
                                    writer.writerow(data.keys())
                                    exist = True
                                writer.writerow(data.values())

########### facilities
if os.path.isfile(file_name):
    exist = True
with open(file_name, 'a+', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    for spec in address_sorted_list.keys():
        one_spec_data = address_sorted_list[spec]
        for state in one_spec_data.keys():
            one_state_data = one_spec_data[state]
            for one_county in one_state_data.keys():
                one_country_data = one_state_data[one_county]
                for group in one_country_data.keys():
                    one_group_data = one_country_data[group]
                    if len(one_group_data) == 0:
                        continue
                    for addresses in one_group_data.keys():
                        d = one_group_data[addresses]
                        for data in d:
                            if data['Specialty'] in facilities or data['Source'] == 'Facility':
                                if not exist:
                                    writer.writerow(data.keys())
                                    exist = True
                                writer.writerow(data.values())

# Pharmacy
if os.path.isfile(file_name):
    exist = True
with open(file_name, 'a+', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    for spec in address_sorted_list.keys():
        one_spec_data = address_sorted_list[spec]
        for state in one_spec_data.keys():
            one_state_data = one_spec_data[state]
            for one_county in one_state_data.keys():
                one_country_data = one_state_data[one_county]
                for group in one_country_data.keys():
                    one_group_data = one_country_data[group]
                    if len(one_group_data) == 0:
                        continue
                    for addresses in one_group_data.keys():
                        d = one_group_data[addresses]
                        for data in d:
                            if data['Specialty'] == 'Pharmacy':
                                if not exist:
                                    writer.writerow(data.keys())
                                    exist = True
                                writer.writerow(data.values())
