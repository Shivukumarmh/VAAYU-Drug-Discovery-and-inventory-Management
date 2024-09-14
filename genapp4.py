import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd

# Load the saved GAN generator model
@st.cache(allow_output_mutation=True)
def load_generator():
    return tf.keras.models.load_model('C:\\Users\\abhis\\Desktop\\gen ai model\\generator_model3.h5')

# Generate new molecular descriptors
def generate_new_molecules(generator, num_samples=10, latent_dim=100):
    random_noise = np.random.normal(0, 1, (num_samples, latent_dim))
    generated_molecules = generator.predict(random_noise)
    return generated_molecules

# Streamlit app
def main():
    st.title("Molecule Generation using GAN")
    st.write("This app generates new molecular descriptors using a trained GAN model.")

    # Number of molecules to generate
    num_samples = st.slider("Number of molecules to generate", min_value=1, max_value=10, value=10)

    # Load the GAN generator model
    generator = load_generator()

    # Button to generate new molecules
    if st.button("Generate Molecules"):
        st.write(f"Generating {num_samples} new molecules...")
        new_molecules = generate_new_molecules(generator, num_samples)
        st.write("Generated molecular descriptors:")
        st.dataframe(pd.DataFrame(new_molecules))

        # Option to download the generated molecules as CSV
        csv = pd.DataFrame(new_molecules).to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name="generated_molecules.csv", mime='text/csv')

if __name__ == "__main__":
    main()
