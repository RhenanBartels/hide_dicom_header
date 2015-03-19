#!/usr/bin/env python
#_*_ coding:utf-8_*_

import os
import sys
import time

import dicom

reload(sys)
sys.setdefaultencoding('Cp1252')

FIELD_NAMES = ["PatientName"]
SECRET_FIELD = "************"
FILE_EXTENSION = ".dcm"


class Dicom():
    def __init__(self, path):
        self.path = path
        self.total_altered_files = 0

        print("Counting the number of .dcm files...")
        self.total_files = self._file_count()
        print("Done!")
        print("Number of DICOM files: " + str(self.total_files))

    def execute(self):
        topdir = self.path
        os.path.walk(topdir, self._step, FILE_EXTENSION)

    def _step(self, ext, dirname, names):
        """
        function that is used with os module to walk through directory tree
        """
        altered_files = 0
        for name in names:
            if name.lower().endswith(ext.lower()):
                file_name = os.path.join(dirname, name)
                self. _open_dicom(file_name)
                altered_files += 1
                total = self.total_altered_files + altered_files
                sys.stdout.write("\rAltered Files: %d/%d  - %3.2f%%" %
                                 (total, self.total_files,
                                  (total / float(self.total_files)) * 100))
                sys.stdout.flush()
        self.total_altered_files += altered_files

    def _file_count(self):
        """
        function that is used with os module to walk through directory tree
        """
        path = sys.argv[1]
        directories = file_number = 0

        for information in os.walk(path):
            files = information[2]
            for file in files:
                if file.endswith(FILE_EXTENSION):
                    file_number += 1
        return file_number

    def _open_dicom(self, file_path):
        """
        Open dicom file

        """
        dicom_file = dicom.read_file(file_path)

        #Execute a function inside each dicom
        dicom_file.walk(self._dicom_callback)

    def _dicom_callback(self, ds, data_element):
        """
            This function is executed with dicom object using walk method. It
            search for a Person Name (PN - Patient and Physician) using the PN
            tag and replace with ****************

        """
        #Every field related to Names (physician or patient)
        #have the PN tag
        if data_element.VR == "PN":
            pass
            #data_element.value = SECRET_FIELD


if __name__ == '__main__':
    topdir = sys.argv[1]
    start_time = time.time()
    dicom_object = Dicom(topdir)
    dicom_object.execute()
    print "\nElapsed Time: %s minutes" % ((time.time() - start_time) / 60)
