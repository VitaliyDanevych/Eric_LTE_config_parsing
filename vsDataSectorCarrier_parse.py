import os
import re

try:    # use C-compiled module for python 2.7 (3.3 will do that by default)
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


__AUTHOR__='Lifecell OSS group'
__COPYRIGHT__='Lifecell UA Company, 2018 Kiev, Ukraine'
__version__ = '1.1'
__license__ = "GPL"
__email__ = "oss_group@lifecell.com.ua"
__status__ = "Production"


def savetoFILE(out_file, header, list_my):
    with open(out_file, 'w+') as f:
        f.write(header)
        f.write("\n")
        for each in list_my:
            f.write("%s" % each)
            f.write("\n")


def parseXML(xmlfile, target_parameters):
    """ XML parser function """
    with open(xmlfile, 'rt') as f:  ## open xml file for parsing
        try:
            tree = ET.parse(f)
            root = tree.getroot()
        except:
            print('It is unknown exception raised during xml parsing by ET module. The failed xml file: ', xmlfile)

        sites = set()  #set stores only uniq elements, avoid dublication in the result "my_list"
        list_my = []
        for child_of_root in root:
            for level1 in child_of_root:
                for level2 in level1:
                    for level3 in level2:
                        for level4 in level3:
                            for level5 in level4:
                                for level6 in level5:
                                    for level7 in level6:
                                        for level8 in level7:
                                            cell_name = None;
                                            noOfTxAntennas = None;
                                            maximumTransmissionPower = None;
                                            noOfRxAntennas = None
                                            for level9 in level8:
                                                key, value = level9.tag.replace('{EricssonSpecificAttributes.17.28.xsd}', ''), level9.text
                                                if key in target_parameters:
                                                    if key == 'noOfTxAntennas':
                                                        noOfTxAntennas = value.strip()
                                                    elif key == 'maximumTransmissionPower':
                                                        maximumTransmissionPower = value.strip()
                                                    elif key == 'noOfRxAntennas':
                                                        noOfRxAntennas = value.strip()
                                                    elif key == 'reservedBy':
                                                        try:
                                                            matched = re.search(r'.+?vsDataEUtranCellFDD=([ERBS_]*?\w{2}\d{4}L\d{2})', value)
                                                        except TypeError as e:
                                                            print('TypeError occurs2', e)
                                                            print('Exception22!')
                                                        if matched:
                                                            cell_name = matched.group(1)
                                                            cell_name = cell_name.replace('ERBS_', '').strip()  # in case if we have to delete ERBS_ from the cell name
                                                            if cell_name not in sites:
                                                                sites.add(cell_name)
                                                                if (cell_name is not None) and (noOfTxAntennas is not None) \
                                                                and (maximumTransmissionPower is not None) \
                                                                and (noOfRxAntennas is not None):
                                                                    whole_line = cell_name + ';' + maximumTransmissionPower + ';' + noOfTxAntennas + ';' + noOfRxAntennas
                                                                    list_my.append(whole_line)
                                                                    #print('len: ', str(len(list_my)), 'whole_line: ', whole_line)
    return list_my


def main():
    in_file = 'vsDataSectorCarrier.xml'
    out_file = 'new_cm_exp2.csv'
    abs_out_file = os.getcwd() + os.sep + 'out' + os.sep + out_file
    if os.name == 'posix':
        abs_in_file = '/opt/optima/Interfaces/Configuration/ftp/in/' + in_file
    elif os.name == 'nt':
        abs_in_file = os.getcwd() + os.sep + 'in' + os.sep + in_file

    #below which exactly parameters must be found and parsed from XML file
    target_parameters = ['reservedBy', 'maximumTransmissionPower', 'noOfTxAntennas',  'noOfRxAntennas']
    header = 'Name;totalpower;TxAnt;RxAnt'  #csv file header for sqlloader
    try:
        list_my = parseXML(abs_in_file, target_parameters)
    except TypeError as e:
        print('TypeError occurs', e)
        print('Exception!')

    savetoFILE(abs_out_file, header, list_my)


if __name__ == "__main__":
    main()