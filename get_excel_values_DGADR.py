##################################################################
#
#     Developed by: Ana Isabel Oliveira
#     Project: OMEGA
#     Date: MARETEC IST, 01/02/2020
#     
#     Get values from excel file of DGADR
#
##################################################################

#!/usr/bin/python

import sys
import os
import urllib.request
import urllib
from bs4 import BeautifulSoup
import pandas
import numpy
import unicodedata
import glob

string_to_find = 'BOL_ALB_ATUALIZADO'
save_excel_file_as = 'excel_albufeiras.xlsx'
check_column = 'Cota do plano de água'
get_value_column = '(%)'
fout_name = 'PercentFullDGADR.txt'
emails = ['anaramosoliveira@tecnico.ulisboa.pt','lucian.simionesei@tecnico.ulisboa.pt','tiagobramos@tecnico.ulisboa.pt']

# Function to send emails
def send_email(receivers, message):

    user = 'hazrunoffmaretec@gmail.com'
    password = 'haz_run_off_0'

    header = "To: %s\n" % ','.join(receivers)
    header += "Subject: %s\n\n" % "Error reading reservoir data from DGADR."
    message = header + message
        
    try:
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com:465')
        server_ssl.ehlo()
        server_ssl.login(user,password)
        server_ssl.sendmail(user, receivers, message)
        server_ssl.close()
    
        print('Email sent.')
    
    except:
        print('Something went wrong...')

    return

############# MAIN FUNCTION #############
if __name__ == '__main__':

    if os.path.exists(fout_name):
        os.remove(fout_name)

    print ("Downloading file...")
    
    url = 'https://sir.dgadr.gov.pt/reservas'

    # Get data with BeautifulSoup
    data = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(data, features="html.parser")
    
    # Download file
    for link in soup.findAll('a'):
        link_to_get = link.get('href')
        if link_to_get is not None and string_to_find in link_to_get:
            success = urllib.request.urlretrieve('https://sir.dgadr.gov.pt' + link_to_get, save_excel_file_as)
            if not success:
                message = 'Error downloading file.'
                print (message)
                send_email(emails, message)
                sys.exit()

    df = pandas.DataFrame()
    xlfname = save_excel_file_as
    xl = pandas.ExcelFile(xlfname)
    sheets_list = xl.sheet_names
    try:
        sheets_list.remove('RESUMO')
        sheets_list.remove('GRÁFICOS')
    except:
        pass

    # Loop all sheets of excel
    for sheet in sheets_list:
        print ("        Working on " + sheet + ".")
        # Transform excel sheet to csv
        data_xls = pandas.read_excel(save_excel_file_as, sheet, index_col=None)
        data_xls.to_csv(sheet + '.csv', index=False)
        
        #Read csv
        fin = open(sheet + '.csv', 'r', encoding="utf-8")
        lines = fin.readlines()

        # Identify column index where the last line with record can be identified
        for l in lines:
            l_list = l.split(',')
            col_to_check = numpy.flatnonzero(numpy.core.defchararray.find(l_list,check_column)!=-1)
            if col_to_check.any():
                col_to_check = col_to_check[0]
                break
            
        # Identify last line with record
        lin = len(lines)-1
        for l in reversed(lines):
            l_list = l.split(',')
            try:
                value = float (l_list[col_to_check])
                lin_to_get = lin
            except:
                lin = lin - 1
                pass
            
        # Identify index of the column where to read percent full
        for l in lines:
            l_list = l.split(',')
            col_to_get = numpy.flatnonzero(numpy.core.defchararray.find(l_list,get_value_column)!=-1)
            if col_to_get.any():
                col_to_get = col_to_get[0]
                break

        # Prepare line to write
        line_to_write = sheet + '    ' + lines[lin_to_get].split(',')[col_to_get] + '\n'
        
        # Write output file with name of reservoir and percent full value
        if os.path.exists(fout_name):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not

        fout = open(fout_name,append_write)
        fout.writelines(line_to_write)
        fout.close()

        fin.close()
    
    # Close excel file
    xl = None
    
    # Clear all files
    os.remove(save_excel_file_as)
    
    filelist = glob.glob(os.path.join(os.getcwd(), "*.csv"))
    for f in filelist:
        os.remove(f)

    print ('Done!')