# -*- coding: utf-8 -*-
"""
@author: kevinhhl
Date:    17 April 2020

Source code is publicly available on https://github.com/kevinhhl
"""
from PIL import ImageGrab
from pathlib import Path
import pytesseract
import os
# import time
# from PIL import Image
# from PIL import ImageChops

TESS_PATH = str(Path.home()) + r'\Tesseract-OCR\tesseract.exe'

DEFAULT_TRAINEDDATA = "digitsall_layer"
INDENT_MARGIN = " "*10                  #10 spaces

class PyCast:

    def __init__(self,debug_mode=False):
        self._count = 0
        self._debug_mode = debug_mode
        
        pytesseract.pytesseract.tesseract_cmd = TESS_PATH
        # Check for tesseract.exe's existence
        exeExists = os.path.exists(TESS_PATH)
        if not exeExists:
            input("\n (!) Error: Tesseract not found\n  Expected path={0}\n\nEnter Any Key to exit program...\n".format(TESS_PATH))
            raise Exception
        else:
            print("...loaded: " + TESS_PATH + "\n")

    # def __str__(self):
    #     return "{0}".format(self._str_casted_results)
    
    def _parseAndCollect(self, s, replace_period_dec=True) -> [float]:
        ''' A helper function for self.cast()
        This function parses string 's' received from tesseract OCR, parses it, and converts 
        all numbers within string 's' to floats, and stores them in a list collection for returning.
        
        Parameters
        ----------
        s                  : String, returned by tesseract, being our raw OCR data.
        
        replace_period_dec : boolean, optional
                             - Workaround for issue that OCR might classify "." as ","
                             - so say, image number is 100.00, and OCR outputs '100,00', this is referenced by 's' 
                                if argument is true, this function converts 's' to '100.00'
        Returns
        -------
        [float]  : list of the numbers to sum up by this PyCast when .cast() is called

        '''
        ### tokenize OCR results 's'
        tokens = []
        for t in s.split('\n'):
            tokens += t.split(' ')
        if self._debug_mode:
            print("tokens=" + str(tokens))

        ### Iteration through the tokens
        output = []
        for e in tokens:
            ## Workaround for issue that OCR might consider 100.00 as '100,00'
            if replace_period_dec:   
                e = e.replace('.',',')
        
                if len(e) > 1 and e[len(e)-2] == ',':
                    tmpL = list(e)
                    tmpL[len(e)-2] = '.'
                    e = "".join(tmpL)
                elif len(e) > 2 and e[len(e)-3] == ',':
                    tmpL = list(e)
                    tmpL[len(e)-3] = '.'
                    e = "".join(tmpL)
            
            ## Replacing all ',' with null string
            e = e.replace(',','')

            if e.startswith('(') and e.endswith(')'):   #Negative numbers '(e)' converted as as '-e'
                e = e.replace('(','')
                e = e.replace(')','')
                e = '-' + e

            ## Build output list
            try:                            
                output.append(float(e))
            except ValueError:# as err:
                if self._debug_mode:
                    print ("Could not convert non-numbers to float: " + e)
        if self._debug_mode:
            print("Output (list of parsed str -> floats)=" + str(output))

        return output

    def cast(self, zoom, train_data=DEFAULT_TRAINEDDATA) -> [[float], float, str]:
        '''
        Parameters
        ----------
        zoom       : integer, being the multipler that copied image will be enlarged by.
        
        train_data : the name of the .traineddata file that will be used for performing OCR via tesserract
                     The default is DEFAULT_TRAINEDDATA.
        Returns
        -------
        [[float], float, str] : 
                                0 = list of floats, being integers recognized by OCR.
                                1 = String representing the results to be printed out in terminal.
                                2 = string representation of results, for standard output purposes
        '''
        
        resultsList = self._helpFunction_cast(zoom, train_data)
        assert len(resultsList) == 3        
        return resultsList
    
    def _helpFunction_cast(self, zoom, train_data) -> [[float], float, str]:
        ''' This is a helper function to the function above.
        '''
        ### Step 1: Process image data into num_list
        num_list = None
        img = ImageGrab.grabclipboard()
        imgSize = img.size
        img_zoomed = img.resize((int(imgSize[0]*zoom), int(imgSize[1]*zoom)))

        strInput = pytesseract.image_to_string(img_zoomed, lang=train_data)
        if self._debug_mode:
            tmp = strInput.replace('\n', ";  ")
            print("Raw input = {\n" + tmp + "\n}\n")

        num_list = self._parseAndCollect(strInput)

        ### Step 2: Build the output sum based on num_list
        str_casted_results = "\nOCR @Zoom={0}x\n".format(zoom)
        casted_sum = 0
        if self._debug_mode:
            print("Parsed input:\n[{0}.traineddata]".format(train_data))
        for e in num_list:
            casted_sum += e
            str_casted_results += f"{e:,.2f}\n"
            
        str_casted_results += ("{0}--------------------\n{0}".format(INDENT_MARGIN) \
            + f"{casted_sum:,.2f}\n" + "{0}====================".format(INDENT_MARGIN))
        
        #self._img = None #clean up
        strRepOut = self._formatCastedResults(str_casted_results)
        self._count += 1
        return [num_list, casted_sum, strRepOut]


    def _formatCastedResults(self, unformattedStr) -> str:
        ''' This is a helper function to the function above.

        Parameters
        ----------
        unformattedStr : string
            DESCRIPTION.

        Returns
        -------
        str
            Formatting the raw unformattedStr to, for example: 
            if casted "1k + 2k", this function will return:
            '    1,000
                 2,000
               -------
                 1,000
               ======='
        '''
        lines = unformattedStr.split("\n")
        max_ln_length = 0
        for ln in lines:
            if len(ln) > max_ln_length:
                max_ln_length = len(ln)
        
        formatted_results = ""
        counter = 0
        for ln in lines:
            # Align all lines, excpet the line ["OCR @Zoom X"]
            if counter == 1: #first line is empty line of "\n", so not 0
                formatted_results += ln
            else:
                formatted_results += ln.rjust(max_ln_length," ")

            formatted_results += "\n"
            counter += 1
        return formatted_results    

    # def get_cast_count(self):
    #     """ Returns the number of times that this instance of PyCast has performed casting
    #     """
    #     return self._count
