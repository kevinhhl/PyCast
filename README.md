# PyCast
 A tool that assists external auditors to perform casting on drafted AFSs

## What this program does:
- This program leverages on Tesseract-OCR and uses a trained dataset to recognize numbers from screenshots captured. It then outputs the total-sum. You are recommended to set your pdf viewer to size 130% - 150% for the program to perform optimally. As a fail-safe approach, before processing the input, the program will enlarge the screenshot at further zoom levels before performing OCR. Lastly it takes a look at the majority vote to see which results most likely depict the numbers in the original document.
