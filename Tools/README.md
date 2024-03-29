# Overview of Notebooks

Below is an overview of each notebook contained in this repository. It is recommended to follow the notebooks in their numerical order to ensure a seamless experience and understanding of the entire pipeline.

### 1. Key Generation for Training Data (`#1_create_keys_train.ipynb`)

**Objective:** Generates encryption keys necessary for the encryption of training data. This step is crucial as it lays the foundation for securing the data before the model training begins.

**Key Features:**
- Utilizes multiprocessing to speed up the key generation process.
- Outputs keys are saved for later use in data encryption.

**Usage Guide:**
1. Verify that the `_1_keygen_json.py` script is available in your project directory. This script is essential for the key generation process.
2. Run all cells within the notebook to generate the encryption keys. These keys will be used in the subsequent encryption of your training data.

### 2. Creating Ciphertexts for Training Data (`#2_create_ciphertexts_train.ipynb`)

**Objective:** Encrypts the training data using the keys generated in the previous step. This notebook transforms the plaintext training data into ciphertexts, thus preparing it for the model training process in a secure manner.

**Key Features:**
- Encryption process utilizes multiprocessing for enhanced performance.
- Ensures the integrity and confidentiality of the training data.

**Usage Guide:**
1. Ensure access to the encryption keys generated from Notebook 1.
2. Execute the notebook to encrypt the training data, converting it into a secure format for the upcoming training phase.

### 3. Preparing Training Data (`#3_create_npy-data_train.ipynb`)

**Objective:** Converts the encrypted training data into a numpy (`.npy`) format. This format is more conducive for machine learning operations, facilitating efficient data manipulation and model training.

**Key Features:**
- Optimizes data storage and access for the training process.
- Supports large datasets through efficient file handling.

**Usage Guide:**
1. This notebook should be run post-encryption of the training data to prepare it in an optimized format for machine learning models.

### 4. Training Models (`#4_train_models.ipynb`)

**Objective:** Embarks on the actual model training using the encrypted and prepared training data. This notebook dives into the model building, configuration, and training phases, showcasing various techniques and optimizations.

**Key Features:**
- Demonstrates the handling of encrypted data within machine learning models.
- Covers essential practices in memory management and environmental setup for model training.

**Usage Guide:**
1. Follow the detailed instructions within the notebook to train your machine learning models on the encrypted data.

### 5. Key Generation for Testing Data (`#5_create_keys_test.ipynb`)

**Objective:** Mirrors the first notebook but focuses on generating keys for the testing data. Ensuring that the testing data is encrypted with a separate set of keys maintains the integrity of the testing process.

**Usage Guide:**
1. Similar to the first notebook, ensure the presence of the necessary key generation script.
2. Generate the keys required for encrypting the testing dataset.

### 6. Creating Ciphertexts for Testing Data (`#6_create_ciphertexts_test.ipynb`)

**Objective:** Encrypts the testing data, preparing it for use in evaluating the trained models. This step ensures that the model's performance can be accurately assessed on secure data.

**Usage Guide:**
1. After generating the testing data keys, use this notebook to encrypt the testing dataset.

### 7. Preparing Testing Data (`#7_create_npy-data_test.ipynb`)

**Objective:** Converts the encrypted testing data into a numpy format, facilitating efficient model evaluation and performance testing.

**Usage Guide:**
1. Post-encryption of the testing data, run this notebook to optimize the data for the testing phase.

### 8. Testing Models (`#8_test_models.ipynb`)

**Objective:** Evaluates the performance of the trained models using the encrypted and prepared testing data. This notebook provides insights into how well the models can decrypt and interpret the encrypted data, highlighting their effectiveness and areas for improvement.

**Key Features:**
- Comprehensive model evaluation techniques.
- Visualizations and performance metrics for in-depth analysis.

**Usage Guide:**
1. With the models trained and the testing data prepared, follow the notebook to test and analyze the performance of your models on encrypted data.


