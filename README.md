[Python Downloads](https://www.python.org/downloads/)  
**Prerequisite:**

- Python version > 3.9 is required (needed for Flask).

# INITIALIZING THE PROJECT

1. **Clone the repository**

   ```
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **If on mac**

   ```
   make install

   ```

3. **Create a virtual environment**

   ```
   python3 -m venv .venv
   ```

4. **Activate the virtual environment**

   - On Linux/Mac:
     ```
     . .venv/bin/activate
     ```
   - On Windows:
     ```
     .\venv\Scripts\activate (replace venv with your environment's name) and press Enter
     ```

5. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

6. **Run the application**

   ```
   python run.py
   ```

7. **(Optional) For development mode**

   ```
   make dev
   ```

8. **(Optional) To update requirements.txt after installing new packages**
   ```
   make freeze
   ```

> **Note:**
>
> - Uploaded files and generated data are stored in the `uploads/` and `store/` directories, which are git-ignored by default.
> - Ensure you have the required environment variables set up if your application depends on them (e.g., API keys).
> - I did not added .env file in .gitignore so that setting up the project will be easier as this project uses mapbox public key.
