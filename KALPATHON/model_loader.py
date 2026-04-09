import os
from typing import Tuple

import streamlit as st
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_NAME = "google/gemma-3-270m"
LORA_ADAPTER_DIR = "./model"


def _pick_dtype() -> torch.dtype:
    if torch.cuda.is_available():
        # Widely supported on consumer GPUs; bfloat16 is not always available.
        return torch.float16
    return torch.float32


@st.cache_resource(show_spinner=False)
def load_model() -> Tuple[AutoTokenizer, torch.nn.Module]:
    """
    Loads tokenizer + base model, then attaches LoRA adapter from ./model/.
    This is cached so it only loads once per Streamlit session.
    """
    if not os.path.isdir(LORA_ADAPTER_DIR):
        raise FileNotFoundError(
            f"LoRA adapter folder not found: {LORA_ADAPTER_DIR}. "
            "Expected ./model/ to contain adapter weights (not a full model)."
        )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    dtype = _pick_dtype()
    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=dtype,
        device_map="auto" if torch.cuda.is_available() else None,
    )

    model = PeftModel.from_pretrained(base_model, LORA_ADAPTER_DIR)
    model.eval()

    # If we're on CPU, ensure the model is actually on CPU.
    if not torch.cuda.is_available():
        model.to(torch.device("cpu"))

    return tokenizer, model