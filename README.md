# Practuce III - Document Similarity

In pursuit of the indications this code performs a searching process in order to find the most similar documents within a corpus given a document.  
To install all the required modules run:

> pip install -r requirements.txt

## How to run

Once the requirements are installed just run:

> streamlit run interfaz.py

You will get this tab open on you browser

![General viw](https://github.com/skoday/kindeyStone/blob/main/Screenshot%20from%202024-04-09%2019-46-25.png)

Now follow the following steps:
1. Upload a corpus in the indicated place
2. Set you documents, you can achive this in two differen ways:
   * Upload a text file in the second box. 
   * Write or paste a document in the textbox. 
   Either way using a line breaker means that a new document starts, so you can seach similarities for N documents.
3. Select your desired parameters
4. Press "Enviar"
5. If you wish to make all possible comparisons you can just ignore the parameters and directly press "Comparar todo"

Once the process is done a table with the results will de displayed under the button you pressed, simultaneously a pdf is also generated and opened using you default pdf viewer.

Note: if you want to use a txt file don't add anything in the text box and vice versa, if you want to use the text box dont attach a txt file.

