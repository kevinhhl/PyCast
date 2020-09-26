# PyCast
 A tool that assists external auditors, and corporate accountants in group reporting practices, to perform casting on drafted financial statements

## Times when you need PyCast:
- It's that time of the year when a PIE needs to issue their FS for annual/interim reporting purposes. During this process, there will be a copywriter involved who will likely provide you the latest version of the typesets in .pdf format. Although your teammembers have checked the tracked changes multiple times and are monitoring changes closely, you will still need to perform a full tie-cast-check on the entire FS to obtain a level of comfort that all sections can tie out.
- This program leverages on Tesseract-OCR and uses a trained dataset to recognize numbers from screenshots captured. It then outputs the total-sum. You are recommended to set your pdf viewer to size 130% - 150% for the program to perform optimally. As a fail-safe approach, before processing the input, the program will enlarge the screenshot at further zoom levels before performing OCR. Lastly it takes a look at the majority vote to see which results most likely depict the numbers in the original document.
