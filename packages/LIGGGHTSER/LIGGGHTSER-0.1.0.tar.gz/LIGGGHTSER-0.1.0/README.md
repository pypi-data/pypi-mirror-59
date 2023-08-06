LIGGGHTSER is a program that is able to automatically read data file printed or dumped by LIGGGHTS software.

Other funcitons are under developing.


Auther: Di

E-mail: wangdi931010@gmail.com

Github: https://github.com/DiWang1010

To read files:

import LIGGGHTSER
reader=LIGGGHTSER.read.Read()

#To get all files in directory
filedict=reader.read_file('./')

#To get dumpfile data
dumpdata=reader.read_dump('./dump10000.ouput')
print(dumpdata['id'])
print(dumpdata['type'])
pritn(dumpdata['x'])

#To read ave file
avedata=reader.read_ave('./ave_force.txt')
print(avedata['TimeStep'])

#To read thermo in log file
logdata=reader.read_log_thermo('./log.liggghts')
print(logdata['data1'])
print(logdata['data2'])
