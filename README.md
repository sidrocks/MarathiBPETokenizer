<!-- ...existing code... -->

# Marathi BPE Tokenizer

Project to build and visualize a language-specific Byte-Pair Encoding (BPE) tokenizer for Marathi.

**Objective**  
Build a BPE tokenizer that satisfies:
- Vocabulary size > 5000 tokens
- Compression ratio ≥ 3.0

---

## Why BPE for Indian languages

- Indian languages (Devanagari scripts such as Marathi) are morphologically rich with many inflected and compound forms.  
- BPE learns frequent subword fragments (roots, suffixes, prefixes), reducing OOV issues while keeping vocabulary manageable.  
- BPE balances vocabulary size and sequence length: more robust than pure word-level tokenizers, and more compact than character-level tokenizers.

---

## Dataset

Primary dataset used in examples and training:
- `ai4bharat/samanantar` (Hugging Face datasets) — multilingual parallel corpora; use the Marathi subset (`--subset mr`) for training.

Hugging Face: https://huggingface.co/datasets/ai4bharat/samanantar

---

## Repository layout

- `tokenizer.py` — BPE tokenizer implementation (train/save/load/encode/decode).
- `train.py` — training script (dataset load, BPE merges, save `model/vocab.json`).
- `app.py` — Gradio visualization UI.
- `model/` — trained artifacts (e.g., `vocab.json`).
- `data/` — optional saved training text and samples.
- `README.md` — this file.

---

## Setup (Windows)

1. Create and activate virtual environment
```powershell
python -m venv .env
# PowerShell
.\.env\Scripts\Activate.ps1
# CMD
.\.env\Scripts\activate.bat
```

2. Install dependencies
```bash
pip install -r requirements.txt
```
If you don't have `requirements.txt`:
```bash
pip install gradio datasets
# add other packages if tokenizer requires (e.g., sentencepiece)
```

---

## Train the tokenizer

Example (Marathi subset, target vocab 6000 recommended to exceed 5000):

```bash
python train.py \
  --dataset ai4bharat/samanantar \
  --subset mr \
  --split train \
  --lang-side tgt \
  --num-examples 20000 \
  --vocab-size 6000 \
  --model-dir model \
  --data-dir data
```

Notes:
- `--num-examples` — number of examples to use (0 = all when using streaming).
- `--vocab-size` — set > 5000 to meet the requirement.
- Output: `model/vocab.json` (or whatever the script saves).

---

## Verify objectives

1. Check vocabulary size
```python
import json
v = json.load(open("model/vocab.json", "r", encoding="utf-8"))
print("Vocab size:", len(v))
```

2. Compute compression ratio (sample)
```python
from tokenizer import MarathiBPETokenizer

tok = MarathiBPETokenizer()
tok.load_vocab("model/vocab.json")

text = open("data/marathi_sample.txt", encoding="utf-8").read()
chars = len(text)
tokens = tok.encode(text)
ratio = chars / len(tokens) if tokens else 0.0
print(f"chars={chars}, tokens={len(tokens)}, compression_ratio={ratio:.2f}")
```
Aim: `compression_ratio >= 3.0`. If below:
- Increase vocab size and retrain.
- Use more training data.
- Improve pre-tokenization rules to capture frequent subword patterns.

---

## Run the Gradio app

1. Ensure `model/vocab.json` exists (run `train.py` if missing).  
2. Launch:
```bash
python app.py
```
3. Open the local URL printed by Gradio. Paste Marathi text and click Analyze.

---

## Tips for better results

- Use diverse and large training data to capture language variability.  
- Tune pre-tokenization regex for Marathi to avoid splitting meaningful subword units.  
- Monitor token frequency and merge behavior while training.  
- Evaluate on held-out text to ensure compression/generalization.

---

## Licensing & credits

- Dataset credit: ai4bharat / samanantar. Respect dataset license and citation.  
- Add your preferred license (MIT/Apache) to the repo before publishing.

---

## Extras (suggested improvements)

- Add `evaluate_metrics.py` to compute vocab size and compression automatically after training.  
- Save training logs and merge stats to help debugging and tuning.  
- Include unit tests for tokenizer encode/decode operations.

