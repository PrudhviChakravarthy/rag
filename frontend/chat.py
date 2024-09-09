import gradio as gr 
from src.chat import  chat_with_llm,get_files

 
def chat_with_model(tabs):
    with gr.Tab("Chat",id = 3) as chat_model:
        # Left panel with file selectors
        selected_file = gr.Dropdown(label="Files", choices=get_files(), value=[0])

        # Right panel with search configurations
        with gr.Row():
            top_k = gr.Slider(label="Top K", minimum=1, maximum=10, value=20, step=1)
            top_p = gr.Slider(label="Top P", minimum=0.0, maximum=1.0, value=0.5)
            temp = gr.Slider(label="Temperature", minimum=0.1, maximum=1.0, value=0.1)
        llm  = gr.Dropdown(value="gemini",choices=['gemini'])
        search_results = gr.Chatbot(height=1000)
        with gr.Row():
            query = gr.Textbox(lines=1,placeholder="Query ur question" ,container=True)
            search_button = gr.Button("Ask",scale=1)

            # Output area for search results

        # Search functionality
        chat_back = gr.Button("Back")
        chat_back.click(lambda : gr.Tabs(selected=0),None, tabs)
        
        search_button.click(
            chat_with_llm,
            inputs=[query,search_results, selected_file, top_k,top_p,temp,llm],
            outputs=search_results
        )
    return chat_model