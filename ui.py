from importlib import reload
import gradio as gr

# Custom CSS to replicate the design
css = """
@import url('https://fonts.googleapis.com/css2?family=Imperial+Script&family=JetBrains+Mono&display=swap');

body, .gradio-container {
    background-color: #FDE2F7;
    font-family: 'JetBrains Mono', monospace;
    color: #000000;
}

/* Add more space on top for desktop version */
@media (min-width: 768px) {
    .gradio-container {
        padding-top: 3rem !important;
    }
    
    #title-text {
        margin-top: 2rem !important;
    }
}

#title-text {
    font-family: 'Imperial Script', cursive !important;
    font-size: 48px !important;
    font-weight: 400 !important;
    line-height: normal !important;
    letter-spacing: 0% !important;
    text-align: center;
    margin-bottom: 0.5rem;
    color: #000000 !important;
}

#title-text p,
#title-text h1,
#title-text * {
    font-family: 'Imperial Script', cursive !important;
    font-size: 48px !important;
    font-weight: 400 !important;
    line-height: normal !important;
    letter-spacing: 0% !important;
    color: #000000 !important;
}

#description-text {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    line-height: normal !important;
    letter-spacing: 0% !important;
    margin-bottom: 2rem;
    color: #000000 !important;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

#description-text p,
#description-text * {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    line-height: normal !important;
    letter-spacing: 0% !important;
    text-align: center !important;
    color: #000000 !important;
}

#scan-button {
    background-color: #8937C7;
    color: white;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    line-height: normal !important;
    letter-spacing: 0% !important;
    text-align: center !important;
    border-radius: 20px;
    padding: 0.75rem 2rem;
    border: none;
    cursor: pointer;
    margin-top: 1rem;
    width: fit-content;
    margin-left: auto;
    margin-right: auto;
    display: block;
}

#scan-button * {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    line-height: normal !important;
    letter-spacing: 0% !important;
    text-align: center !important;
    color: white !important;
}

"""

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

    scan_button.click(lambda x: None, inputs=image_input, outputs=[])

if __name__ == "__main__":
    demo.launch(css=css, share=True)