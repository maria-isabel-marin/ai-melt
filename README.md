# AI-MELT

**AI-MELT** is a research-oriented project aimed at implementing a multi-step metaphor processing pipeline based on the MELT model (*Metaphor Field-Loop Theory*), introduced in:

> Valdivia Milla, B., & Valdivia Martin, P. (2023).  
> *Conflictive Cultural Narratives in the Collective Memory of the Spanish Transition: The Case of Trampa para Pájaros by José Luis Alonso De Santos.*  
> In K. Robbe (Ed.), *Remembering Transitions* (pp. 57–84). De Gruyter.  
> https://doi.org/10.1515/9783110707793-003

This pipeline forms part of the doctoral research titled:

> **Can an AI-enabled system help us understand how cultural narratives are configured, and how do they prime social mobilization?**

---

## 🎯 Project Goals

AI-MELT is designed to implement several key tasks from the MELT model:

1. **Identification of metaphorical expressions**  
2. **Construction of conceptual metaphor**  
3. **Classification into conventional vs. novel metaphors**  
4. **Clustering of expressions into metaphorical scenarios**  
5. **Grouping of scenarios into narrative regimes**

---

## 🚀 Setup Instructions

1. **Clone the repository and navigate to the project:**
   ```bash
   git clone https://github.com/your-user/ai-melt.git
   cd ai-melt/scripts/step-one-primary-metaphor
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/macOS
   venv\Scripts\activate    # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   python -m spacy download es_core_news_sm
   ```

4. **Prepare your configuration:**
   - Copy and customize the template:
     ```bash
     cp config_template.py config.py
     ```
   - Edit `config.py` to set active models and API keys (if applicable).

5. **Run the pipeline:**
   ```bash
   python pipeline.py < input.txt > output.json
   ```

---

## 🧠 Model Integration

The system supports various metaphor detection models, including:

- Hugging Face fine-tuned transformers
- OpenAI GPT models (e.g., GPT-4)
- Gemini, Mistral, LLaMA (API-based or local inference)

Each can be configured and activated via the `config.py` file.

---

## 📄 Citation Requirement

If you use **AI-MELT** in academic work, you **must cite** the following source:

> Marín-Morales, M.I., Valdivia, P. (2025).  
> *AI-MELT: A pipeline for metaphor detection and narrative analysis* [Computer software].  
> GitHub. https://github.com/maria-isabel-marin/ai-melt  
> (Work in progress as part of the Ph.D. dissertation: *“Can an AI-enabled system help us understand how cultural narratives are configured, and how do they prime social mobilization?”*)

---

## 👩‍💻 Author

María Isabel Marín  
Ph.D. Candidate – Graduate School for the Humanities  
University of Groningen  
m.i.marin.morales@rug.nl
Supervised by Prof. Dr. Pablo Valdivia

---

## 📜 License

This repository is part of an ongoing doctoral dissertation. Academic use is welcome, **provided proper citation is given**. Commercial or redistributive use is not permitted without prior written consent.
