# Placeholder script

This script replaces common n-grams between source and target with a placeholder that can be configured in ner-placeholder.conf. The use case of this script is to generate synthetic data to train translation engines on to improve their placeholder handling.

You can use this script when you have python3 installed.

Best practice is to first create a virtual environment:

`python3 -m venv <name>`

Next you activate the environment using following command:

`source <name>/bin/activate`

Now you can install your dependencies in your virtual environment:

`python3 -m pip install -r requirements.txt`

To run the script you have to make sure the configuration file (ner-placeholder.conf) is in the same directory as the script. After pointing to your input and output files in the configuration, you can run the script by:

`python3 ner-placeholder.py`