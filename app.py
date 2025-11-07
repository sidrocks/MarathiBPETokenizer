# ...existing code...
"""
Gradio app for Marathi BPE Tokenizer — redesigned UI: elegant, business-oriented styling.
Usage: python app.py
"""
from typing import Tuple, List, Dict
import re

import gradio as gr

from tokenizer import MarathiBPETokenizer  # type: ignore

# Accent palette: bright but refined accents for token chips
ACCENTS = [
    "#1FB6FF",  # azure
    "#00D4B8",  # teal
    "#FFB86B",  # warm amber
    "#FF6B6B",  # coral
    "#A78BFA",  # muted violet
    "#FFD166",  # soft yellow
    "#8ED1FC",  # light sky
    "#6CE0B6",  # mint
]


def _token_text(tokenizer: MarathiBPETokenizer, tid: int) -> str:
    """Resolve token id to readable text using common fallbacks."""
    try:
        if hasattr(tokenizer, "decode"):
            out = tokenizer.decode([tid])
            if out:
                return out
    except Exception:
        pass

    if isinstance(getattr(tokenizer, "id_to_token", None), dict):
        return tokenizer.id_to_token.get(tid, f"<{tid}>")

    vocab = getattr(tokenizer, "vocab", None)
    if isinstance(vocab, dict):
        if tid in vocab:
            return vocab[tid]
        for k, v in vocab.items():
            if v == tid:
                return k

    return f"<{tid}>"


def tokenize_and_visualize(text: str, tokenizer: MarathiBPETokenizer) -> Tuple[str, str, str]:
    """Return (visual_html, count_card_html, token_ids_table_html)."""
    if not text or not text.strip():
        placeholder = (
            "<div style='color:#9CA3AF; font-size:15px; padding:12px;'>"
            "Enter Marathi text and click Analyze.</div>"
        )
        return placeholder, "<div style='color:#9CA3AF;'>Token count will appear here</div>", placeholder

    # Try bulk encode; fallback to per-word
    try:
        token_ids: List[int] = tokenizer.encode(text)
    except Exception:
        token_ids = []
        for part in text.split():
            try:
                token_ids.extend(tokenizer.encode(part))
            except Exception:
                continue

    # map unique token ids -> accent color
    tid_to_color: Dict[int, str] = {}
    unique_tids: List[int] = []
    for tid in token_ids:
        if tid not in tid_to_color:
            tid_to_color[tid] = ACCENTS[len(unique_tids) % len(ACCENTS)]
            unique_tids.append(tid)

    # Visualization tile (azure-toned business tile)
    vis_outer = [
        '<div style="padding:18px; border-radius:12px; background:linear-gradient(180deg,#063b66 0%,#0a2b48 100%);'
        'color:#F8FAFC; font-family:Inter, \'Noto Sans Devanagari\', Arial, sans-serif; font-size:18px; line-height:2;">'
    ]

    # split text into tokens/chunks for visualization (use tokenizer.pattern if available)
    pattern = getattr(tokenizer, "pattern", r"\S+")
    chunks = re.findall(pattern, text)
    token_idx = 0
    token_rows = []  # list of (idx, tid, token_text, color) for table

    for chunk in chunks:
        # prefer tokenizer's _apply_bpe if available, else encode chunk
        if hasattr(tokenizer, "_apply_bpe"):
            try:
                chunk_tids = tokenizer._apply_bpe(chunk)
            except Exception:
                chunk_tids = tokenizer.encode(chunk) if hasattr(tokenizer, "encode") else []
        else:
            try:
                chunk_tids = tokenizer.encode(chunk)
            except Exception:
                chunk_tids = []

        for tid in chunk_tids:
            token_text = _token_text(tokenizer, tid)
            color = tid_to_color.get(tid, ACCENTS[0])
            token_rows.append((token_idx, tid, token_text, color))

            # bright chip with subtle border and drop
            vis_outer.append(
                f'<span class="token-chip" data-idx="{token_idx}" '
                f'style="background:{color}; color:#fff; padding:8px 12px; margin:6px 6px 6px 0; '
                f'border-radius:10px; display:inline-block; font-weight:600; box-shadow:0 6px 18px rgba(3,12,26,0.35); '
                f'text-shadow:0 1px 2px rgba(0,0,0,0.25);">'
                f'{token_text}</span>'
            )
            token_idx += 1

    vis_outer.append("</div>")
    visual_html = "".join(vis_outer)

    # Count card: clean slate card
    count_html = (
        '<div style="padding:14px; border-radius:10px; background:linear-gradient(180deg,#f8fbff 0%,#eaf3ff 100%);'
        'color:#0b2540; text-align:center; font-family:Inter, Arial, sans-serif;">'
        f'<div style="font-size:28px; font-weight:700;">{len(token_ids)}</div>'
        f'<div style="color:#567096; margin-top:6px;">Total tokens • {len(unique_tids)} unique</div>'
        "</div>"
    )

    # Token IDs table: elegant white text on soft azure panel
    table_parts = [
        '<div style="padding:12px; border-radius:10px; background:#083E8C; color:#FFFFFF; max-height:420px; overflow:auto;">',
        '<table style="width:100%; border-collapse:collapse; font-family:Menlo, Monaco, monospace; font-size:13px;">',
        '<thead><tr style="text-align:left; color:red;"><th style="padding:8px 10px;">Idx</th><th style="padding:8px 10px;">Token ID</th><th style="padding:8px 10px;">Token</th><th style="padding:8px 10px;">Color</th></tr></thead>',
        "<tbody>"
    ]

    for idx, tid, ttext, color in token_rows:
        table_parts.append(
            '<tr style="border-bottom:1px solid rgba(255,255,255,0.05);">'
            f'<td style="padding:8px 10px; color:#C9D6E6;">{idx}</td>'
            f'<td style="padding:8px 10px; font-weight:700; color:#FFFFFF;">{tid}</td>'
            f'<td style="padding:8px 10px; color:#FFFFFF;">{ttext!r}</td>'
            f'<td style="padding:8px 10px;"><span style="display:inline-block; background:{color}; padding:6px 14px; border-radius:8px; box-shadow:0 6px 14px rgba(3,12,26,0.28);"></span></td>'
            "</tr>"
        )

    table_parts.extend(["</tbody></table></div>"])
    token_ids_html = "".join(table_parts)

    return visual_html, count_html, token_ids_html


