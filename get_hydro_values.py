##################################################################
#
#     Developed by: Ana Isabel Oliveira
#     Project: HazRunoff
#     Date: MARETEC IST, 19/07/2018
#
##################################################################

#!/usr/bin/python

import sys
import os
import re
import difflib
import calendar
import numpy as np
import urllib.request
from bs4 import BeautifulSoup

#M3323010 - L'Ernée à Andouillé
#M5300010 - La Loire à Montjean-sur-Loire
#M5222010 - Le Layon à Saint-Lambert-du-Lattay
#K4080010 - La Loire à Saint-Satur
#K1930010 - La Loire à Nevers


estacao = 'K1930010'
nome_estacao = 'Loire_A_Nevers'
anos = ['2008','2009','2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']
meses = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet',\
         'Août','Septembre','Octobre','Novembre','Décembre']



############# MAIN FUNCTION #############
if __name__ == '__main__':
    
    to_write = []
    for ano in anos:
        print ('Working on year ' + ano + '...')
        url = 'http://www.hydro.eaufrance.fr/stations/' + estacao + '&procedure=qjm&annee=' + ano

        # Get data with BeautifulSoup
        data = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(data, features="html.parser")

        i = 1
        for mes in meses:
            month_class = soup.find_all('h3')

            max = 0
            for mon in month_class:
                sequence = difflib.SequenceMatcher(lambda x: x == " ", mes, str(mon))
                difference = sequence.ratio()
                if difference > max:
                    max = difference
                    m_index = month_class.index(mon)
            
            h3_parent = month_class[m_index].parent()
            data = h3_parent[1].text
            data_splitted = re.split('\n+', data)

            days_in_month = calendar.monthrange(int(ano),i)[1]
            for day in range(1,days_in_month+1):
                try:
                    day_index = data_splitted.index(str(day).zfill(2))
                    value = float(data_splitted[day_index+1])
                    previous_index = day_index
                except:
                    value = -9999

                to_write.append(str(np.datetime64(ano + '-' + str(i).zfill(2) + '-' + str(day).zfill(2))) + ', ' + str(value) + '\n')

            i = i + 1
            
    fin = open(estacao + '_' + nome_estacao + '.txt', 'w')
    fin.writelines('Station: ' + estacao + '\n')
    for lin in to_write:
        fin.writelines(lin)
    fin.close()
    
    print ('Done!')