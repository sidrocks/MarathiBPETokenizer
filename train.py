# ...existing code...
"""
Training script for Marathi BPE Tokenizer.
Designed for extensibility and parameter-based runs.

Usage examples:
  python train.py --dataset ai4bharat/samanantar --subset mr --lang-side tgt --num-examples 10000 --vocab-size 5000
  python train.py --tokenizer-module my_tokenizers.bpe --tokenizer-class CustomTokenizer --vocab-size 8000
"""
from dataclasses import dataclass
import argparse
import logging
import os
import sys
from typing import Optional, Type

from datasets import load_dataset

# Default tokenizer import (can be overridden via CLI)
from tokenizer import MarathiBPETokenizer  # type: ignore

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@dataclass
class TrainConfig:
    dataset: str = "ai4bharat/samanantar"
    subset: Optional[str] = "mr"
    split: str = "train"
    lang_side: str = "tgt"
    num_examples: int = 10000
    vocab_size: int = 5000
    model_dir: str = "model"
    data_dir: str = "data"
    output_text_filename: str = "marathi_samanantar.txt"
    streaming: bool = True
    tokenizer_module: Optional[str] = None
    tokenizer_class: Optional[str] = None


def ensure_dirs(config: TrainConfig) -> None:
    os.makedirs(config.model_dir, exist_ok=True)
    os.makedirs(config.data_dir, exist_ok=True)


def import_tokenizer_class(module_name: Optional[str], class_name: Optional[str]) -> Type:
    """
    Dynamically import a tokenizer class if module_name and class_name provided.
    Otherwise, return the default MarathiBPETokenizer imported above.
    """
    if module_name and class_name:
        import importlib

        logging.info("Importing tokenizer class %s from module %s", class_name, module_name)
        module = importlib.import_module(module_name)
        tokenizer_cls = getattr(module, class_name)
        return tokenizer_cls
    logging.info("Using default MarathiBPETokenizer from tokenizer.py")
    return MarathiBPETokenizer


def load_training_texts(config: TrainConfig) -> str:
    """
    Load texts from the dataset according to configuration.
    Returns concatenated text (separated by double newlines).
    """
    logging.info("Loading dataset %s (subset=%s, split=%s, streaming=%s)",
                 config.dataset, config.subset, config.split, config.streaming)

    ds = load_dataset(config.dataset, config.subset, split=config.split, streaming=config.streaming)

    texts = []
    for i, example in enumerate(ds):
        if config.num_examples > 0 and i >= config.num_examples:
            break
        # Guard for missing key
        if config.lang_side not in example:
            logging.warning("example %d missing key '%s'; skipping", i, config.lang_side)
            continue
        texts.append(example[config.lang_side])
        if (i + 1) % 1000 == 0:
            logging.info("Loaded %d texts...", i + 1)

    logging.info("Loaded %d texts in total", len(texts))
    return "\n\n".join(texts)


def save_text(text: str, config: TrainConfig) -> str:
    path = os.path.join(config.data_dir, config.output_text_filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    logging.info("Saved training text to %s", path)
    return path


def train_and_save_tokenizer(tokenizer_cls: Type, text: str, config: TrainConfig) -> None:
    tokenizer = tokenizer_cls()
    logging.info("Training tokenizer with vocab size: %d", config.vocab_size)
    tokenizer.train(text, vocab_size=config.vocab_size)
    vocab_path = os.path.join(config.model_dir, "vocab.json")
    tokenizer.save_vocab(vocab_path)
    logging.info("Saved vocabulary to %s", vocab_path)


def parse_args(argv) -> TrainConfig:
    parser = argparse.ArgumentParser(description="Train a BPE tokenizer with parameterized options.")
    parser.add_argument("--dataset", type=str, default="ai4bharat/samanantar")
    parser.add_argument("--subset", type=str, default="kn", help="Dataset subset/config (e.g., language code).")
    parser.add_argument("--split", type=str, default="train")
    parser.add_argument("--lang-side", type=str, default="tgt", help="Which side of parallel data to use (src/tgt).")
    parser.add_argument("--num-examples", type=int, default=10000, help="Number of examples to load (0 for all).")
    parser.add_argument("--vocab-size", type=int, default=5000)
    parser.add_argument("--model-dir", type=str, default="model")
    parser.add_argument("--data-dir", type=str, default="data")
    parser.add_argument("--output-text-filename", type=str, default="Marathi_samanantar.txt")
    parser.add_argument("--no-streaming", dest="streaming", action="store_false", help="Disable streaming mode.")
    parser.add_argument("--tokenizer-module", type=str, default=None, help="Optional module path for tokenizer class.")
    parser.add_argument("--tokenizer-class", type=str, default=None, help="Class name in module for tokenizer.")
    args = parser.parse_args(argv)

    return TrainConfig(
        dataset=args.dataset,
        subset=args.subset,
        split=args.split,
        lang_side=args.lang_side,
        num_examples=args.num_examples,
        vocab_size=args.vocab_size,
        model_dir=args.model_dir,
        data_dir=args.data_dir,
        output_text_filename=args.output_text_filename,
        streaming=args.streaming,
        tokenizer_module=args.tokenizer_module,
        tokenizer_class=args.tokenizer_class,
    )


def main(argv=None):
    cfg = parse_args(argv or sys.argv[1:])
    ensure_dirs(cfg)
    tokenizer_cls = import_tokenizer_class(cfg.tokenizer_module, cfg.tokenizer_class)

    text = load_training_texts(cfg)
    save_text(text, cfg)
    train_and_save_tokenizer(tokenizer_cls, text, cfg)


if __name__ == "__main__":
    main()