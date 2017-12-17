# Wordpress to PDF

This is a tiny tool to turn your wordpress xml export into a printable PDF.

## Getting the export
There is a guide by wordpress.com that shows you step by step how to export the necessary xml file:

## Running the script
First you have to install all dependencies with:

    pip install -r requirements.txt

Now you can run the script with:

    python3 wordpress_to_pdf.py path/to/wordpress.xml path/to/out.pdf

To see all available options (like headline color or font) run:

    python3 wordpress_to_pdf.py --help