---
```<!-- filepath: c:\Users\sidhe\TSAIV4\Session11-Assignment\mr-bpe-tokenizer-main\README.md -->
<!-- ...existing code... -->

# Marathi BPE Tokenizer

Project to build and visualize a language-specific Byte-Pair Encoding (BPE) tokenizer for Marathi.

**Objective**  
Build a BPE tokenizer that satisfies:
- Vocabulary size > 5000 tokens
- Compression ratio ≥ 3.0

---

## Why BPE for Indian languages

- Indian languages (Devanagari scripts such as Marathi) are morphologically rich with many inflected and compound forms.  
- BPE learns frequent subword fragments (roots, suffixes, prefixes), reducing OOV issues while keeping vocabulary manageable.  
- BPE balances vocabulary size and sequence length: more robust than pure word-level tokenizers, and more compact than character-level tokenizers.

---

## Dataset

Primary dataset used in examples and training:
- `ai4bharat/samanantar` (Hugging Face datasets) — multilingual parallel corpora; use the Marathi subset (`--subset mr`) for training.

Hugging Face: https://huggingface.co/datasets/ai4bharat/samanantar

---

## Repository layout

- `tokenizer.py` — BPE tokenizer implementation (train/save/load/encode/decode).
- `train.py` — training script (dataset load, BPE merges, save `model/vocab.json`).
- `app.py` — Gradio visualization UI.
- `model/` — trained artifacts (e.g., `vocab.json`).
- `data/` — optional saved training text and samples.
- `README.md` — this file.

---

## Setup (Windows)

1. Create and activate virtual environment
```powershell
python -m venv .env
# PowerShell
.\.env\Scripts\Activate.ps1
# CMD
.\.env\Scripts\activate.bat
```

2. Install dependencies
```bash
pip install -r requirements.txt
```
If you don't have `requirements.txt`:
```bash
pip install gradio datasets
# add other packages if tokenizer requires (e.g., sentencepiece)
```

---

## Train the tokenizer

Example (Marathi subset, target vocab 6000 recommended to exceed 5000):

```bash
python train.py \
  --dataset ai4bharat/samanantar \
  --subset mr \
  --split train \
  --lang-side tgt \
  --num-examples 20000 \
  --vocab-size 6000 \
  --model-dir model \
  --data-dir data
```

Notes:
- `--num-examples` — number of examples to use (0 = all when using streaming).
- `--vocab-size` — set > 5000 to meet the requirement.
- Output: `model/vocab.json` (or whatever the script saves).

---

## Verify objectives

1. Check vocabulary size
```python
import json
v = json.load(open("model/vocab.json", "r", encoding="utf-8"))
print("Vocab size:", len(v))
```

2. Compute compression ratio (sample)
```python
from tokenizer import MarathiBPETokenizer

tok = MarathiBPETokenizer()
tok.load_vocab("model/vocab.json")

text = open("data/marathi_sample.txt", encoding="utf-8").read()
chars = len(text)
tokens = tok.encode(text)
ratio = chars / len(tokens) if tokens else 0.0
print(f"chars={chars}, tokens={len(tokens)}, compression_ratio={ratio:.2f}")
```
Aim: `compression_ratio >= 3.0`. If below:
- Increase vocab size and retrain.
- Use more training data.
- Improve pre-tokenization rules to capture frequent subword patterns.

---

## Run the Gradio app

1. Ensure `model/vocab.json` exists (run `train.py` if missing).  
2. Launch:
```bash
python app.py
```
3. Open the local URL printed by Gradio. Paste Marathi text and click Analyze.

---
## Training Logs

    2025-11-07 22:03:09,022 INFO Training tokenizer with vocab size: 6000
    Initial vocab size (unique characters): 209
    Training on 660268 characters
    Merged 1000/5791 pairs, vocab size: 1209
    Merged 2000/5791 pairs, vocab size: 2209
    Merged 3000/5791 pairs, vocab size: 3209
    Merged 4000/5791 pairs, vocab size: 4209
    Merged 5000/5791 pairs, vocab size: 5209
    2025-11-07 22:10:25,119 INFO Saved vocabulary to model\vocab.json
    ============================================================
    Training Complete!
    ============================================================
    Final vocab size: 6000
    Original characters: 660268
    Final BPE tokens: 159781
    Compression ratio: 4.13x
    ============================================================
---
## Try the App 🚀

The tokenizer visualization app is deployed on Hugging Face Spaces:  
🔗 [Marathi BPE Tokenizer Demo](https://huggingface.co/spaces/sidharthg/marathi-bpe-tokenizer)

<img width="1504" height="909" alt="image" src="https://github.com/user-attachments/assets/8b06a4ce-1141-48a3-9a97-2029d380b698" />

### How to use:
1. Visit the demo link above
2. Enter Marathi text in the input box (or use sample texts)
3. Click "Analyze Text" to see:
   - Color-coded token visualization
   - Token count and statistics
   - Detailed token ID mapping table

Example inputs are provided below the text box - click any to load into the editor.

### Features:
- Interactive token chips with hover details
- Token frequency analysis
- Compression statistics
- Rich visualization of subword splits
- Mobile-friendly interface

### Limitations:
- Max input length: ~500 tokens
- Processing time varies with text length
- Requires modern browser for best experience

---
## Tips for better results

- Use diverse and large training data to capture language variability.  
- Tune pre-tokenization regex for Marathi to avoid splitting meaningful subword units.  
- Monitor token frequency and merge behavior while training.  
- Evaluate on held-out text to ensure compression/generalization.

---

## Licensing & credits

- Dataset credit: ai4bharat / samanantar. Respect dataset license and citation.  
- Add your preferred license (MIT/Apache) to the repo before publishing.

---

## Extras (suggested improvements)

- Add `evaluate_metrics.py` to compute vocab size and compression automatically after training.  
- Save training logs and merge stats to help debugging and tuning.  
- Include unit tests for tokenizer encode/decode operations.


---

