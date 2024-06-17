import shutil

from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os
import os
from flask import send_file, render_template
from reportlab.lib.pagesizes import portrait, A4
from reportlab.pdfgen import canvas
import os
from flask import send_file
from reportlab.lib.pagesizes import portrait, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

app = Flask(__name__)


@app.route('/')
def start():
    return render_template('start.html')
@app.route('/start')
def star1():
    return render_template('start.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/under_construct')
def und():
    return render_template('under_constr.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/index')
def index():
    # Remove all files from the static/plots folder
    folder_path = 'static/plots'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    return render_template('form-cs.html')


# Route for collecting form data via wifi tunneling
@app.route('/wifi-tunneling', methods=['GET', 'POST'])
def wifi_tunneling():
    return render_template('wifi_tunneling.html')

@app.route('/readme', methods=['GET', 'POST'])
def readme():
    return render_template('readme.html')


ALLOWED_EXTENSIONS = {'csv', 'txt', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route for generating and displaying clustering results
@app.route('/generate-clusters', methods=['GET', 'POST'])
def generate_clusters():
    if request.method == 'POST':
        # Get form data
        num_clusters = int(request.form['num_clusters'])
        algo_type = request.form['algo_type']

        print("--GOT ALGO--")
        dataset_selection = request.form['dataset']
        print("--GOT DATASET--")

        if request.form['dataset'] == 'custom':
            file = request.files['custom_dataset']
            if file and allowed_file(file.filename):
                # Save the custom dataset file to the "datasets" folder
                if file:
                    filename = 'custom.csv'  # Set the desired filename
                    file_path = os.path.join('datasets', filename)
                    file.save(file_path)  # Save the file
                    # Perform clustering on the custom dataset

        # Determine dataset selection and load dataset
        if dataset_selection == 'dataset1':
            dataset = pd.read_csv('datasets/Sales Transaction.csv')
        elif dataset_selection == 'dataset2':
            dataset = pd.read_csv('datasets/Personal Info.csv')
        elif dataset_selection == 'dataset3':
            dataset = pd.read_csv('datasets/Customer Demographics.csv')
        elif dataset_selection == 'dataset4':
            dataset = pd.read_csv('datasets/Wine Quality.csv')
        elif dataset_selection == 'dataset5':
            dataset = pd.read_csv('datasets/online retail.csv')
        elif dataset_selection == 'dataset6':
            dataset = pd.read_csv('datasets/geolocation.csv')
        elif dataset_selection == 'dataset7':
            dataset = pd.read_csv('datasets/Product Sales.csv')
        elif dataset_selection == 'dataset8':
            dataset = pd.read_csv('datasets/Sports Performance.csv')
        elif dataset_selection == 'dataset9':
            dataset = pd.read_csv('datasets/Customer-Segmentation.csv')
        elif dataset_selection == 'dataset10':
            dataset = pd.read_csv('datasets/dataset7.csv')
        elif dataset_selection == 'custom':
            print("CUSTOM - ENTER")
            dataset = pd.read_csv('datasets/custom.csv')
        else :
            return render_template('error.html')

        # Identify and remove non-numeric columns
        non_numeric_columns = []
        for column in dataset.columns:
            if not np.issubdtype(dataset[column].dtype, np.number):
                non_numeric_columns.append(column)

        # Drop rows with NaN values
        dataset = dataset.dropna()
        dataset = dataset.drop(columns=non_numeric_columns)

        # Convert remaining columns to floats
        dataset = dataset.astype(float)


        # Get feature names
        feature_names_a = dataset.columns.tolist()
        # Convert dataset to HTML table
        table_html = dataset.to_html(index=False)


        # Run clustering algorithm
        if algo_type == 'k-means':
            print("KMEANS = ENTER")
            kmeans = KMeans(n_clusters=num_clusters)
            kmeans.fit(dataset)
            dataset['cluster'] = kmeans.labels_
            # Get feature names
            feature_names = dataset.columns.tolist()
            # Remove 'cluster' column from feature names
            feature_names.remove('cluster')
            # Generate scatter plot
            plots = []
            # Generate scatter plot
            plots = []
            plot_dir = os.path.join('static', 'plots')
            if not os.path.exists(plot_dir):
                os.makedirs(plot_dir)

            image_names = []
            for i in range(len(feature_names)):
                for j in range(i + 1, len(feature_names)):
                    fig, ax = plt.subplots()
                    ax.scatter(dataset[feature_names[i]], dataset[feature_names[j]], c=dataset['cluster'])
                    ax.set_xlabel(feature_names[i])
                    ax.set_ylabel(feature_names[j])
                    # Save plot image to file
                    plot_file = f'plot_{feature_names[i]}_{feature_names[j]}.png'
                    plot_path = os.path.join(plot_dir, plot_file)
                    plt.savefig(plot_path, format='png')
                    plt.close(fig)
                    image_names.append(plot_file)

            print("EXIT - KMEANS")
            # Return results HTM
            return render_template('result.html', image_names=image_names, feature_names=feature_names,feature_names_a=feature_names_a  ,table_html=table_html)

        elif algo_type == 'hierarchical':
            # Implement hierarchical clustering algorithm
            # ...
            return render_template('under_constr.html')
        elif algo_type == 'DBSCAN':
            # Implement DBSCAN clustering algorithm
            # ...
            return render_template('under_constr.html')
        else:
            return render_template('error.html')
    return render_template('error.html')



@app.route('/download-pdf')
def download_pdf():
    image_folder = 'static/plots'
    pdf_path = 'static/pdf/special_project_report.pdf'

    # Get all the image files in the folder
    image_files = [filename for filename in os.listdir(image_folder) if filename.endswith(('.png', '.jpg', '.jpeg'))]

    # Calculate the number of pages needed
    images_per_page = 2
    total_pages = (len(image_files) + images_per_page - 1) // images_per_page

    # Create a new PDF canvas
    pdf_canvas = canvas.Canvas(pdf_path, pagesize=portrait(A4), bottomup=True)

    # Set margins
    left_margin = 0.75 * inch
    right_margin = A4[0] - 0.75 * inch
    top_margin = A4[1] - 0.75 * inch
    bottom_margin = 0.75 * inch

    # Set background color
    pdf_canvas.setFillColorRGB(0.9, 0.9, 0.9)

    # Add introduction page
    intro_image_path = 'static/intro.png'
    pdf_canvas.drawImage(intro_image_path, x=0, y=0, width=A4[0], height=A4[1])

    # Iterate through the image files and add them to the PDF
    page_count = 0
    for i, image_file in enumerate(image_files):
        # Add a new page if necessary
        if i % images_per_page == 0:
            pdf_canvas.showPage()
            page_count += 1

            # Add header
            header_text = f"Page {page_count}/{total_pages}"
            pdf_canvas.setFont('Helvetica', 12)
            pdf_canvas.drawCentredString(A4[0] / 2, top_margin - inch, header_text)

        # Calculate the position for the current image
        x = left_margin
        y = top_margin - (i % images_per_page) * (A4[1] / 2) - 4.8 * inch

        # Add the image to the current page
        image_path = os.path.join(image_folder, image_file)
        pdf_canvas.drawImage(image_path, x=x, y=y, width=6.4 * inch, height=4.8 * inch)

        # Add the image name below the image
        pdf_canvas.setFont('Helvetica', 10)
        pdf_canvas.drawRightString(x + 6.3 * inch, y - 0.2 * inch, image_file)

    # Add ending page
    ending_image_path = 'static/end.png'
    pdf_canvas.showPage()
    pdf_canvas.drawImage(ending_image_path, x=0, y=0, width=A4[0], height=A4[1])

    # Save the PDF file
    pdf_canvas.save()

    # Send the generated PDF file as an attachment
    return send_file(pdf_path, as_attachment=True)


if __name__ == '__main__':
    app.run()
