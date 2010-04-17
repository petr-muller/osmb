#!/usr/bin/python

import scenario

print "IMPORT:    PASS"

fact = scenario.CommandFactory()
scen = scenario.Scenario(threads=5)

wj1 = scenario.Workjob("wj1")
wj1.addCommand(fact.parseLine("alloc one 40 by 1"))
wj1.addCommand(fact.parseLine("alloc two 24 by 8"))
wj1.addCommand(fact.parseLine("alloc three 30"))
wj1.addCommand(fact.parseLine("work read whole one sequential"))
wj1.addCommand(fact.parseLine("work write whole two sequential"))
wj1.addCommand(fact.parseLine("work rw random three random"))
wj1.addCommand(fact.parseLine("work wr random three bacwards"))
wj1.addCommand(fact.parseLine("dealloc one"))
wj1.addCommand(fact.parseLine("dealloc two"))
wj1.addCommand(fact.parseLine("dealloc three"))

scen.addWorkjob(wj1)

scen.addThread(scenario.Thread(1, wj1, 1000))
scen.addThread(scenario.Thread(2, wj1, 500))
scen.addThread(scenario.Thread(3, wj1, 600))
scen.addThread(scenario.Thread(4, wj1, 700))
scen.addThread(scenario.Thread(5, wj1, 2000))

print "ASSIGN:    PASS"

scen.validate()
