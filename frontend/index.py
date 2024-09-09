import gradio as gr

def get_indexes(tabs):
    with gr.TabItem("Index",id = 0) as index:
        emmbeding = gr.Button(" -> GO TO EMMBEDDINGS TAB")
        emmbeding.click(lambda x : gr.Tabs(selected=1), None,outputs=tabs)
        
        uplaod = gr.Button("-> GO TO  UPLOAD TAB")
        uplaod.click(lambda x : gr.Tabs(selected=2), None,outputs=tabs)
        
        chat = gr.Button("-> CHAT WITH LLM.")
        chat.click(lambda:gr.Tabs(selected=3), None, tabs )
    return index