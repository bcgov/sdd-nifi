#!/usr/bin/python3

import os
import re
import uuid
from tableschema import Table
from tableschema import exceptions
from datetime import datetime
import dateutil.parser as parser

class DIPSeparator:
    IDENTITY_FIELD = 'var_class'
    DIRECT_IDENTIFIER = 'direct_identifier'
    INDIRECT_IDENTIFIER = 'indirect_identifier'
    INGESTIONID_COLUMN_NAME = 'IngestionID'

    def __makeFolder(self, directoryPath):
        if not os.path.exists(directoryPath):
            os.makedirs(directoryPath)

    def __getHeader(self, fields):
        header = ""
        for fieldName in fields:
            header += fieldName + ","
        header = header[0:len(header) -1]
        return header


    def __writeFileContents(self, table, idFile, contentFile, idFields, contentFields, indirectFields):
        for keyed_row in table.iter(keyed=True, cast=False):
            idLine = contentLine = str(uuid.uuid1()) + ","
            for key, value in keyed_row.items():
                fieldName = table.schema.get_field(key).name
                isDatetime = False
                try:
                    index = indirectFields.index(fieldName)
                    val = str(value)
                    if re.match('[A-Za-z]\d[A-Za-z] ?\d[A-Za-z]\d',val): 
                        idLine += val.upper().replace(" ", "") + ","
                        contentLine += val[0:3].upper() + ","
                    else:
                        idLine += val + ","
                        isDatetime = True
                        cl = parser.parse(val).strftime('%Y-%m') + ","
                        contentLine += cl
                    continue
                except ValueError:
                    if isDatetime:
                        contentLine += "unknown datetime,"
                        continue
                    else:
                        # not in array
                        noop = True
                try:
                    index = idFields.index(fieldName)
                    idLine += str(value) + ","
                except ValueError:
                    # not in array
                    noop = True
                try:
                    index = contentFields.index(fieldName)
                    contentLine += str(value) + ","
                except ValueError:
                    # not in array
                    noop = True

            idLine = idLine[0:len(idLine) - 1]
            idLine += "\n"
            idFile.write(idLine)

            contentLine = contentLine[0:len(contentLine) - 1]
            contentLine += "\n"
            contentFile.write(contentLine)


    def separate(self, table, filename):
        directory = "."+os.sep+"output"
        identifiersFilename = filename + "-identifiers.csv"
        contentFilename = filename + "-contentFile.csv"

        self.__makeFolder(directory)

        idFile = open(directory + os.sep + identifiersFilename, 'w')
        contentFile = open(directory + os.sep + contentFilename, 'w')

        idFields = [self.INGESTIONID_COLUMN_NAME]
        contentFields = [self.INGESTIONID_COLUMN_NAME]
        indirectFields = []
        
        for field in table.schema.descriptor['fields']:
            fieldName = field['name']
            
            if ((self.IDENTITY_FIELD in field) and (field[self.IDENTITY_FIELD].lower() == self.DIRECT_IDENTIFIER)):
                idFields.append(fieldName)
            elif ((self.IDENTITY_FIELD in field) and (field[self.IDENTITY_FIELD].lower() == self.INDIRECT_IDENTIFIER)):
                indirectFields.append(fieldName)
                idFields.append(fieldName)
                contentFields.append(fieldName)
            else:
                contentFields.append(fieldName)
        
        idFile.write(self.__getHeader(idFields)+"\n")
        contentFile.write(self.__getHeader(contentFields) + "\n")

        self.__writeFileContents(table, idFile, contentFile, idFields, contentFields, indirectFields)

        idFile.close()
        contentFile.close()

        return [directory+os.sep+identifiersFilename, directory+os.sep+contentFilename]
