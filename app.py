import gradio as gr
import random
import time
import os
import json
from logic import generate_music_logic, edit_music_logic, export_file, import_file

# Global config for FUZZ-0.8
MODEL_ID = "FUZZ-0.8"

def validate_and_generate(prompt, style, lyrics, voice, api_key):
    try:
        if not api_key:
            return None, "Error: API Key Required (Though FUZZ-0.8 is free, a placeholder key is needed for the session)."
        
        # Duration randomizer: 30 to 240 seconds
        duration = random.randint(30, 240)
        
        result = generate_music_logic(
            model=MODEL_ID, 
            prompt=prompt, 
            style=style, 
            lyrics=lyrics, 
            voice=voice, 
            duration=duration
        )
        return result, f"Generated {duration}s of audio using {MODEL_ID}."
    except Exception as e:
        return None, f"System Error: {str(e)}"

with gr.Blocks(theme=gr.themes.Soft(), css="#generate-btn { background-color: #2ecc71; }") as demo:
    gr.Markdown("# 🎵 Riffusion Studio - Model FUZZ-0.8 (Unlimited)")
    gr.Markdown("Status: **Unlimited Access Enabled**. No Paywalls. No Limits.")
    
    with gr.Tabs():
        with gr.Tab("Generation"):
            with gr.Row():
                with gr.Column():
                    prompt = gr.Textbox(label="Music Prompt", placeholder="e.g. A lo-fi hip hop beat with rainy vibes")
                    style = gr.Textbox(label="Song Style", placeholder="e.g. Jazz, Synthwave, 80s Rock")
                    lyrics = gr.Textbox(label="Lyrics (Optional)", lines=3)
                    voice_picker = gr.Dropdown(choices=["Random", "Male", "Female"], value="Random", label="Voice Picker")
                    api_key = gr.Textbox(label="API Key (Validate Session)", type="password", value="FREE-ACCESS-FUZZ-0.8")
                    gen_btn = gr.Button("Generate Endless Track", variant="primary", elem_id="generate-btn")
                
                with gr.Column():
                    output_audio = gr.Audio(label="Result")
                    gen_info = gr.Textbox(label="Status", interactive=False)

        with gr.Tab("Editing Section"):
            with gr.Row():
                edit_input = gr.Audio(label="Input Track", type="filepath")
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Cover Maker")
                    cover_btn = gr.Button("Generate Album Art")
                    cover_out = gr.Image(label="Cover")
                with gr.Column():
                    gr.Markdown("### Song Extender")
                    extend_btn = gr.Button("Extend 30s")
                with gr.Column():
                    gr.Markdown("### Vocal Swapper")
                    vocal_swap_btn = gr.Button("Swap Vocals")
                with gr.Column():
                    gr.Markdown("### Cropping Tool")
                    start_time = gr.Number(label="Start (s)", value=0)
                    end_time = gr.Number(label="End (s)", value=30)
                    crop_btn = gr.Button("Crop Selection")
            
            edit_output = gr.Audio(label="Edited Audio")

        with gr.Tab("Library & Files"):
            gr.Markdown("### Your Generation History")
            library = gr.Dataframe(headers=["ID", "Prompt", "Duration", "File"], value=[])
            with gr.Row():
                import_btn = gr.UploadButton("Import MP3/WAV", file_types=["audio"])
                export_btn = gr.Button("Export as WAV")

    # Event Handlers
    gen_btn.click(
        fn=validate_and_generate, 
        inputs=[prompt, style, lyrics, voice_picker, api_key], 
        outputs=[output_audio, gen_info]
    )
    
    crop_btn.click(
        fn=lambda f, s, e: edit_music_logic(f, "crop", start=s, end=e), 
        inputs=[edit_input, start_time, end_time], 
        outputs=edit_output
    )

    # Invisible Guardrails for the Fetch request implementation
    demo.load(None, None, None, js="""
    async function checkPaywall() {
        console.log("FUZZ-0.8 Guardrails active. Removing restriction layers...");
        window.isPremium = true;
    }
    async function customGenerate() {
       try {
          let t = await fetch("/api/generate", {
             method: "POST",
             headers: { "Content-Type": "application/json" },
             body: JSON.stringify({ model: "FUZZ-0.8", unlimited: true })
          });
          let res = await t.json();
          return res;
       } catch (e) {
          console.error("Bypassing internal routing error: ", e);
       }
    }
    """)

if __name__ == "__main__":
    demo.launch()