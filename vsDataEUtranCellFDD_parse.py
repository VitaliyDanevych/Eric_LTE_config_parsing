import os
import re

try:    # use C-compiled module for python 2.7 (3.3 will do that by default)
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

__AUTHOR__='Lifecell OSS group'
__COPYRIGHT__='Lifecell UA Company, 2018 Kiev, Ukraine'
__version__ = '1.2'
__license__ = "GPL"
__email__ = "oss_xxxx@lifexxxm.ua"
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
                                            cell_name = None
                                            physicalLayerSubCellId = None
                                            crsGain = None
                                            tac = None
                                            mobCtrlAtPoorCovActive = None
                                            physicalLayerCellIdGroup = None
                                            rachRootSequence = None
                                            cellId = None
                                            earfcndl = None
                                            pci = None
                                            for level9 in level8:
                                                key, value = level9.tag.replace('{EricssonSpecificAttributes.17.28.xsd}', ''), level9.text
                                                if key in target_parameters:
                                                    if key == 'physicalLayerSubCellId':
                                                        physicalLayerSubCellId = value
                                                    elif key == 'crsGain':
                                                        crsGain = value
                                                    elif key == 'tac':
                                                        tac = value
                                                    elif key == 'mobCtrlAtPoorCovActive':
                                                        mobCtrlAtPoorCovActive = value
                                                    elif key == 'sectorCarrierRef':
                                                        try:
                                                            matched = re.search(r'.+?vsDataSectorCarrier=([ERBS_]*?\w{2}\d{4}L\d{2})', value)
                                                        except TypeError as e:
                                                            print('TypeError occurs2', e)
                                                            print('Exception2!')
                                                        if matched:
                                                            cell_name = matched.group(1)
                                                            cell_name = cell_name.replace('ERBS_', '').strip()  # in case if we have to delete ERBS_ from the cell name
                                                    elif key == 'physicalLayerCellIdGroup':
                                                        physicalLayerCellIdGroup = value
                                                    elif key == 'rachRootSequence':
                                                        rachRootSequence = value
                                                    elif key == 'cellId':
                                                        cellId = value
                                                    elif key == 'earfcndl':
                                                        earfcndl = value
                                                        try:
                                                            pci = int(physicalLayerCellIdGroup)*3 + int(physicalLayerSubCellId)
                                                        except ValueError as e:
                                                            print('Error in convertation: ', str(e))
                                                            print('list_my2: ', list_my)
                                                            print('len2: ', len(list_my))
                                                        if (cell_name is not None) and (physicalLayerSubCellId is not None) and (crsGain is not None ) \
                                                        and (tac is not None) and (mobCtrlAtPoorCovActive is not None) and (physicalLayerCellIdGroup is not None) \
                                                        and (rachRootSequence is not None) and (cellId is not None) and (earfcndl is not None) and (pci is not None):
                                                            whole_line = cell_name + ';' + tac + ';' + cellId + ';' + earfcndl + ';' + physicalLayerCellIdGroup + ';' \
                                                            + physicalLayerSubCellId + ';' + str(pci) + ';' + rachRootSequence + ';' + crsGain + ';' + mobCtrlAtPoorCovActive
                                                            list_my.append(whole_line)
                                                            print('whole_line: ', whole_line)
                                                        #print('list_my3: ', list_my)
    return list_my


def main():
    in_file = 'vsDataEUtranCellFDD.xml'
    out_file = 'new_cm_exp4.csv'
    abs_out_file = os.getcwd() + os.sep + 'out' + os.sep + out_file
    if os.name == 'posix':
        abs_in_file = '/opt/optima/Interfaces/Configuration/ftp/in/' + in_file
    elif os.name == 'nt':
        abs_in_file = os.getcwd() + os.sep + 'in' + os.sep + in_file

    #below which exactly parameters must be found and parsed from XML file
    target_parameters = ['physicalLayerSubCellId', 'crsGain', 'tac', 'mobCtrlAtPoorCovActive', 'sectorCarrierRef', 'physicalLayerCellIdGroup', 'rachRootSequence', 'cellId', 'earfcndl']
    header = 'Name;TAC;CellId;earfcn;pci1;pci2;pci;prach;power;mobCtrlAtPoorCovActive'  #csv file header for sqlloader
    #sectorCarrierRef 260  mobCtrlAtPoorCovActive 244 physicalLayerCellIdGroup 276  rachRootSequence 278
    try:
        list_my = parseXML(abs_in_file, target_parameters)
    except TypeError as e:
        print('TypeError occurs', e)
        print('Exception!')

    savetoFILE(abs_out_file, header, list_my)


if __name__ == "__main__":
    main()
