# 🔐 CipherLab

**A public codebreaking workbench for learning, exploring, and solving
ciphers.**

CipherLab is a web-based platform built with Flask that allows users to
study how famous ciphers were broken and to collaboratively explore
unsolved encrypted messages using real analysis tools.

------------------------------------------------------------------------

## 🚀 Vision

CipherLab is designed to bridge the gap between:

-   📚 **Educational cryptography**
-   🧠 **Hands-on codebreaking**
-   🌍 **Collaborative problem solving**

Users don't just read about ciphers --- they **interact with them**,
analyze them, and attempt to break them.

------------------------------------------------------------------------

## 🧩 Features (Current & Planned)

### 🔍 Cipher Exploration

-   Browse **solved** and **unsolved** cipher messages
-   View ciphertext, metadata, and context
-   Filter by type, difficulty, and language

### 📊 Built-in Analysis Tools

-   Character frequency analysis
-   Bigram / trigram analysis *(planned)*
-   Index of Coincidence *(planned)*
-   Repeated sequence detection *(planned)*
-   Language likelihood estimation *(planned)*

### 🛠 Interactive Workbench *(planned)*

-   Substitution cipher solver
-   Key experimentation tools
-   Transformation pipeline
-   Save personal progress

### 🧠 Learn by Doing

-   Step-by-step breakdowns of **historical cipher solutions**
-   "Try it yourself" modes for solved ciphers

### 🌐 Collaborative Codebreaking *(planned)*

-   Submit solution attempts
-   Share hypotheses
-   Track partial progress on unsolved messages

------------------------------------------------------------------------

## 🏗️ Tech Stack

-   **Backend:** Flask
-   **Database:** PostgreSQL
-   **Authentication:** Flask-Login
-   **Architecture:** Modular (entities → processors → database)

------------------------------------------------------------------------

## ⚙️ Setup

### 1. Clone the repository

``` bash
git clone https://github.com/yourusername/cipherlab.git
cd cipherlab
```

### 2. Create virtual environment

``` bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure environment

Create a `.env` file:

``` env
FLASK_SECRET_KEY=your-secret-key
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=cipherlab
POSTGRES_USER=cipherlab_user
POSTGRES_PASSWORD=your-password
```

------------------------------------------------------------------------

### 5. Prepare PostgreSQL

``` sql
CREATE DATABASE cipherlab;
CREATE USER cipherlab_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE cipherlab TO cipherlab_user;
```

------------------------------------------------------------------------

### 6. Create tables

``` bash
python setup.py
```

------------------------------------------------------------------------

### 7. Run the application

``` bash
python app.py
```

Visit:

http://127.0.0.1:5000

------------------------------------------------------------------------

## 📁 Project Structure

core/ → Users, authentication, database layer\
cipher/ → Cipher logic, analysis tools, processing\
blueprints/ → Flask routes\
templates/ → HTML views

------------------------------------------------------------------------

## 🧪 Roadmap

-   [ ] CipherMessage entity + CRUD interface
-   [ ] Frequency analysis (first tool)
-   [ ] Cipher detail page
-   [ ] Substitution solver UI
-   [ ] Index of Coincidence
-   [ ] Vigenère tools
-   [ ] Workspace saving
-   [ ] Public cipher archive
-   [ ] Collaborative solving

------------------------------------------------------------------------

## 🤝 Contributing

This project is in early development. Contributions, ideas, and feedback
are welcome.

------------------------------------------------------------------------

## 📜 Inspiration

-   *Codebreaking* by Elonka Dunin & Klaus Schmeh

------------------------------------------------------------------------

## ⚠️ Disclaimer

CipherLab is intended for **educational and research purposes only**.

------------------------------------------------------------------------

## 🧠 Final Thought

> Every cipher tells a story.\
> CipherLab is where you learn how to read it.
