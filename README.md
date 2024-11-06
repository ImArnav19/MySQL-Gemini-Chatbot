# T-Shirt Database App

![Screenshot (102)](https://github.com/user-attachments/assets/5dd35d2f-8e44-4dc4-9831-1d9fa37af9d4)
![Screenshot (103)](https://github.com/user-attachments/assets/d3b4cabd-1c8b-4386-a3e2-9a0a6b1aec8a)
![Screenshot (104)](https://github.com/user-attachments/assets/df81d28f-5226-4a04-82ab-3f3476350408)



This Streamlit app provides a user interface to query and view data from a t-shirt inventory database. It allows users to search for t-shirts by brand, color, size, and price range, and includes additional features like discount display and stock management.

## Features
- View and search for t-shirts by various attributes (brand, color, size, price).
- Display discounts applied to specific t-shirts.
- Stock management with real-time updates.

## Project Structure

- `app.py`: The main Streamlit application file, which contains the code to build and render the web interface.
- `requirements.txt`: Lists all the Python dependencies required to run the app.
- `.streamlit/secrets.toml`: Holds sensitive information, such as database credentials, necessary for database connection (excluded from version control).
- `myenv/`: The virtual environment directory, which contains all installed packages and dependencies for this project (not required for version control).
- `test01.ipynb`: A Jupyter Notebook file, possibly for testing or experimenting with SQL and data retrieval.

## Setup Instructions

Follow these steps to set up and run the application locally.

### Prerequisites

- Python 3.8 or higher
- A virtual environment (recommended)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/tshirt-database-app.git
   cd tshirt-database-app

### Installation

2. **Set Up a Virtual Environment** (optional but recommended)
   ```bash
   python -m venv myenv
   source myenv/Scripts/activate  # On Windows use `myenv\Scripts\activate`

3. **Install the Required Packages**  
   Use `requirements.txt` to install all dependencies:
   ```bash
   pip install -r requirements.txt


4. **Configure Secrets**  
   - Place your `secrets.toml` file inside the `.streamlit/` directory.
   - **Do not share `secrets.toml` publicly** as it contains sensitive information, like database connection credentials. If you do not have this file, contact the repository owner to obtain it.

### Running the App

Run the Streamlit app with the following command:
  ```bash
    streamlit run app.py
  ```

This will start the app locally, and Streamlit will provide a local URL (usually http://localhost:8501) to access the app in your browser.

Example Usage
Once the app is running:

Search for specific t-shirts by applying filters based on attributes.
Check discounts applied to different t-shirts.
View available stock and price details.
