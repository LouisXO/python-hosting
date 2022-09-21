
from flask import Flask, render_template, request, send_file
import os
from os.path import join, dirname, realpath
import pandas as pd


app = Flask(__name__)

app.config["DEBUG"] = True


# Upload Folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER




@app.route('/')
def hello():
    return render_template('form.html')

@app.route('/', methods = ['POST'])
def submit():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
           file_path = os.path.join(app.static_folder, uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
           parseCSV(file_path)
    
    return render_template('submit.html')


# This is the function that you could replace with the script
def parseCSV(filePath):
      # CVS Column Name, feel free to change, testing only
      col_names = ['first_name','last_name','address', 'street', 'state' , 'zip']
      # Use Pandas to parse the CSV file
      # filePath is where the user submits
      csvData = pd.read_csv(filePath, names=col_names, header=None)
      
      
      # Keep the last two for saving the file
      result_path = os.path.join(app.static_folder, "result.csv")
      # Save the result file
      csvData.to_csv(result_path, encoding='utf-8', index=False)
    

@app.route('/download') # this is a job for GET, not POST
def plot_csv():
    result_path = os.path.join(app.static_folder, "result.csv")
    
    return send_file(
        result_path,
        mimetype='text/csv',
        download_name='results.csv',
        as_attachment=True
    )


app.run(host='localhost', port=5000)
