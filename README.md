# QueryDocs 💬

QueryDocs is a web application designed to enhance document analysis by intelligently retrieving relevant sentences based on user queries. Traditional search methods often miss nuanced information in documents, requiring exact keyword matches. QueryDocs overcomes this limitation using advanced sentence transformer models to identify contextually relevant sentences, even when specific keywords are absent.

<p align="center">
  <img src="https://github.com/KrishnakanthSrikanth/QueryDocs/blob/main/Images/Concept.gif" width="700">
</p>

## Features

- **Contextual Search:** Search for topics of interest without needing exact keyword matches.
- **Intelligent Analysis:** Utilizes advanced models to identify and extract relevant information.
- **Efficient Retrieval:** Presents a sorted list of the most pertinent sentences from uploaded documents.
- **User-Friendly Interface:** Simple upload interface with query input for seamless operation.

## How It Works

1. **Upload Document:** Upload your PDF document of interest.
2. **Enter Query:** Specify your query or topic, such as "sustainable practices"
3. **Retrieve Results:** QueryDocs scans the document, identifies contextually similar sentences, and presents them in a sorted list.

## Preview
The following image illustrates the real-time functionality of the QueryDocs App

![Preview](https://github.com/KrishnakanthSrikanth/QueryDocs/blob/main/Images/Preview.png)

## Installation

To set up the QueryDocs App on your local machine, follow these steps:

1. **Clone the repository**

```bash
git clone https://github.com/KrishnakanthSrikanth/QueryDocs.git
```
2. **Change Directory**

```bash
cd QueryDocs
```
3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the application**
   
```bash
python app.py
```

## Project Structure

```text
.
|-- README.md                                      # The main documentation file for the project
|-- app.py                                         # The main Flask application file
|-- images
|   |-- Concept.gif                                # Animated GIF illustrating the concept or workflow
|   |-- Preview.png                                # Preview image showing the main interface
|   `-- ProposedSolution.png                       # Image depicting the proposed solution or architecture
|-- input                                          # Directory for storing input files, such as PDFs
|-- notebooks
|   |-- MVP_V1_Analysis.ipynb                      # Jupyter Notebook for MVP version 1 analysis and development
|   |-- MVP_V2_Analysis.ipynb                      # Jupyter Notebook for MVP version 2 analysis and development
|   |-- POC_Analysis.ipynb                         # Jupyter Notebook for Proof of Concept (POC) analysis
|   |-- Regex_Analysis.ipynb                       # Jupyter Notebook for regex-based analysis
|   |-- Sentence_Parser_Analysis.ipynb             # Jupyter Notebook for sentence parser analysis
|   `-- Validation_Template.ipynb                  # Jupyter Notebook for validation template
|-- script.py                                      # Additional Python script for auxiliary functions
|-- static
|   `-- styles.css                                 # CSS file for styling the web application
`-- templates
    |-- login.html                                 # HTML template for the login page
    |-- pdfParser.html                             # HTML template for the PDF parser interface
    |-- registration.html                          # HTML template for the registration page
    `-- results.html                               # HTML template for displaying the results

6 directories, 17 files
```
## Contributing

Contributions to QueryDocs are welcome! Here's how you can contribute:

- Fork the repository
- Create your feature branch `git checkout -b feature/YourFeature`
- Commit your changes `git commit -am 'Add some feature'`
- Push to the branch `git push origin feature/YourFeature`
- Open a pull request

## Acknowledgements

QueryDocs would not be possible without the contributions of many open source projects:

- PyPDF
- PyTorch
- Flask
- Tesseract / PyTesseract
- Transformers and many others!

## License

This project is licensed under the [MIT license](./LICENSE.txt).

It contains code that is copied and adapted from [transformers](https://github.com/huggingface/transformers), which is Apache 2.0 licensed.
