import streamlit as st
import pandas as pd
import subprocess
import os
import base64
import pickle

# Custom CSS for pro-level styling
st.markdown("""
    <style>
    /* Style the sidebar */
    .sidebar .sidebar-content {
        background-color: #f0f0f5;
    }
    
    /* Style the header text */
    .main .block-container h1 {
        color: #2c3e50;
        font-family: 'Arial', sans-serif;
        text-align: center;
    }

    /* Style the buttons */
    .stButton button {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        border: none;
    }

    .stButton button:hover {
        background-color: #2980b9;
        color: white;
    }

    /* Custom styling for the file uploader */
    .stFileUploader div div {
        background-color: #ecf0f1;
        padding: 10px;
        border-radius: 8px;
    }

    /* Custom styling for success messages */
    .stAlert p {
        color: #27ae60;
        font-size: 18px;
        font-weight: bold;
    }

    /* Custom styling for error messages */
    .stAlert .stAlert p {
        color: #e74c3c;
        font-size: 18px;
        font-weight: bold;
    }
    
    /* Set the main container width */
    .main .block-container {
        max-width: 800px;
        margin: auto;
    }
    
    </style>
""", unsafe_allow_html=True)

def desc_calc():
    # Ensure the output directory exists
    output_dir = "C:\\Users\\abhis\\Downloads\\bioactivity-prediction-app-main\\bioactivity-prediction-app-main"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Absolute path to input file and descriptor output
    input_file = os.path.join(output_dir, 'molecule.smi')
    descriptor_output = os.path.join(output_dir, 'descriptors_output.csv')
    descriptor_list_file = os.path.join(output_dir, 'descriptor_list.csv')

    # Your command
    bashCommand = f"java -Xms2G -Xmx2G -Djava.awt.headless=true -jar {os.path.join(output_dir, 'PaDEL-Descriptor', 'PaDEL-Descriptor.jar')} -removesalt -standardizenitro -fingerprints -descriptortypes {os.path.join(output_dir, 'PaDEL-Descriptor', 'PubchemFingerprinter.xml')} -dir {output_dir} -file {descriptor_output}"

    # Run the command and capture the output
    try:
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode != 0:
            st.error(f"Error running PaDEL-Descriptor: {error.decode('utf-8')}")
        else:
            st.success("Descriptor calculation completed successfully!")

    except Exception as e:
        st.error(f"Failed to run PaDEL-Descriptor: {str(e)}")

    # Ensure the output file exists before proceeding
    if not os.path.exists(descriptor_output):
        st.error(f"Descriptor output file not found: {descriptor_output}")
    else:
        st.success("Descriptor output file found!")
    
    # Ensure descriptor_list.csv exists
    if not os.path.exists(descriptor_list_file):
        st.error(f"Descriptor list file not found: {descriptor_list_file}")
    else:
        st.success("Descriptor list file found!")

    if os.path.exists(input_file):
        os.remove(input_file)

# File download
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv" style="color:white;background-color:#3498db;padding:10px;border-radius:8px;text-decoration:none;">Download Predictions</a>'
    return href

# Model building
def build_model(input_data):
    # Path to the model file
    model_file = 'C:\\Users\\abhis\\Downloads\\bioactivity-prediction-app-main\\bioactivity-prediction-app-main\\acetylcholinesterase_model.pkl'
    if not os.path.exists(model_file):
        st.error(f"Model file not found: {model_file}")
        return

    # Reads in saved regression model
    try:
        load_model = pickle.load(open(model_file, 'rb'))
        # Apply model to make predictions
        prediction = load_model.predict(input_data)
        st.header('**Prediction output**')
        prediction_output = pd.Series(prediction, name='pIC50')
        molecule_name = pd.Series(load_data[1], name='molecule_name')
        df = pd.concat([molecule_name, prediction_output], axis=1)
        st.write(df)
        st.markdown(filedownload(df), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to load or apply the model: {str(e)}")


# Page title
st.markdown("""
# Bioactivity Prediction App (Acetylcholinesterase)

This app allows you to predict the bioactivity towards inhibiting the `Acetylcholinesterase` enzyme. `Acetylcholinesterase` is a drug target for Alzheimer's disease.

""")

# Sidebar
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input file", type=['txt'])
    

if st.sidebar.button('Predict'):
    if uploaded_file is not None:
        load_data = pd.read_table(uploaded_file, sep=' ', header=None)
        input_file = os.path.join("C:\\Users\\abhis\\Downloads\\bioactivity-prediction-app-main\\bioactivity-prediction-app-main", 'molecule.smi')
        load_data.to_csv(input_file, sep='\t', header=False, index=False)

        st.header('**Original input data**')
        st.write(load_data)

        with st.spinner("Calculating descriptors..."):
            desc_calc()

        # Read in calculated descriptors and display the dataframe
        descriptor_output = os.path.join("C:\\Users\\abhis\\Downloads\\bioactivity-prediction-app-main\\bioactivity-prediction-app-main", 'descriptors_output.csv')
        if os.path.exists(descriptor_output):
            desc = pd.read_csv(descriptor_output)
            st.header('**Calculated molecular descriptors**')
            st.write(desc)
            st.write(desc.shape)

            # Read descriptor list used in previously built model
            descriptor_list_file = os.path.join("C:\\Users\\abhis\\Downloads\\bioactivity-prediction-app-main\\bioactivity-prediction-app-main", 'descriptor_list.csv')
            if os.path.exists(descriptor_list_file):
                st.header('**Subset of descriptors from previously built models**')
                Xlist = list(pd.read_csv(descriptor_list_file).columns)
                desc_subset = desc[Xlist]
                st.write(desc_subset)
                st.write(desc_subset.shape)

                # Apply trained model to make prediction on query compounds
                build_model(desc_subset)
            else:
                st.error('Descriptor list file was not found. Ensure it exists in the expected location.')
        else:
            st.error('Descriptor output file was not created. Please check the command and input files.')

    else:
        st.error('No input file uploaded. Please upload a file to proceed.')
else:
    st.info('Upload input data in the sidebar to start!')

