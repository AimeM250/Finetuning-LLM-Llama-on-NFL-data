import gradio as gr
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

def generate_answer(user_prompt):
    instruction_set = """
    <s>[INST] <<SYS>>
    You are a highly knowledgeable NFL expert, Provide concise, accurate, and direct answers to NFL-records related queries. Ensure your responses are factual, free from biases, and strictly professional.
    If a query is unclear or lacks factual basis, clarify or request more information rather than providing incorrect or misleading answers. Avoid any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content in your responses.
    <</SYS>>
    """
    
    combined_prompt = f"{instruction_set}{user_prompt} [/INST]"
    
    # Initialize the text generation pipeline without token limit
    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=1000)
    result = pipe(combined_prompt)
    
    # Extract the generated answer
    generated_answer = result[0]['generated_text'].split("[/INST]", 1)[1].strip()
    
    return generated_answer

iface = gr.Interface(
    fn=generate_answer,
    inputs=gr.Textbox(lines=5, placeholder="Enter Your Query Here..."),
    outputs=gr.Text(label="Generated Answer"),
    title="NFL Expertise Generator",
    description="This model provides concise, accurate, and direct answers to NFL-related queries."
)
iface.launch()
