##################################################################
#
#     Developed by: Ana Isabel Oliveira
#     Project: HazRunoff
#     Date: MARETEC IST, 10/01/2020
#     
#     Get values from HTML format from http://ceh-flumen64.cedex.es/
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

estacao = ['3006','3007','3008','3009','3013','3016','3019','3043','3050','3065','3066','3068','3069','3073','3074','3079','3111','3112','3113','3114','3115','3116','3127','3128','3141','3142','3143','3145','3148','3151','3152','3154','3155','3156','3157','3160','3166','3181','3189','3190','3191','3195','3196','3199','3201','3203','3208','3227','3247','3252','3257','3263','3264','3267','3285','3287','3300']
nome_estacao = ['ENTREPENAS','BOLARQUE','ZORITA','ALMOGUERA','PORTINA','TORREJON-TAJO','ALCANTARA','BUENDIA','VADO','PALMACES','ATANCE','BELENA','SANTILLANA','FINISTERRE','CASTRO','TAJERA','BURGUILLO','SANJUAN','PICADAS','CHARCODELCURA(PUENTENUEVO)','CAZALEGAS','MORALES','ROSARITO','TORREJON-TIETAR','GUIJODEGRANADILLA','GABRIELYGALAN','VALDEOBISPO','JERTE-PLASENCIA','BORBOLLON','CASTREJON','VALDECANAS','RIOSEQUILLO','PUENTESVIEJAS','ATAZAR','VELLON','RIVERADEGATA','TORCON','VALMAYOR','NAVACERRADA','JAROSA','NAVALMEDIO','VILLAR','PINILLA','NAVALCAN','MOLINODECHINCHA','AZUTAN','SALOR','ACENA','NAVAMUNO','GUAJARAZ','BUJEDA','PARDO','GUADILOBA','PORTAJE','CEDILLO','ALCORLO','BANOS']
anos = ['1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016']

############# MAIN FUNCTION #############
if __name__ == '__main__':
    
    for e in range(len(estacao)):
        to_write = []
        for ano in anos:
            print ('Working on station ' + estacao[e] + ', year ' + ano + '...')
            url = 'http://ceh-flumen64.cedex.es/anuarioaforos/afo/embalse-datos_dia.asp?ref_ceh=' + estacao[e] + '&ano_hidr=' + ano

            # Get data with BeautifulSoup
            data = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(data, features="html.parser")

            line_class = soup.find_all('td')
            for i in range(len(line_class)):
                line_text = line_class[i].text
                if re.match(r'(\d+/\d+/\d+)', line_text) is not None:
                    try:
                        date = re.findall(r'(\d+/\d+/\d+)', line_class[i].text)[0]
                        volume = re.findall(r'(\d+,\d+)', line_class[i+1].text)[0]
                        #outflow = re.findall(r'(\d+,\d+)', line_class[i+2].text)[0]
                        line_to_write = date + '    ' + volume.replace(',','.') + '\n'#volume.replace(',','.'), outflow.replace(',','.')
                        to_write.append(line_to_write)
                    except:
                        pass

        fin = open(estacao[e] + '_' + nome_estacao[e] + '.txt', 'w')
        fin.writelines('Station: ' + estacao[e] + '\n')
        for lin in to_write:
            fin.writelines(lin)
        fin.close()
    
    print ('Done!')