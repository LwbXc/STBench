# STBench: Assessing the Ability of Large Language Models in Spatio-Temporal Analysis

![local file](overview.png)

STbench is a benchmark to evaluate the ability of large language models in spatio-temporal analysis. This benchmark consists of 13 distinct tasks and over 60,000 question-answer pairs, covering four dimensions: knowledge comprehension, spatio-temporal reasoning, accurate computation and downstream applications.

All data samples in STbench are in the form of text completion. An instance is as follows:
```text
Question: Below is the coordinate information and related comments of a point of interest: $\cdots$. Please answer the category of this point of interest.
Options: (1) xxxx, (2) xxxx, (3) xxxx, $\cdots$.
Please answer one option.
Answer: The answer is option (
```
The model is expected to complete the text, *i.e.*, it should generate an option number. Therefore, to benchmark a model with STBench, it is necessary to use a text completion API rather than a chat completion API. For chatting models that only provide chat completion API, we suggest instructing the models to complete the text through the system prompt:
```json
[{"role": "system", "content": "you are a helpful text completion assistant. Please continue writing the text entered by the human."}, {"role": "human", "content": "Question: Below is the coordinate information and related comments of a point of interest: ... Please answer the category of this point of interest.\nOptions: (1) xxxx, (2) xxxx, (3) xxxx, ...\nPlease answer one option.\nAnswer: The answer is option ("}]
```

## Quick Start
We have benchmarked 13 distinct large language models and here we provide a simple guide to reproduce our experiments.

1. Dependency Installation
 Run the following command to install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Model Downloading
Our experiments about open-source models are based on [modelscope](https://github.com/modelscope/modelscope) and the models can be downloaded by following command:
    ```bash
    cd code/open_source
    python downloads_llms.py
    ```
3. Basic Prompt
Run the following command to benchmark all 12 open-source models through 13 tasks:
    ```bash
    python basic_prompting.py
    ``` 

4. In-Context Learning
Run the following command to evaluate the performance of open-source models with in-context learning:
    ```bash
    python icl_prompting.py
    ``` 

5. Chain-of-Thought Prompting
To conduct experiments with chain-of-thought prompting for open-source models, run the following command:
    ```bash
    python cot_prompting.py
    ```

6. Fine-tuning
Run the following command to fine-tune the model and evaluate the fine-tuned model:
    ```bash
    python fine_tuning.py
    ```