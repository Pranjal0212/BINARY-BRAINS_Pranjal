"""
Inference Module
Handles model inference with optimized generation parameters.
Supports batch processing and efficient token generation for Gemma 3.
"""

from typing import List, Dict, Optional
import logging
import re

import torch
from transformers.modeling_utils import PreTrainedModel
from transformers.tokenization_utils import PreTrainedTokenizer

logger = logging.getLogger(__name__)


class InferenceEngine:
    """Optimized inference engine for legal clause simplification."""
    
    def __init__(
        self,
        model: PreTrainedModel,
        tokenizer: PreTrainedTokenizer,
        device: torch.device
    ):
        """
        Initialize the inference engine.
        
        Args:
            model: The loaded Hugging Face model
            tokenizer: The tokenizer for the model
            device: The device to run inference on
        """
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        
        # Set padding token if not set
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
    
    @torch.no_grad()  # Disable gradient computation for inference
    def generate(
        self,
        clause: str,
        max_new_tokens: int = 200,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 50,
        repetition_penalty: float = 1.1,
        do_sample: bool = True
    ) -> str:
        """
        Generate simplified explanation for a legal clause.
        
        Args:
            clause: The input legal clause text
            max_new_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (higher = more random)
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter
            repetition_penalty: Penalty for repeating tokens
            do_sample: Whether to use sampling (vs greedy decoding)
            
        Returns:
            Generated explanation text
        """
        try:
            # Build prompt
            prompt = self._build_prompt(clause)
            
            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            ).to(self.device)
            
            # Generate with optimized parameters
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                repetition_penalty=repetition_penalty,
                do_sample=do_sample,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                use_cache=True  # Enable KV cache for faster generation
            )
            
            # Decode output
            full_output = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )
            
            # Extract only the generated part (remove prompt)
            generated_text = full_output[len(prompt):].strip()
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            raise RuntimeError(f"Inference error: {str(e)}")
    
    def _build_prompt(self, clause: str) -> str:
        """
        Build the prompt for the model.
        
        Args:
            clause: Input legal clause
            
        Returns:
            Formatted prompt string
        """
        return f"Clause: {clause}\nExplanation:"
    
    def simplify_clause(
        self,
        clause: str,
        max_new_tokens: int = 200
    ) -> Dict[str, str]:
        """
        Simplify a legal clause and extract risk level.
        
        Args:
            clause: The input legal clause text
            max_new_tokens: Maximum tokens to generate
            
        Returns:
            Dictionary with 'risk' and 'explanation' keys
        """
        # Generate raw output
        raw_output = self.generate(clause, max_new_tokens=max_new_tokens)
        
        # Parse risk level and explanation
        risk, explanation = self._parse_output(raw_output)
        
        return {
            "risk": risk,
            "explanation": explanation
        }
    
    def _parse_output(self, output: str) -> tuple[str, str]:
        """
        Parse the model output to extract risk level and explanation.
        
        Args:
            output: Raw model output
            
        Returns:
            Tuple of (risk_level, explanation)
        """
        # Try to find risk level pattern: "Risk: <level>"
        risk_pattern = r'\b(Low|Medium|High)\s*(?:Risk)?:?\s*'
        risk_match = re.search(risk_pattern, output, re.IGNORECASE)
        
        if risk_match:
            risk_level = risk_match.group(1).capitalize()
            # Remove risk prefix from explanation
            explanation = re.sub(risk_pattern, '', output, flags=re.IGNORECASE).strip()
        else:
            # Default to Medium if no risk level found
            risk_level = "Medium"
            explanation = output.strip()
        
        # Clean up explanation
        explanation = self._clean_explanation(explanation)
        
        return risk_level, explanation
    
    def _clean_explanation(self, text: str) -> str:
        """
        Clean and format the explanation text.
        
        Args:
            text: Raw explanation text
            
        Returns:
            Cleaned explanation text
        """
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Remove excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove incomplete sentences at the end
        if text and not text[-1] in '.!?':
            # Find the last complete sentence
            last_period = max(
                text.rfind('.'),
                text.rfind('!'),
                text.rfind('?')
            )
            if last_period > len(text) // 2:  # Only if we're past halfway
                text = text[:last_period + 1]
        
        return text
    
    def batch_simplify(
        self,
        clauses: List[str],
        max_new_tokens: int = 200
    ) -> List[Dict[str, str]]:
        """
        Simplify multiple clauses in batch (future optimization).
        
        Args:
            clauses: List of legal clause texts
            max_new_tokens: Maximum tokens per generation
            
        Returns:
            List of dictionaries with risk and explanation
        """
        results = []
        for clause in clauses:
            try:
                result = self.simplify_clause(clause, max_new_tokens)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process clause: {str(e)}")
                results.append({
                    "risk": "Medium",
                    "explanation": "Error processing this clause. Please try again."
                })
        return results


def create_inference_engine(
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizer,
    device: torch.device
) -> InferenceEngine:
    """
    Factory function to create an inference engine.
    
    Args:
        model: The loaded model
        tokenizer: The tokenizer
        device: The device to use
        
    Returns:
        Configured InferenceEngine instance
    """
    return InferenceEngine(model, tokenizer, device)
