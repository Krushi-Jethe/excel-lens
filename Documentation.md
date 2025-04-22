# Excel Lens

## Data Processors: processors.py

Cell data processors (Pandas/openpyxl)

- Multiple sheets present within the file.
- Multiple tables present in a single sheet.
- Final data should include all tables present in the excel file. Dynamic assignment of variables might be needed.
- Image and chart processors (openpyxl)
- The data i.e.  pictures, charts, links will be loaded using openpyxl.
- Tables can be processed using pandas.
- Use @dataclass decorator to create a data class which will holds tables, images, charts, urls or any other components from the excel file.

## Prompts config: prompts.py

Prompts should first understand what kind of processing is expected and then generate a code. 
1. If mathematical - numpy/pandas/math/sklearn
2. If plot/chart - seaborn or matplotlib
3. Arithmetic – add, subtract, multiply, divide, exponent, square root
4. Statistical – mean, median, mode, variance, standard deviation
5. Geometric and Trigonometric – sine, cosine, tangent etc.
6. Code generation could be for mathematical processing or to obtain any graphs/charts.
7. Check for the possibility of getting data from URLs and summarize them.
<br>
</br>

- The generated code will be executed using python builtin exec(). A safer option is RestrictedPython as it blocks unsafe commands from being executed.
  
  `code = "a = 5\nb = 10\nc = a + b"; exec(code)`
- Exploration of LangChain and agents - [create_pandas_dataframe_agent](https://python.langchain.com/api_reference/experimental/agents/langchain_experimental.agents.agent_toolkits.pandas.base.create_pandas_dataframe_agent.html)
- Mathematical processing could be done using pandas, if simple linear regression is expected we may include scikit-learn as well.
- For charts/plots matplotlib/seaborn can be utilized.
- Utilize re to process prompt output.
- The generated code can cause errors - prompt again with generated code, error and let LLM rewrite the code.
- Expecting a LLM to write a large chunk of code would be more prone to errors, split the problem and prompt to write the chunks of code and get everything together. 

## LLM pipeline: model.py, inference.py

1. **Text2Text**: Multiple models tailored for specific prompts since one prompt might work well with one model but perform poorly with one model.
2. **Image2Text**: Try out current lightweight Visual Q/A models.
   - Is there a need to perform OCR and pass it along with the image to the Visual Q/A model?
   - OCR would give context i.e. the title of the plot, what's present on X, Y axis and the values.
- Try different quantizations bf16, f16, f32.
- To save memory dynamically load models based on the prompt to be used and delete from memory once it is done.
- Deletion should be done only after receiving the next prompt and it is confirmed that the next prompt won’t require the current model.

## Data post processing: postprocessor.py
TBD after experimentation.

## UI: Streamlit app 
1. Upload button to upload excel file.
2. The uploaded excel components should be displayed consisting of tabs which are fetched from data class:
   1. Tables
   2. Images
   3. Charts
   4. URLs
   
Prompt chat window – To type questions/prompts and get responses. A dropdown within the prompt window to select the table/chart/image to use. 


## Package
TBD - .whl/.toml/setup.py/dockerfile

Demo colab notebook

## Coding
- Code formatter: black formatter and pylint.
- Docstrings: autoDocstring – Python Docstring Generator (Nils Werner) if using VSCode.
- Jupyter notebooks to be placed under the notebooks directory.
     
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`%load_ext jupyter_black` to be run in 1st block of code  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Naming –  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[num]-[name]-[exp_name].ipynb  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;E.g. 001-kj-cell-data-processing.ipynb

    
 `from IPython.display import Markdown, display`

## Data sources for testing
https://github.com/bharathirajatut/sample-excel-dataset

https://github.com/microsoft/powerbi-desktop-samples/tree/main/powerbi-service-samples

https://catalog.data.gov/dataset/18-excel-spreadsheets-by-species-and-year-giving-reproduction-and-growth-data-one-excel-sp

https://www.thespreadsheetguru.com/sample-data/

https://marcus-small.squarespace.com/ebit-dashboard



