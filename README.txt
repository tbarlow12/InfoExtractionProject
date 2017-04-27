This is my question-answering project for Information Extraction

This folder contains the source code that I wrote, as well as the datasets I used, but it leverages a few different external libraries, as documented in my technical design

--MY SOURCE CODE--
    /helpers - This is a Python module I created with helper functions required to support question answering.
    These helpers could be anything from reading a file to searching for RegEx matches to finding the Jaccard similarity of two sentences

    /questionAnswering - This is the Python module with the Question Answering algorithm I used. As mentioned above,
    I tried to encapsulate any methods/information non-essential to the algorithm inside the /helpers module and use it here

    test.py - Script to actually run the test for the accuracy of the question-answerer

--DATASETS--
    /datasets
        /train - Two datasets used in development (S08 and S09)
        /test - One dataset used only for testing (S10)

--RUNNING THE PROGRAM--

At runtime, the script fetches those libraries and uses them in the algorithm
To run the program with the development sets, type the following command into a CADE lab Linux terminal:

sh qa.sh

To run the program with the test set, type the following command into a CADE lab Linux terminal:

sh full.sh

I have tested to be sure that permissions are open for the necessary folders.
