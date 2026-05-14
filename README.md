```text
   ______ _       _                _           _           
  / ____(_)     | |              | |         | |          
 | |     _ _ __ | |__   ___ _ __ | |     __ _| |__  ___   
 | |    | | '_ \| '_ \ / _ \ '__|| |    / _` | '_ \/ __|  
 | |____| | |_) | | | |  __/ |   | |___| (_| | |_) \__ \  
  \_____|_| .__/|_| |_|\___|_|   |______\__,_|_.__/|___/  
           | |                                            
           |_|                                            

 A guided cryptanalysis workbench for interactive codebreaking
```

# 🔐 CipherLabs

**A public codebreaking workbench for learning, exploring, and solving ciphers.**

🌐 Website: https://cipherlabs.eu

CipherLabs is a Flask-based cryptanalysis platform focused on interactive
cipher solving, guided analysis workflows, and educational codebreaking.

Instead of offering isolated tools, CipherLabs aims to provide a real
**cryptanalysis workbench** where users progressively analyze, classify,
and solve encrypted messages.

---

## 🚀 Vision

CipherLabs bridges the gap between:

- 📚 Educational cryptography
- 🧠 Practical codebreaking
- 🛠 Guided cryptanalysis workflows
- 🌍 Collaborative solving

Users do not simply read about ciphers — they actively investigate them.

---

## 🧩 Current Features

### 🔍 Cipher Exploration

- Browse solved and unsolved ciphers
- Cipher metadata and contextual information
- Public cipher archive
- Cipher glossary / lexicon

### 🧠 Guided Cryptanalysis Workbench

- Cipher classification engine
- Guided solving recommendations
- Workbench phases:
  - Identify
  - Analyze
  - Solve
  - Validate
  - Notes

### 📊 Analysis Tools

- Frequency analysis
- Index of Coincidence (IoC)
- Repeated sequence detection
- Language frequency matching
- Digram similarity analysis
- Word pattern analysis

### 🛠 Interactive Solving

- Caesar brute force analysis
- Substitution solver workspace
- Mapping confidence engine
- Progressive plaintext reveal
- Ranked substitution candidates
- Substitution mapping assistant
- Workspace persistence

### 💾 Workspace Features

- Save solving progress
- Save mappings and notes
- Continue solving sessions later

---

## 🏗️ Tech Stack

- **Backend:** Flask
- **Database:** PostgreSQL
- **Authentication:** Flask-Login
- **Architecture:** Modular layered architecture

```text
entities → processors → database
```

---

## 📁 Project Structure

```text
blueprints/     Flask routes
cipher/         Cipher logic and analysis tools
templates/      Workbench and UI templates
static/         CSS and front-end assets
reference/      Static datasets and dictionaries
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/cipherlab.git
cd cipherlab
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Create a `.env` file:

```env
FLASK_SECRET_KEY=your-secret-key
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=cipherlab
POSTGRES_USER=cipherlab_user
POSTGRES_PASSWORD=your-password
```

### 5. Prepare PostgreSQL

```sql
CREATE DATABASE cipherlab;
CREATE USER cipherlab_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE cipherlab TO cipherlab_user;
```

### 6. Create tables

```bash
python setup.py
```

### 7. Run the application

```bash
python app.py
```

Visit:

```text
http://127.0.0.1:5000
```

---

## 🧪 Roadmap

### Near-Term

- [x] Cipher CRUD system
- [x] Frequency analysis
- [x] IoC analysis
- [x] Repeated sequence detection
- [x] Cipher classification engine
- [x] Guided workbench phases
- [x] Substitution solver
- [x] Mapping confidence engine
- [x] Progressive plaintext reveal
- [x] Workspace persistence
- [x] Cipher glossary

### Next Steps

- [ ] Click-to-accept mappings
- [ ] Conflict highlighting
- [ ] Auto-detected probable plaintext words
- [ ] Trigram analysis
- [ ] N-gram scoring engine
- [ ] Interactive plaintext reconstruction
- [ ] Workspace history / undo system

### Future Goals

- [ ] Full Vigenère workflow
- [ ] Kasiski examination tools
- [ ] Columnar transposition workflows
- [ ] Collaborative solving system
- [ ] Public challenge archive
- [ ] Team-based cryptanalysis
- [ ] AI-assisted solving guidance

---

## 🤝 Contributing

CipherLabs is under active development.

Feedback, ideas, testing, and contributions are welcome.

---

## 📜 Inspiration

- *Codebreaking* — Elonka Dunin & Klaus Schmeh
- Historical cryptanalysis workflows
- Classical cipher solving communities

---

## ⚠️ Disclaimer

CipherLabs is intended for educational, historical, and research purposes only.

---

## 🧠 Final Thought

> Every cipher hides a structure.  
> CipherLabs is where you learn to uncover it.
```