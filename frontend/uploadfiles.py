import gradio as gr
from src.uplaod_files import save_file_to_db


def create_upload_files(tabs):

    # Upload file interface
    with gr.TabItem("Upload",id=2) as upload:
        gr.Markdown("## Upload a File and Save to DB")

        file_upload = gr.File(label="Upload a File",file_types=['pdf','docx'])
        upload_button = gr.Button("Save File.")
        upload_status = gr.Textbox(label="Upload Status")
    
        # Save uploaded file on button click
        upload_button.click(
            fn=save_file_to_db, 
            inputs=[file_upload], 
            outputs=upload_status
        )

        upload_back = gr.Button("Menu")
        upload_back.click(lambda : gr.Tabs(selected=0),None,tabs)
        
    

    return upload

# Run the Gradio app
