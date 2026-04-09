# Legal Clause Simplifier (Streamlit)

AI-powered Streamlit app that takes a **rental agreement clause** and generates:

- A **simplified explanation**
- A **risk level**: Low / Medium / High (color-coded)

## Tech stack

- **Streamlit** (UI)
- **Hugging Face Transformers** (base model)
- **PEFT (LoRA)** (adapter loading)
- **PyTorch**

## Model

- **Base model**: `google/gemma-3-270m`
- **Adapter**: LoRA weights stored in `./model/` (this folder is **NOT** a full model)

Loading is done correctly as:

1. Tokenizer from `google/gemma-3-270m`
2. Base model from `google/gemma-3-270m`
3. LoRA adapter attached via `PeftModel.from_pretrained(base_model, "./model/")`

## Project structure

```
legal-simplifier/
│── app.py                # Streamlit UI
│── model_loader.py       # Model loading logic (cached)
│── inference.py          # Inference + cleaning
│── utils.py              # Helper functions
│── requirements.txt
│── README.md
│── model/                # LoRA adapter weights (you provide this)
```

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

## Notes

- Runs fully locally (no external APIs).
- Model loads **once** using Streamlit resource caching for fast demo performance.