def create_app(tokenizer: MarathiBPETokenizer) -> gr.Blocks:
    """Build Gradio Blocks UI with refined, business styling."""
    css = """
    <style>
      :root{
        --panel-bg:#0b2540;
        --tile-azure:#083E8C;
        --muted-text:#9CA3AF;
        --header-grey:#374151;
      }
      /* Page baseline */
      body { background: linear-gradient(180deg,#061328 0%, #071627 100%); font-family:Inter, "Noto Sans Devanagari", Arial, sans-serif; }

      /* Header */
      #header { margin-bottom:14px; }
      .app-title { color: var(--header-grey); font-weight:700; font-size:20px; margin:0; }
      .app-sub { color: var(--muted-text); margin:4px 0 0 0; }

      /* Token chip hover */
      .token-chip { transition: transform 0.16s ease, box-shadow 0.16s ease; cursor:default; }
      .token-chip:hover { transform: translateY(-6px); box-shadow:0 28px 48px rgba(3,12,26,0.55); }

      /* Examples styling (compatible across Gradio versions) */
      .gr-examples, .gr-examples td, .gr-examples th { background: transparent !important; color: #E6EEF7 !important; }

      /* Make Gradio tooltips readable */
      .gradio-tooltip { color:#081026 !important; background:#F3F7FB !important; }

      /* Responsive columns spacing */
      .gr-row { gap:18px; }

      /* Small utility */
      .muted { color: var(--muted-text); font-size:13px; }
    </style>
    """

    with gr.Blocks(css="") as demo:
        # Inject CSS
        gr.HTML(css, visible=False)

        # Header area (remove unsupported 'classes' kwarg for compatibility)
        with gr.Row(elem_id="header"):
            with gr.Column(scale=1):
                gr.Markdown(
                    "<div><h1 class='app-title' style='display:inline-block;'>Marathi BPE Tokenizer</h1>"
                    "<div class='app-sub'>Enterprise token inspection & visualization</div></div>"
                )

        # Main content: two-column layout
        with gr.Row():
            # Left: input + examples
            with gr.Column(scale=1):
                input_text = gr.Textbox(
                    label="Input Text",
                    placeholder="नमस्ते, मी एक मराठी टोकनायझर आहे",
                    lines=6
                )
                analyze_btn = gr.Button("Analyze", variant="primary")
                gr.Markdown("<div class='muted' style='margin-top:8px;'>Sample inputs</div>")
                gr.Examples(
                    examples=[
                        ["नमस्ते, मी एक मराठी टोकनायझर आहे."],
                        ["क्रिकेट - लहान मुले बागेत क्रिकेट खेळत आहेत."],
                        ["गाडी हळूहू चालवा किंवा आपल्याला अपघात होऊ शकतो."],
                        ["सचिन तेंडुलकर हा आमचा अव्वल क्रिकेटपटू आहे."],
                    ],
                    inputs=[input_text],
                )

            # Right: visual tile, count card, token table
            with gr.Column(scale=1):
                # visual tile
                visual_out = gr.HTML("<div class='muted'>Token visualization will appear here</div>")
                # compact row for count card
                count_out = gr.HTML("<div class='muted'>Token count will appear here</div>")
                # token ids table
                table_out = gr.HTML("<div class='muted'>Token details will appear here</div>")

        # Processing closure binds tokenizer instance
        def _process(text: str):
            return tokenize_and_visualize(text or "", tokenizer)

        analyze_btn.click(fn=_process, inputs=[input_text], outputs=[visual_out, count_out, table_out])
        input_text.submit(fn=_process, inputs=[input_text], outputs=[visual_out, count_out, table_out])

    return demo


def main():
    tokenizer = MarathiBPETokenizer()
    try:
        tokenizer.load_vocab("model/vocab.json")
        print("✓ Loaded vocabulary successfully")
    except FileNotFoundError:
        print("ERROR: Vocabulary file not found at 'model/vocab.json'")
        print("Run: python train.py to train and save the tokenizer.")
        return

    demo = create_app(tokenizer)
    demo.launch(share=True)


if __name__ == "__main__":
    main()
# ...existing code...