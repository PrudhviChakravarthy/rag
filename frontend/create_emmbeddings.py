import gradio as gr
from src.create_embeddings import (
    get_files,
    embed_documents)

def select_transformer(name):
    print(name)
    if name == "sentence transformer":
        choices =  ["all-MiniLM-L6-v2"]
    elif name == "huggingface transformer":
        choices =  ["bert-base-uncased","bert-large-cased"]
    else:
        choices =  ['no model found']
    return gr.Dropdown(choices=choices)


def create_embedding(tabs):
    with gr.TabItem("Embed Documents",id=1) as embed_tab:
        gr.Markdown("## Embed Documents")
        with gr.Row():
            select_files = gr.Dropdown(choices=get_files())
            refresh_files = gr.Button("Refresh files")
            refresh_files.click(lambda: gr.Dropdown(choices=get_files()),None,select_files)
        embedding_type = gr.Dropdown(choices=["sentence transformer", "huggingface transformer"],label="Embedding Type")
        embedding_model = gr.Dropdown(choices=[], label="Embedding Model", )
        store = gr.Radio(choices=["faiss","chroma"],value="faiss")
        with gr.Row():
            chunksize = gr.Slider(minimum=50, maximum=700 , step=50, label="Chunk size", value=200)
            chunk_overlap = gr.Slider(minimum=0, maximum=100 , step=20,value=20,label="Chunk overlap")
        embed_button = gr.Button("Embed")
        embed_output = gr.Textbox(label="Embedding Status")
        emmbed_back = gr.Button("Back")
        
        # Define action on embed button click
        embedding_type.change(fn = select_transformer,
                              inputs =[embedding_type],
                              outputs=[embedding_model])
         
        embed_button.click(fn=embed_documents,
                           inputs=[select_files,embedding_type, embedding_model,store,chunksize,chunk_overlap],
                           outputs=embed_output)
        
        emmbed_back.click(lambda : gr.Tabs(selected=0),None,tabs)

    return embed_tab
