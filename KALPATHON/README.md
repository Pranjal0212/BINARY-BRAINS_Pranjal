# Legal Clause Simplifier

A premium, futuristic web application that simplifies complex rental agreement clauses using a local AI model. Features advanced glassmorphism UI, 3D animations, and complete privacy.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red.svg)
![PyTorch](https://img.shields.io/badge/pytorch-2.1+-orange.svg)

## 🌟 Features

- **🔒 100% Private**: All processing happens locally on your machine
- **✨ AI-Powered**: Fine-tuned Gemma 3 270M model for legal text
- **⚖️ Risk Assessment**: Automatic classification (Low, Medium, High)
- **🎨 Premium UI**: Advanced glassmorphism with 3D animations
- **⚡ Optimized**: Fast inference with torch optimizations

## 🏗️ Project Structure

```
legal-simplifier/
├── app.py                 # Main Streamlit application
├── model_loader.py        # Model loading and caching
├── inference.py           # Optimized inference engine
├── utils.py              # Utility functions
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── model/                # Local Hugging Face model directory
    ├── config.json
    ├── pytorch_model.bin
    ├── tokenizer.json
    └── ...
```

## 📋 Requirements

- Python 3.10 or higher
- 8GB+ RAM recommended
- GPU optional (CUDA or MPS supported, but works on CPU)
- Local Hugging Face model in `./model/` directory

## 🚀 Installation

### 1. Clone or Download the Project

```bash
cd legal-simplifier
```

### 2. Create Virtual Environment (Recommended)

```bash
# Using venv
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Frontend Dependencies

```bash
npm install
```

### 5. Place Your Model

Ensure your fine-tuned Gemma 3 270M model is in the `./model/` directory:

```bash
legal-simplifier/
└── model/
    ├── config.json
    ├── pytorch_model.bin
    ├── tokenizer.json
    ├── tokenizer_config.json
    └── special_tokens_map.json
```

## 🎯 Usage

### Run the Application

```bash
streamlit run app.py
```

### Run React Frontend + API Integration

Run the backend API in one terminal:

```bash
uvicorn backend_api:app --host 127.0.0.1 --port 8000 --reload
```

Run the frontend in another terminal:

```bash
npm run dev
```

Open `http://localhost:5173` for the React UI.

The app will open in your browser at `http://localhost:8501`

### Using the Application

1. **Landing Page**: View the futuristic hero section with 3D animations
2. **Input**: Paste your rental agreement clause in the text area
3. **Analyze**: Click "✨ Simplify Clause" button
4. **Results**: View the risk level and plain English explanation

### Example Clauses

Try these example clauses:

**Low Risk:**
```
The tenant must provide written notice of at least 30 days prior to vacating the premises.
```

**Medium Risk:**
```
The landlord reserves the right to increase the monthly rent with 30 days written notice to the tenant.
```

**High Risk:**
```
The tenant shall be responsible for all repairs and maintenance to the premises, including structural repairs, regardless of the cause of damage.
```

## 🎨 UI Features

### Advanced Glassmorphism
- Backdrop blur effects
- Semi-transparent panels
- Dynamic glow borders based on risk level

### 3D Animations
- Integrated Spline 3D viewer
- Floating abstract shapes
- Smooth CSS keyframe animations

### Risk-Based Styling
- **Low Risk**: Pulsing green glow
- **Medium Risk**: Pulsing amber glow
- **High Risk**: Pulsing red glow

### Custom Animations
- Hero entrance animations
- Scroll-reveal effects
- Loading spinners
- Smooth transitions

## ⚡ Performance Optimizations

### Model Loading
- Singleton pattern for model caching
- Automatic device detection (CUDA/MPS/CPU)
- FP16 precision on GPU for faster inference
- Low memory mode enabled

### Inference
- `torch.no_grad()` context for inference
- KV cache enabled for generation
- Efficient tokenization with fast tokenizers
- Optimized generation parameters

### Caching
- `@st.cache_resource` for model loading
- Persistent model in memory across requests

## 🔧 Configuration

### Model Parameters

Edit in `inference.py`:

```python
def generate(
    self,
    clause: str,
    max_new_tokens: int = 200,      # Max tokens to generate
    temperature: float = 0.7,        # Sampling temperature
    top_p: float = 0.9,             # Nucleus sampling
    top_k: int = 50,                # Top-k sampling
    repetition_penalty: float = 1.1  # Repetition penalty
)
```

### UI Customization

Edit CSS in `app.py` inside the `inject_custom_css()` function.

## 🐛 Troubleshooting

### Model Not Found
```
FileNotFoundError: Model directory not found: ./model
```
**Solution**: Ensure your model is in the correct directory

### Out of Memory
```
RuntimeError: CUDA out of memory
```
**Solution**: The model will automatically fall back to CPU. Close other applications to free memory.

### Import Errors
```
ModuleNotFoundError: No module named 'transformers'
```
**Solution**: Install requirements: `pip install -r requirements.txt`

## 📊 Model Information

- **Base Model**: Gemma 3 270M
- **Fine-tuning**: Rental agreement clauses
- **Task**: Text generation with risk classification
- **Format**: Hugging Face Transformers
- **Inference**: Local-first, no API calls

## 🔐 Privacy & Security

- **100% Local**: No data sent to external servers
- **No Analytics**: No tracking or telemetry
- **Private Processing**: All inference runs on your machine
- **No Storage**: Clauses are not saved or logged

## 📝 License

This project is for educational and personal use.

## 🤝 Contributing

This is a template project. Feel free to:
- Customize the UI
- Adjust model parameters
- Add new features
- Improve performance

## 📞 Support

For issues:
1. Check the model is in `./model/` directory
2. Verify Python version (3.10+)
3. Ensure all dependencies are installed
4. Check console logs for errors

## 🎓 Technical Details

### Architecture
- **Frontend**: Streamlit with custom HTML/CSS
- **Backend**: PyTorch + Transformers
- **Model**: Gemma 3 270M (local)
- **Inference**: Optimized generation pipeline

### Code Quality
- Type hints throughout
- Comprehensive error handling
- Logging for debugging
- Clean architecture (separation of concerns)

### Enterprise Standards
- Singleton pattern for resources
- Proper exception handling
- Efficient memory management
- Production-ready code structure

## 🚀 Next Steps

1. **Connect Your Model**: Place your fine-tuned model in `./model/`
2. **Customize**: Adjust colors, animations, and parameters
3. **Deploy**: Run locally or deploy to a private server
4. **Extend**: Add more clause types or features

---

**Built with ❤️ for legal clarity and privacy**
