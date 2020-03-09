from flask import Flask
from studystore import FindingFiveStudyStoreStudy

x = FindingFiveStudyStoreStudy.FindingFiveStudyStoreStudy(42, "hell0 world", "John Bald", 50, "the purpose of this is to show that we can do fun things", "references are not fun", "HCI", "usability", ["keyword1", "keyword2"], 10, 14, True, "15 minutes", 21, 5, "SUNY Oswego", "template1")
y = FindingFiveStudyStoreStudy.FindingFiveStudyStoreStudy(42, "hell1 world", "Tom", 51, "the purpose of this is to show that we can do fun things too", "references are not fun here either", "Social", "subcat", ["keyword3", "keyword4"], 11, 15, False, "10 minutes", 22, 2, "SUNY Oswego", "template2")
w = FindingFiveStudyStoreStudy.FindingFiveStudyStoreStudy(123456, "mystudies", "Nahyro", 123456, "to test", "my Dreams", "ISC", "science", ["key1", "key2", "key3"], 4,5, True,"30 minutes", 3, 3, "Oswego", "template3")
z = FindingFiveStudyStoreStudy.FindingFiveStudyStoreStudy(999999, "bop", "Tommy", 42, "this is a bop", "pls love me", "CSC", "science rulez", ["kw1", "kw2", "kw3"], 2, 15, True, "20 minutes", 4,5, "Webster", "Rubber Duck")