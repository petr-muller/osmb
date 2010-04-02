#!/usr/bin/python

import scenario

print "IMPORT:    PASS"

fact = scenario.CommandFactory()

print "CTOR:      PASS"

comm = fact.parseLine("alloc one 40 by 4")
comm = fact.parseLine("dealloc one")
comm = fact.parseLine("work read whole one seq")

print "PARSE:     PASS"

scen = scenario.Scenario()
fp = open("../scenarios/small-lot.alloc", "r")
scen.readFrom(fp)
fp.close()

print "FILE:      PASS"
