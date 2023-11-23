# app.py

from flask import Flask, render_template, request, send_from_directory
import nbformat
from nbconvert import PythonExporter
import subprocess
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_data = request.form['input_data']

        # Update the Jupyter Notebook
        update_notebook_line(form_data, 88)

        # Execute the Jupyter Notebook
        result = execute_notebook()

        # Check the form data condition
        if is_good_to_go(form_data):
            return render_template('result.html')
        else:
            return render_template('result2.html')

    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/superlogin')
def superlogin():
    return render_template('superuserlogin.html')


@app.route('/superindex')
def superindex():
    return render_template('superindex.html')


def is_good_to_go(data):
    print(f"Received data: {data}")
    try:
        # Assuming data is a valid Python list representation of a 2D array
        array_2d = eval(data)
        
        # Check if each element in the 2D array is less than 100
        if all(all(element > 100 for element in row) for row in array_2d):
            return True  # Good to go
        else:
            return False  # Not good to go
    except Exception as e:
        print(f"Error processing data: {e}")
        return False


def update_notebook_line(data, cell_index):
    print(f"Received data: {data}")
    # Load the notebook
    with open('Final_notebook.ipynb', 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    # Modify the source field of the specified code cell
    if 0 <= cell_index < len(notebook.cells) and notebook.cells[cell_index].cell_type == 'code':
        # Update the source code based on the form data
        notebook.cells[
            cell_index].source = f"skanda_test = {data}\n\ny_xgb_pred = model_xgb.predict(skanda_test)\n\ny_xgb_pred"

    # Save the updated notebook
    with open('Final_notebook.ipynb', 'w', encoding='utf-8') as f:
        nbformat.write(notebook, f)


def execute_notebook(kernel_name='python3.11'):

    # Execute and save the Jupyter Notebook in place
    subprocess.run(['jupyter', 'nbconvert', '--execute',
                   '--inplace', '--ExecutePreprocessor.kernel_name', kernel_name, 'Final_Notebook.ipynb'])

    # Convert the notebook to a Python script
    subprocess.run(['jupyter', 'nbconvert', '--to',
                   'script', 'Final_Notebook.ipynb'])

    # Execute the Python script
    execop = subprocess.Popen(['python', 'Final_Notebook.py'], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)  # capture_output=True, text=True

    '''# Analyze the result and return 0 or 1 accordingly
    return 1 if result.returncode == 0 else 0

    if result.returncode == 0:
        return 1
    else:
        print("Error during script execution:")
        print(result.stderr)
        return 0'''


if __name__ == '__main__':
    app.run(debug=True)
