"""Export a notebook as a PDF for manual grading.

Adapted from https://github.com/dibyaghosh/gsExport
"""

from IPython.core.display import display, HTML
from nbconvert import PDFExporter #, HTMLExporter, LatexExporter
from tqdm import tqdm

import glob
import hashlib
import nbconvert
import nbformat
import os
import pkg_resources
import re
import shutil
import copy
import pathlib


def generate_pdf_cmdline(nb_path, pdf_path):
    """Generate a PDF (used from the command line)"""
    filtered = load_and_filter(nb_path)
    export_notebook(filtered, pdf_path)


def generate_pdf(nb_path, pdf_path, **kwargs):
    """Generate a PDF (called from a notebook)"""
    assert run_from_ipython(), "You must run this from within a notebook"
    print("Generating PDF...")
    filtered = load_and_filter(nb_path)
    success = export_notebook(filtered, pdf_path, **kwargs)
    # TODO check if the PDF is too short.
    if not success:
        display(HTML(
            "<h2>Export to PDF failed. Read the error above, fix it, SAVE, and try again!</h2>"
            "<h3>Running each cell individually to locate the problem...</h3>"
            ))
        cell_by_cell(nb_path)


def cell_by_cell(nb_path):
    assert run_from_ipython(), "You must run this from within a notebook"
    filtered = load_and_filter(nb_path)
    temp_nb = filtered.copy()

    for cell in tqdm(filtered.cells):
        if cell['cell_type'] == 'code':
            continue
        temp_nb.cells = [cell]
        error = has_error(temp_nb)

        if error is not None:
            print("""

            There is an error with the following cell:
            ==========================================================================

            %s

            ==========================================================================
            Here's the error message we were able to extract

            %s

            ==========================================================================
            """%(cell['source'],str(error)))


QUESTION_TAG = re.compile(r"\s*<!--\s*EXPORT TO PDF\s*(format:(image))?\s*-->\s*")
NUM_QUESTIONS_TAG = re.compile(r"\s*<!--\s*EXPECT (\d+) EXPORTED QUESTIONS\s*-->\s*")
MATH_EXP = re.compile(r"\$[^$]+\$")
ANY_QUESTION_TAG = re.compile(r"BEGIN QUESTION") #This looks for both manual and autograded questions

def is_question_cell(cell):
    # Check if this is cell is a manually graded question
    return (cell['cell_type'] == 'markdown' and
            bool(QUESTION_TAG.search(cell['source'])))

def is_any_question_cell(cell):
    # Check if this cell is a manually or autograded question
    return (cell['cell_type'] == 'markdown' and
            bool(ANY_QUESTION_TAG.search(cell['source'])))    


def question_format(cell):
    """Return a format restriction if there is one, otherwise a false value."""
    _, format = QUESTION_TAG.search(cell['source']).groups()
    return format


def load_and_filter(nb_path):
    nb = nbformat.read(nb_path, nbformat.current_nbformat)
    check_num_questions(nb)
    return filter_nb(nb)


def fix_dollar_sign_in_source(cell):
    if 'cell_type' in cell and cell['cell_type'] == 'markdown':
        cell['source'] = fix_dollar_sign(cell['source'])


def fix_dollar_sign(source):
    return MATH_EXP.sub(strip_dollar_sign, source)


def strip_dollar_sign(match):
    return match.group(0).replace('$ ','$').replace(' $','$')


def paraphrase(text,fromBegin=3,fromEnd=3):
    numLines = text.count('\n')
    if numLines < fromBegin + fromEnd:
        return text
    textSplit = text.split('\n')
    newParts = (textSplit[:fromBegin] +
                ['... Omitting %d lines ... ' % (numLines-fromBegin-fromEnd)] +
                textSplit[-1*fromEnd:])
    return '\n'.join(newParts)


