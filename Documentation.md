Excel Lens
—------------------------------------------------------------------------------------------------------------------
Data Processors: processors.py
—------------------------------------------------------------------------------------------------------------------
Cell data processors (Pandas/openpyxl)
Multiple sheets present within the file. 
Multiple tables present in a single sheet.
Final data should include all tables present in the excel file. Dynamic assignment of variables might be needed.
Image and chart processors (openpyxl)
The data i.e.  pictures, charts, links will be loaded using openpyxl. 
Tables can be processed using pandas.
Use @dataclass decorator to create a data class which will holds tables, images, charts, urls or any other components from the excel file.
—------------------------------------------------------------------------------------------------------------------
Prompts config: prompts.py
—------------------------------------------------------------------------------------------------------------------
Prompts should first understand what kind of processing is expected and then generate a code. 
If mathematical - numpy/pandas/math/sklearn
If plot/chart - seaborn or matplotlib
Arithmetic – add, subtract, multiply, divide, exponent, square root
Statistical – mean, median, mode, variance, standard deviation
Geometric and Trigonometric – sine, cosine, tangent etc.
Code generation could be for mathematical processing or to obtain any graphs/charts.
Check for the possibility of getting data from URLs and summarize them.
 The generated code will be executed using python builtin exec(). A safer option is RestrictedPython as it blocks unsafe commands from being executed.
 code = "a = 5\nb = 10\nc = a + b"; exec(code)
Mathematical processing could be done using pandas, if simple linear regression is expected we may include scikit-learn as well. For charts/plots matplotlib/seaborn can be utilized.
The generated code can cause errors - prompt again with generated code, error and let LLM rewrite the code.
Expecting a LLM to write a large chunk of code would be more prone to errors, split the problem and prompt to write the chunks of code and get everything together. 

—------------------------------------------------------------------------------------------------------------------
LLM pipeline: model.py, inference.py
—------------------------------------------------------------------------------------------------------------------
Text2Text: 
Multiple models tailored for specific prompts since one prompt might work well with one model but perform poorly with one model.
Try different quantizations bf16, f16, f32.
To save memory dynamically load models based on the prompt to be used and delete from memory once it is done.
Deletion should be done only after receiving the next prompt and it is confirmed that the next prompt won’t require the current model.
Image2Text:
Try out current lightweight Visual Q/A models.
Is there a need to perform OCR and pass it along with the image to the Visual Q/A model? OCR would give context i.e. the title of the plot, what's present on X, Y axis and the values.

—------------------------------------------------------------------------------------------------------------------
Data post processing: postprocessor.py
—------------------------------------------------------------------------------------------------------------------
TBD after experimentation.






—------------------------------------------------------------------------------------------------------------------
UI: Streamlit app 
—------------------------------------------------------------------------------------------------------------------
Upload button to upload excel file.
The uploaded excel components should be displayed consisting of tabs which are fetched from data class:
Tables
Images
Charts
URLs
Prompt chat window – To type questions/prompts and get responses. A dropdown within the prompt window to select the table/chart/image to use. 

—------------------------------------------------------------------------------------------------------------------
Package
—------------------------------------------------------------------------------------------------------------------
TBD - .whl/.toml/setup.py/dockerfile


—------------------------------------------------------------------------------------------------------------------
Coding
—------------------------------------------------------------------------------------------------------------------
Code formatter: black formatter and pylint.
Docstrings: autoDocstring – Python Docstring Generator (Nils Werner) if using VSCode.
Jupyter notebooks to be placed under the notebooks directory.
Naming – 
[num]-[name]-[exp_name].ipynb
E.g. 001-kj-cell-data-processing.ipynb
from IPython.display import Markdown, display


—------------------------------------------------------------------------------------------------------------------
Data
—------------------------------------------------------------------------------------------------------------------
https://github.com/bharathirajatut/sample-excel-dataset
https://github.com/microsoft/powerbi-desktop-samples/tree/main/powerbi-service-samples
https://catalog.data.gov/dataset/18-excel-spreadsheets-by-species-and-year-giving-reproduction-and-growth-data-one-excel-sp
https://www.thespreadsheetguru.com/sample-data/
https://marcus-small.squarespace.com/ebit-dashboard



