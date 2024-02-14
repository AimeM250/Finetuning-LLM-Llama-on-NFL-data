- **`Project` :** LLM - NFL (Finetuning Llama-2-7b-chat with Official 2023
National Football League Record
& FactBook) 
- **`NFL Book`:** [Download](https://operations.nfl.com/media/nppjkdp1/2023-record-and-fact-book.pdf)
- **`Model Link to HuggingFace`:** [Check](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
<br/>

# Key Objectives
1. Fine-tune Llama-2-7b-chat model on NFL facts and records document.
2. Develop an interactive interface to showcase the model's capabilities after finetuning.

# Data Engineering Process
![Llama-2-7b-chat Model by meta](data\Llama2.JPG)

- **PDF to Text Conversion:** Utilize `process_data.py` to convert PDF files containing the NFL Factbook into raw text format.
- **Text Preprocessing:** Clean the raw text, removing unnecessary characters like newline characters, and format it appropriately for training.

# Training the Model
The model is trained using the provided training script on the processed data. The training script fine-tunes the Llama-2-7b-chat model on the NFL Factbook data.

# Demo
The trained model can be interactively tested using a small interface created with Gradio. Users can input queries related to NFL facts and records, and the model will generate relevant responses.

![Gradio Demo](data\gradio.demo.JPG)

# Usage
To reproduce the training process and testing using the Gradio demo, follow the below steps:

1. Install the necessary dependencies by running:
    ```
    pip install -r requirements.txt
    ```
2. Run `process_data.py` to convert the PDF files to text and preprocess the data.

3. Execute the `train.py` script to fine-tune the Llama-2-7b-chat model on the prepared dataset.

4. Launch the Gradio demo interface using the `test.py` script.

# Acknowledgments
- The Llama-2-7b-chat model has been developed and open sourced by Meta.
- The NFL Factbook dataset is sourced from [NFL operations Website](https://operations.nfl.com/media/nppjkdp1/2023-record-and-fact-book.pdf).

