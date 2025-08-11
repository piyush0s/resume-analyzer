# 📝 Resume Analyzer

A **Machine Learning-powered** web application that analyzes resumes, extracts key skills, and predicts job suitability.  
Built using **Python, Flask, HTML, CSS, and Jupyter Notebook**, with `.pkl` files for trained ML models.

---

## 🚀 Features

- 📂 **Upload Resume** – Supports PDF/DOCX formats.
- 🧠 **Machine Learning Model** – Predicts job role suitability using pre-trained `.pkl` models.
- 📊 **Skill Extraction** – Extracts key skills, education, and experience from resumes.
- 🎯 **Job Recommendation** – Suggests relevant job categories.
- 🌐 **Web Interface** – Simple and responsive UI using HTML, CSS, and Flask.
- ⚡ **Fast & Lightweight** – Works locally without heavy dependencies.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **File Handling**: PyPDF2, docx2txt
- **Model Storage**: `.pkl` files
- **Development**: Jupyter Notebook

---

## 📂 Project Structure

```
Resume_Analyzer/
│
├── app.py                  # Flask app entry point
├── model.pkl               # Trained ML model
├── vectorizer.pkl          # Text vectorizer
├── templates/
│   └── index.html          # Main HTML page
├── static/
│   ├── style.css           # Styling
│   └── script.js           # (If any JS)
├── resume_parser.ipynb     # Jupyter Notebook for training
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/resume_analyzer.git
cd resume_analyzer
```

### 2️⃣ Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate    # On Windows
source venv/bin/activate # On Mac/Linux
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Flask app
```bash
python app.py
```

### 5️⃣ Open in browser
```
http://127.0.0.1:5000
```

---

## 📊 Model Training

If you want to retrain the ML model:
1. Open **`resume_parser.ipynb`** in Jupyter Notebook.
2. Prepare the dataset.
3. Train the model and save it as `.pkl`:
   ```python
   import pickle
   pickle.dump(model, open("model.pkl", "wb"))
   ```

---

## 📸 Screenshots

### Upload Resume
![Upload Screenshot](screenshots/upload.png)

### Results Page
![Results Screenshot](screenshots/results.png)

---

## 📜 License
This project is licensed under the MIT License – you’re free to use, modify, and distribute it.

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📧 Contact
For queries or collaboration, reach out:
- **Email**: your.email@example.com
- **GitHub**: [yourusername](https://github.com/yourusername)
