#!/usr/bin/env python
#_*_ coding:utf-8_*_

import os
import sys
import time

import dicom

reload(sys)
sys.setdefaultencoding('Cp1252')

#Desired fields
FIELD_NAMES = ["Institution Name"]
SECRET_FIELD = "************"
FILE_EXTENSION = ".dcm"


class Dicom(object):
    def __init__(self, path):
        self.path = path
        self.total_altered_files = 0

    def execute(self):
        self.log("\nCounting the number of DICOM files...")
        self.total_files = self._file_count()
        self.log("\nDone!")
        self.log("\nNumber of DICOM files: {}".format(self.total_files))

        topdir = self.path
        os.path.walk(topdir, self._step, FILE_EXTENSION)

    def _step(self, ext, dirname, names):
        """
        function used with os module to walk through directory tree
        to alter the desired fields
        """
        altered_files = 0
        for name in names:
            if name.lower().endswith(ext.lower()):
                file_name = os.path.join(dirname, name)
                self. _open_dicom(file_name)
                altered_files += 1
                total = self.total_altered_files + altered_files
                percentual = (total / float(self.total_files)) * 100
                self.log("\rAltered Files: {altered}/{total} - "
                         "{percent:3.2f}%".format(altered=total,
                         total=self.total_files, percent=percentual))
                self._save_dicom(file_name)

        self.total_altered_files += altered_files

    def log(self, message, to=sys.stdout):
        to.write(message)
        to.flush()

    def _file_count(self):
        """
        function used with os module to walk through directory tree
        and count the DICOM files
        """
        path = sys.argv[1]
        file_number = 0
        for information in os.walk(path):
            files = information[2]
            for file in files:
                if file.endswith(FILE_EXTENSION):
                    file_number += 1
        return file_number

    def _open_dicom(self, file_path):
        """
        Open DICOM file

        """
        self.dicom_file = dicom.read_file(file_path)

        #Execute a function inside each dicom
        self.dicom_file.walk(self._dicom_callback)

    def _save_dicom(self, file_name):
        """
        Save DICOM file
        """
        output_name, extension = file_name.split(FILE_EXTENSION)
        output_name = output_name + "_altered" + FILE_EXTENSION
        #self.dicom_file.save_as(output_name)

    def _dicom_callback(self, ds, data_element):
        """
            This function is executed with dicom object using walk method. It
            search for a Person Name (PN - Patient and Physician) using the PN
            tag and replace with ****************

        """
        #Hide the field that have PN tag
        if data_element.VR == "PN":
            data_element.value = SECRET_FIELD
        #Hide some other fields within FIELD_NAMES list
        if data_element.name.strip() in FIELD_NAMES:
            data_element.value = SECRET_FIELD
        #print data_element

if __name__ == '__main__':
    if len(sys.argv) - 1:
        topdir = sys.argv[1]

        start_time = time.time()
        dicom_object = Dicom(topdir)
        dicom_object.execute()
        dicom_object.log("\nElapsed Time: {:3.2f} minutes\n".
                         format(((time.time() - start_time) / 60)))
    else:
        print "You need to specify the path of directory"
