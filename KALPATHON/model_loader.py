"""
Model Loader Module
Handles loading and initialization of the Hugging Face model and tokenizer.
Optimized for Gemma 3 270M with efficient device mapping and caching.
"""

import os
from typing import Tuple, Optional
from pathlib import Path
import logging

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.modeling_utils import PreTrainedModel
from transformers.tokenization_utils import PreTrainedTokenizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelLoader:
    """Singleton class for loading and managing the Hugging Face model."""
    
    _instance: Optional['ModelLoader'] = None
    _model: Optional[PreTrainedModel] = None
    _tokenizer: Optional[PreTrainedTokenizer] = None
    _device: Optional[torch.device] = None
    
    def __new__(cls) -> 'ModelLoader':
        """Ensure only one instance of ModelLoader exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """Initialize the model loader with device detection."""
        if self._device is None:
            self._device = self._get_optimal_device()
            logger.info(f"Using device: {self._device}")
    
    @staticmethod
    def _get_optimal_device() -> torch.device:
        """
        Detect and return the optimal device for inference.
        
        Returns:
            torch.device: The optimal device (CUDA, MPS, or CPU)
        """
        if torch.cuda.is_available():
            return torch.device("cuda")
        elif torch.backends.mps.is_available():
            return torch.device("mps")
        else:
            return torch.device("cpu")
    
    def load_model(
        self,
        model_path: str = "./model",
        trust_remote_code: bool = True,
        use_cache: bool = True
    ) -> Tuple[PreTrainedModel, PreTrainedTokenizer]:
        """
        Load the Hugging Face model and tokenizer from local path.
        
        Args:
            model_path: Path to the local model directory
            trust_remote_code: Whether to trust remote code in model
            use_cache: Whether to use model cache for faster inference
            
        Returns:
            Tuple of (model, tokenizer)
            
        Raises:
            FileNotFoundError: If model path doesn't exist
            RuntimeError: If model loading fails
        """
        # Return cached model if already loaded
        if self._model is not None and self._tokenizer is not None:
            logger.info("Using cached model and tokenizer")
            return self._model, self._tokenizer
        
        # Validate model path
        model_dir = Path(model_path)
        if not model_dir.exists():
            raise FileNotFoundError(
                f"Model directory not found: {model_path}\n"
                f"Please ensure your fine-tuned model is placed in {model_path}"
            )
        
        try:
            logger.info(f"Loading tokenizer from {model_path}...")
            self._tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                trust_remote_code=trust_remote_code,
                use_fast=True  # Use fast tokenizer for better performance
            )
            
            logger.info(f"Loading model from {model_path}...")
            self._model = AutoModelForCausalLM.from_pretrained(
                model_path,
                trust_remote_code=trust_remote_code,
                torch_dtype=torch.float16 if self._device.type == "cuda" else torch.float32,
                low_cpu_mem_usage=True,
                use_cache=use_cache
            )
            
            # Move model to optimal device
            self._model.to(self._device)
            
            # Set model to evaluation mode for inference
            self._model.eval()
            
            logger.info(
                f"Model loaded successfully on {self._device} "
                f"({self._model.num_parameters():,} parameters)"
            )
            
            return self._model, self._tokenizer
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise RuntimeError(f"Model loading failed: {str(e)}")
    
    @property
    def device(self) -> torch.device:
        """Get the current device being used."""
        return self._device
    
    def get_model_info(self) -> dict:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary containing model information
        """
        if self._model is None:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "device": str(self._device),
            "dtype": str(self._model.dtype),
            "parameters": self._model.num_parameters(),
            "model_type": self._model.config.model_type if hasattr(self._model, 'config') else "unknown"
        }


# Global singleton instance
model_loader = ModelLoader()


def get_model_and_tokenizer(
    model_path: str = "./model"
) -> Tuple[PreTrainedModel, PreTrainedTokenizer]:
    """
    Convenience function to get model and tokenizer.
    
    Args:
        model_path: Path to the local model directory
        
    Returns:
        Tuple of (model, tokenizer)
    """
    return model_loader.load_model(model_path)
