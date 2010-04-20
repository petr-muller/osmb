#!/usr/bin/python

import osmb
import sys

if __name__ == '__main__':
  fp = open(sys.argv[1], 'r')
  scen = osmb.scenario_parser.parseScenario(fp)
  fp.close()
  
  scen.validate()
  
  if scen.isValid():
    print scen.translateToC()
  else:
    printed = []
    for message in scen.getMessages():
      if message not in printed:
        printed.append(message)
        print message