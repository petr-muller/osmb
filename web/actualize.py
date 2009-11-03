#!/usr/bin/python

fp = open("shortlog")
cont = fp.read()
fp.close()

fp = open("index.html.template", 'r')
cont2 = fp.read()
fp.close()

fp = open("index.html", "w")
cont2 = cont2.replace("RECACT PLACEHOLDER", cont)
fp.write(cont2)
fp.close()
