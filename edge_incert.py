import os
import pyorient
import json



def main():
    client = pyorient.OrientDB("localhost", 2424)

    client.connect("root", "12Krokodil")

    client.db_open("roads", "root", "12Krokodil")
    #
    #
    # client.command('CREATE PROPERTY E.formOfWay STRING')
    # #
    # client.command('CREATE PROPERTY E.directionality STRING')
    # # #
    # client.command('CREATE PROPERTY E.types STRING')
    # # #
    # client.command('CREATE PROPERTY E.geometry EMBEDDED OLineString')

    f = []

    for subdir, dirs, files in os.walk('Roadlink'):
        for file in files:
            f.append(os.path.join(subdir, file))

    loader(f[1:], client)









def loader(x, client):
    for i in x:
        json_data=open(i).read()
        data = json.loads(json_data)
        in_edge(data['features'], client)
        print 'Done   ' + i

#
# def coords(x):
#     s = '['+  str(x).replace('[', '').replace('],','').replace(']','') + ']'
#     return s




def in_edge(v, client):



    for i in range(0, len(v)):

        a = 'begin' + '; '
        b ='select from V where TOID =' + '"' + v[i]['properties']['startNode'] + '"'
        c = 'select from V where TOID =' + '"' + v[i]['properties']['endNode'] + '"'

        e ='create edge'+ ' ' + 'E' +' '+ 'from (' + b + ') to ('+ c +') '+'set formOfWay ='+ '"'\
           + v[i]['properties']['formOfWay']+ '"'+ ' ,'+ 'directionality = ' + '"'+ v[i]['properties']['directionality'] + '"'+ ' ,'+ 'geometry = ' + '{"@class": "OLineString","coordinates" :'+str(v[i]['geometry']['coordinates'])+'}'\
         #  +'; ' + "commit retry 100;"

        #print(e)
        try:
            client.command(e)
            print 'success!'
        except: print "exception"






main()