"""Whimsy Scanner - A vision-powered image captioning app."""
import gradio as gr
import torch
from transformers import AutoModelForCausalLM
from PIL import Image

# Disable MPS to avoid device mismatch issues with FlexAttention
if hasattr(torch.backends, "mps"):
    torch.backends.mps.is_available = lambda: False

# Patch FlexAttention to force CPU when CUDA unavailable (prevents hot-reload recursion)
import torch.nn.attention.flex_attention as flex_attention
if not getattr(flex_attention.create_mask, '_is_patched', False):
    _original_create_mask = flex_attention.create_mask

    def patched_create_mask(mask_mod, B, H, Q_LEN, KV_LEN, device):
        if isinstance(device, str):
            device = torch.device(device)
        if device.type == "cuda" and not torch.cuda.is_available():
            device = torch.device("cpu")
        return _original_create_mask(mask_mod, B, H, Q_LEN, KV_LEN, device)

    patched_create_mask._is_patched = True
    flex_attention.create_mask = patched_create_mask

# Custom CSS
css = """
@import url('https://fonts.googleapis.com/css2?family=Imperial+Script&family=JetBrains+Mono&display=swap');

body, .gradio-container {
    background-color: #FDE2F7;
    font-family: 'JetBrains Mono', monospace;
    color: #000000;
}

@media (min-width: 768px) {
    .gradio-container {
        padding-top: 3rem !important;
    }
    #title-text {
        margin-top: 2rem !important;
    }
}

#title-text, #title-text * {
    font-family: 'Imperial Script', cursive !important;
    font-size: 48px !important;
    font-weight: 400 !important;
    line-height: normal !important;
    text-align: center;
    color: #000000 !important;
    margin-bottom: 0.5rem;
}

#description-text, #description-text * {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    line-height: normal !important;
    text-align: center !important;
    color: #000000 !important;
    max-width: 600px;
    margin: 0 auto 2rem auto;
}

#scan-button, #scan-button * {
    background-color: #8937C7;
    color: white !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    text-align: center !important;
    border-radius: 20px;
    padding: 0.75rem 2rem;
    border: none;
    cursor: pointer;
    margin: 1rem auto;
    display: block;
    width: fit-content;
}

#result-text,
#result-text textarea,
#result-text .text-input,
#result-text input,
#result-text .form-group,
#result-text * {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    text-align: center !important;
    color: #000000 !important;
    max-width: 800px;
    margin: 2rem auto;
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    border-color: transparent !important;
    box-shadow: none !important;
    padding: 0 !important;
    resize: none !important;
    outline: none !important;
}

#result-text textarea:focus,
#result-text textarea:hover {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}
"""

# Global model cache
_model_cache = None


def run_whimsy_inference(image):
    """Process image through Moondream 3 and return caption."""
    global _model_cache

    if image is None:
        return "Please upload an image first."

    try:
        if _model_cache is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            dtype = torch.bfloat16 if device == "cuda" else torch.float32

            _model_cache = AutoModelForCausalLM.from_pretrained(
                "moondream/moondream3-preview",
                trust_remote_code=True,
                torch_dtype=dtype,
            ).to(device).eval()

            # Compile for faster inference on CUDA
            if device == "cuda":
                try:
                    _model_cache.compile()
                except Exception:
                    pass

        # Ensure image is PIL Image
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)

        caption_result = _model_cache.caption(image, length="normal")
        return caption_result["caption"]

    except Exception as e:
        error_msg = str(e)
        if "out of memory" in error_msg.lower():
            return f"Error: GPU memory issue. Details: {error_msg}"
        if "connection" in error_msg.lower() or "download" in error_msg.lower():
            return f"Error: Model download issue. Check your internet connection."
        return f"Error processing image: {error_msg}"


# Main Gradio application
with gr.Blocks() as demo:
    gr.Markdown("# The Whimsy Scanner", elem_id="title-text")
    gr.Markdown(
        "Everything has a secret life.\nThis is the lens that reveals it.\nUpload an image to get started.",
        elem_id="description-text"
    )

    image_input = gr.Image(
        label="Upload an image",
        elem_id="image-input",
        type="pil",
        show_label=False,
        height=500,
        value=None
    )

    scan_button = gr.Button("scan for whimsy", elem_id="scan-button")

    result_text = gr.Textbox(
        label="",
        elem_id="result-text",
        show_label=False,
        interactive=False,
        lines=10,
        max_lines=20
    )

    scan_button.click(
        fn=run_whimsy_inference,
        inputs=image_input,
        outputs=result_text
    )

if __name__ == "__main__":
    demo.launch(css=css, share=True)