def clean_cells(cells):
    """Clean cells in place."""
    for cell in cells:
        if 'outputs' in cell:
            # Paraphrase output
            for output in cell['outputs']:
                if output.get('output_type', 'NA') == 'stream' and 'text' in output:
                    output['text'] = paraphrase(output['text'])
                if output.get('output_type','NA') == 'execute_result':
                    if 'data' in output and 'text/plain' in output['data']:
                        output['data']['text/plain'] = paraphrase(output['data']['text/plain'])
                if output.get('output_type', 'NA') == 'error' and 'traceback' in output:
                    output['traceback'] = output['traceback'][:1]

        if 'source' in cell and (cell['source'].count('\n') > 60 or len(cell['source']) > 8000):
            print('This cell has a lot of content! Perhaps try to shorten your response. ')
            print("\n\n\n", cell['source'][:200])

        fix_dollar_sign_in_source(cell)


def check_num_questions(nb):
    """Check that the number of questions that appear is the number expected."""
    num_questions = len([cell for cell in nb['cells'] if is_question_cell(cell)])
    expected_tags = [NUM_QUESTIONS_TAG.search(cell['source']) for cell in nb['cells']]
    num_expecteds = [int(m.group(1)) for m in expected_tags if m]
    if num_expecteds:
        num_expected = num_expecteds[0]
        assert all(n == num_expected for n in num_expecteds[1:]), 'conflicting num expected'
        assert num_expected == num_questions,(
            "The number of questions (%d) is different than the expected number (%d). "
            "Did you accidentally delete a question?") % (num_questions, num_expected)


def filter_nb(nb):
    """Returns the parts of nb tagged for export and a list of question metadata."""
    new_cells = []
    for i, cell in enumerate(nb['cells']):
        if is_question_cell(cell):
            src = str(cell["source"])
            assert len(nb['cells']) > i + 1, 'A response cell must follow question cell ' + src
            assert not is_question_cell(nb['cells'][i+1]), 'Two question cells in a row after ' + src
            # Append both the question and subsequent cells to our eventual pdf
            # We stop either at the end of the file, or until the next question starts
            """
            new_cells.append(cell)
            for j in range(i+1, len(nb['cells'])):
                next_cell = nb['cells'][j]
                if is_any_question_cell(next_cell):
                    break
                new_cells.append(next_cell)
            """
            # Jasign only looks at the next cell.
            # Disadvantage: miss students that mess up a little bit 
            # Advantage: Much greater chance of outputs being the same length
            response = nb['cells'][i + 1]
            if question_format(cell) == 'image':
                assert any(k.startswith('image') for
                           o in response.get("outputs", {}) for
                           k in o.get("data", {}).keys()), 'Image required after ' + src
            elif response['cell_type'] == 'markdown':
                response['cell_type'] = 'raw'
            new_cells.append(cell)
            new_cells.append(response)
            

    clean_cells(new_cells)
    filtered = nb.copy()
    filtered['cells'] = new_cells
    return filtered


def export_notebook(nb, pdf_path, template="test.tplx", debug=True):
    """Write notebook as PDF to pdf_path. Return True on success or False on error."""
    shutil.copyfile(pkg_resources.resource_filename(__name__, template), "test.tplx")
    pdf_exporter = PDFExporter()
    pdf_exporter.template_file = "test.tplx"
    
    #html_exporter = HTMLExporter()
    #latex_exporter = LatexExporter()
    #latex_exporter.template_file = "test.tplx"
    #html_exporter.template_file = "ds100_html_template.tpl"
    try:
        #html_output = html_exporter.from_notebook_node(nb)
        #html_tester = open(pdf_path + ".html", 'w')
        #html_tester.write(html_output[0])

        #latex_output = latex_exporter.from_notebook_node(nb)
        #with open(pdf_path + '.tex', 'w') as latex_writer: 
        #    latex_writer.write(latex_output[0])

        pdf_output = pdf_exporter.from_notebook_node(nb)
        with open(pdf_path + ".pdf", "wb") as out:
            out.write(pdf_output[0])
            print("Saved", pdf_path)
        return True
    except nbconvert.pdf.LatexFailed as error:
        print("There was an error generating your LaTeX")
        output = error.output
        if not debug:
            print("To see the full error message, run with debug=True")
            output = "\n".join(error.output.split("\n")[-15:])
        print("=" * 30)
        print(output)
        print("=" * 30)
        return False


def has_error(nb):
    pdf_exporter = PDFExporter( )
    try:
        pdf_exporter.from_notebook_node(nb)
        return None
    except nbconvert.pdf.LatexFailed as error:
        return "\n".join(error.output.split("\n")[-15:])


def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


