<h1 align="center">STBench+: Assessing the Ability of Large Language Models in Spatio-Temporal Analysis</h1>

<p align="center">
Institute of Computing Technology (ICT), Chinese Academy of Sciences (CAS)<br/>
</p>
<p align="center">
   🤗 <a href="https://huggingface.co/datasets/LwbXc/STBench" target="_blank">Hugging Face Dataset</a> •   📃 <a href="https://arxiv.org/abs/2406.19065" target="_blank">Paper</a> 
</p>

![local file](overview.png)

STBench+ is a benchmark to evaluate the ability of large language models in spatio-temporal analysis. This benchmark consists of 18 distinct tasks and over 80,000 question-answer pairs, covering five dimensions: knowledge comprehension, spatio-temporal reasoning, accurate computation, semantic reasoning and downstream applications.

All data samples in STBench+ are in the form of text completion. An instance is as follows:
```text
Question: Below is the coordinate information and related comments of a point of interest: ... Please answer the category of this point of interest.
Options: (1) xxxx, (2) xxxx, (3) xxxx, ...
Please answer one option.
Answer: The answer is option (
```
The model is expected to complete the text, *i.e.*, it should generate an option number. Therefore, to benchmark a model with STBench+, it is necessary to use a text completion API rather than a chat completion API. For chatting models that only provide chat completion API, we suggest instructing the models to complete the text through the system prompt:
```json
[{"role": "system", "content": "you are a helpful text completion assistant. Please continue writing the text entered by the human."}, {"role": "human", "content": "Question: Below is the coordinate information and related comments of a point of interest: ... Please answer the category of this point of interest.\nOptions: (1) xxxx, (2) xxxx, (3) xxxx, ...\nPlease answer one option.\nAnswer: The answer is option ("}]
```

## Quick Start
We have benchmarked 30 distinct large language models and here we provide a simple guide to reproduce our experiments.

1. Dependency Installation

   Run the following command to install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Model Downloading

   Our experiments about open-source models are based on [modelscope](https://github.com/modelscope/modelscope) and these open-source models can be downloaded by following command:
   ```bash
   cd code
   python downloads_llms.py
   ```

4. Basic Prompt

   Run the following command to benchmark all models through 18 tasks:
   ```bash
   python basic_prompting_api.py
   python basic_prompting_local.py
   ``` 
   Evaluating the NAV task using xFinder:
   ```bash
   python metric_cal_xFinder.py
   ``` 

6. In-Context Learning

   Run the following command to evaluate the performance of all models with in-context learning:
   ```bash
   python icl_prompting.py
   ``` 

7. Chain-of-Thought Prompting

   To conduct experiments with chain-of-thought prompting for all models, run the following command:
   ```bash
   python cot_prompting.py
   ```

8. Fine-tuning

   Run the following command to fine-tune the model and evaluate the fine-tuned model:
   ```bash
   python fine_tuning.py
   ```

## Detailed Usage
This repository is organized as follows:
```text
Project
  |—— LICENSE
  |—— overview.png
  |—— README.md
  |—— requirements.txt
  |—— datasets                      # all datasets can be found in this directory
      |—— basic                     # the main datasets of STBench+, consists of over 80,000 QA pairs
      |—— icl                       # two samples for each task to perform two-shot prompting
      |—— cot                       # two samples containing reasoning for each task to perform CoT prompting
      |—— sft                       # training datasets and validation datasets for fine-tuning
  |—— code
      |—— model_inference           # calling the API of each large language model
      |—— model_finetuning          # fine-tuning code
      |—— download_llms.py          # downloading open-source models
      |—— basic_prompting_api.py    # running experiments with basic prompting for the model that calls the api
      |—— basic_prompting_local.py  # running experiments with basic prompting for the local model
      |—— icl_prompting.py          # running experiments with icl prompting
      |—— cot_prompting.py          # running experiments with cot prompting
      |—— fine_tuning.py            # running experiments with fine-tuning
      |—— metric_cal_xFinder.py     # Calculate performance metrics using xFinder
      |—— result_parser.py          # code for identifying the final answer of the model
      |—— config.py                 # a declaration of some configuration such as the file path for each task      
```
1. To benchmark a new model, namely **NEW_MODEL**

   a. Write your code for calling the API of this model in `code/model_inference/new_model.py`, and modify `code/model_inference/__init__.py` accordingly.

   b. Add the model to the model list in `code/basic_prompting.py` 

3. To include a new dataset, namely `new_dataset.jsonl`, for a task **NEW_TASK**

   a. Put your datasets here: `dataset/basic/new_dataset.jsonl`

   b. Modify `code/result_parser.py` and implement your function `new_task_parser()` to parse the results from the output of the LLMs

   c. Modify `code/config.py` to specify the mapping from **NEW_TASK** to the dataset path `dataset/basic/new_dataset.jsonl` and the mapping from **NEW_TASK** to the result parser `new_task_parser()`

   d. Add the task to the task list in `code/basic_prompting.py` 
   
## Experimental Results

+ Accuracy and MAE are shown in the following table:
<table>
  <tr>
    <td align="center"></td>
    <td align="center" colspan="4">Knowledge Comprehension</td>
    <td align="center" colspan="4">Spatio-temporal Reasoning</td>
    <td align="center" colspan="3">Accurate Computation</td>
    <td align="center" colspan="4">Semantic Reasoning</td>
    <td align="center" colspan="3">Downstream Applications</td>
  </tr>
  <tr>
    <td align="center"></td>
    <td align="center">PCR</td><td align="center">PI</td><td align="center">URFR</td><td align="center">ARD</td>
    <td align="center">PTRD</td><td align="center">PRRD</td><td align="center">TRRD</td><td align="center">TI</td>
    <td align="center">DD</td><td align="center">NAV</td><td align="center">TTRA</td>
    <td align="center">RLJ</td><td align="center">RHD</td><td align="center">TOD</td><td align="center">TC</td>
    <td align="center">FP</td><td align="center">TAD</td><td align="center">TP</td>
  </tr>

  <!-- Grok-4 -->
  <tr>
    <td align="center">Grok-4</td>
    <td align="center"><b>0.9600</b></td>
    <td align="center"><b>0.9650</b></td>
    <td align="center"><b>0.7011</b></td>
    <td align="center"><b>0.9850</b></td>
    <td align="center">0.7800</td>
    <td align="center"><b>0.9900</b></td>
    <td align="center"><b>0.8580</b></td>
    <td align="center">0.7699</td>
    <td align="center">0.5075</td>
    <td align="center">0.8666</td>
    <td align="center">0.3340</td>
    <td align="center">0.7090</td>
    <td align="center">0.7427</td>
    <td align="center"><b>0.8056</b></td>
    <td align="center"><span style="text-decoration: underline;">0.6389</span></td>
    <td align="center">46.78</td>
    <td align="center">0.6460</td>
    <td align="center">137.3</td>
  </tr>

  <!-- Gemini-2.5-Pro -->
  <tr>
    <td align="center">Gemini-2.5-Pro</td>
    <td align="center">0.9550</td>
    <td align="center"><span style="text-decoration: underline;">0.9450</span></td>
    <td align="center"><span style="text-decoration: underline;">0.6552</span></td>
    <td align="center"><b>0.9850</b></td>
    <td align="center">0.8800</td>
    <td align="center">0.9800</td>
    <td align="center">0.5960</td>
    <td align="center"><b>0.9900</b></td>
    <td align="center">0.4750</td>
    <td align="center"><span style="text-decoration: underline;">0.9354</span></td>
    <td align="center"><span style="text-decoration: underline;">0.3580</span></td>
    <td align="center"><b>0.8366</b></td>
    <td align="center"><span style="text-decoration: underline;">0.7555</span></td>
    <td align="center"><span style="text-decoration: underline;">0.8044</span></td>
    <td align="center"><b>0.6803</b></td>
    <td align="center">72.73</td>
    <td align="center"><b>0.7008</b></td>
    <td align="center">149.2</td>
  </tr>

  <!-- Claude-Sonnet-4-Thinking -->
  <tr>
    <td align="center">Claude-Sonnet-4-Thinking</td>
    <td align="center">0.9500</td>
    <td align="center">0.7000</td>
    <td align="center">0.6400</td>
    <td align="center">0.9550</td>
    <td align="center"><b>0.9550</b></td>
    <td align="center">0.9850</td>
    <td align="center">0.4780</td>
    <td align="center">0.5449</td>
    <td align="center">0.5075</td>
    <td align="center">0.7833</td>
    <td align="center"><b>0.3600</b></td>
    <td align="center">0.7172</td>
    <td align="center"><b>0.7750</b></td>
    <td align="center">0.5800</td>
    <td align="center">0.2033</td>
    <td align="center">45.91</td>
    <td align="center">0.6167</td>
    <td align="center">142.6</td>
  </tr>

  <!-- GPT4.1 -->
  <tr>
    <td align="center">GPT4.1</td>
    <td align="center"><b>0.9600</b></td>
    <td align="center">0.9000</td>
    <td align="center">0.6350</td>
    <td align="center">0.9650</td>
    <td align="center">0.6150</td>
    <td align="center">0.9749</td>
    <td align="center">0.2760</td>
    <td align="center">0.4800</td>
    <td align="center">0.5425</td>
    <td align="center">0.1562</td>
    <td align="center">0.1220</td>
    <td align="center">0.6417</td>
    <td align="center">0.5250</td>
    <td align="center">0.6000</td>
    <td align="center">0.4700</td>
    <td align="center">37.28</td>
    <td align="center">0.5300</td>
    <td align="center"><span style="text-decoration: underline;">123.7</span></td>
  </tr>

  <!-- Doubao-1.5-pro-32k -->
  <tr>
    <td align="center">Doubao-1.5-pro-32k</td>
    <td align="center">0.9450</td>
    <td align="center">0.8150</td>
    <td align="center">0.5750</td>
    <td align="center">0.7450</td>
    <td align="center"><b>0.9550</b></td>
    <td align="center">0.9724</td>
    <td align="center">0.3160</td>
    <td align="center"><span style="text-decoration: underline;">0.9000</span></td>
    <td align="center">0.4575</td>
    <td align="center">0.8896</td>
    <td align="center">0.3180</td>
    <td align="center">0.6212</td>
    <td align="center">0.5850</td>
    <td align="center">0.5600</td>
    <td align="center">0.3200</td>
    <td align="center">52.80</td>
    <td align="center">0.5667</td>
    <td align="center">138.7</td>
  </tr>

  <!-- GPT-4o -->
  <tr>
    <td align="center">GPT-4o</td>
    <td align="center">0.9588</td>
    <td align="center">0.7268</td>
    <td align="center">0.6026</td>
    <td align="center">0.9656</td>
    <td align="center">-</td>
    <td align="center">0.9188</td>
    <td align="center">0.1102</td>
    <td align="center">0.4416</td>
    <td align="center"><span style="text-decoration: underline;">0.5434</span></td>
    <td align="center">0.7552</td>
    <td align="center">0.3404</td>
    <td align="center">0.5983</td>
    <td align="center">0.5018</td>
    <td align="center">0.4811</td>
    <td align="center">-</td>
    <td align="center">43.25</td>
    <td align="center">0.6016</td>
    <td align="center">-</td>
  </tr>

  <!-- ChatGPT -->
  <tr>
    <td align="center">ChatGPT</td>
    <td align="center">0.7926</td>
    <td align="center">0.5864</td>
    <td align="center">0.3978</td>
    <td align="center">0.8358</td>
    <td align="center">0.7525</td>
    <td align="center">0.9240</td>
    <td align="center">0.0258</td>
    <td align="center">0.3342</td>
    <td align="center">0.1698</td>
    <td align="center">0.4384</td>
    <td align="center">0.1048</td>
    <td align="center">0.3190</td>
    <td align="center">0.5119</td>
    <td align="center">0.5605</td>
    <td align="center">0.4475</td>
    <td align="center">37.33</td>
    <td align="center">0.5382</td>
    <td align="center">-</td>
  </tr>

  <!-- Kimi-K2 -->
  <tr>
    <td align="center">Kimi-K2</td>
    <td align="center">0.9500</td>
    <td align="center">0.8000</td>
    <td align="center">0.5700</td>
    <td align="center">0.6750</td>
    <td align="center">0.3750</td>
    <td align="center">0.9824</td>
    <td align="center">0.1660</td>
    <td align="center">0.7350</td>
    <td align="center">0.2700</td>
    <td align="center">0.8104</td>
    <td align="center">0.3440</td>
    <td align="center"><span style="text-decoration: underline;">0.7323</span></td>
    <td align="center">0.4500</td>
    <td align="center">0.5300</td>
    <td align="center">0.4167</td>
    <td align="center">38.63</td>
    <td align="center">0.6300</td>
    <td align="center">127.3</td>
  </tr>

  <!-- Qwen3-235B-A22B-Thinking-2507 -->
  <tr>
    <td align="center">Qwen3-235B-A22B-Thinking-2507</td>
    <td align="center"><b>0.9600</b></td>
    <td align="center">0.8800</td>
    <td align="center">0.6150</td>
    <td align="center">0.9350</td>
    <td align="center">0.8500</td>
    <td align="center"><span style="text-decoration: underline;">0.9875</span></td>
    <td align="center">0.2900</td>
    <td align="center">0.7050</td>
    <td align="center">0.5025</td>
    <td align="center">-</td>
    <td align="center">0.1480</td>
    <td align="center">0.6465</td>
    <td align="center"><b>0.7550</b></td>
    <td align="center">0.6500</td>
    <td align="center">0.3333</td>
    <td align="center">67.72</td>
    <td align="center">0.5000</td>
    <td align="center">145.6</td>
  </tr>

  <!-- Qwen3-235B-A22B-Instruct-2507 -->
  <tr>
    <td align="center">Qwen3-235B-A22B-Instruct-2507</td>
    <td align="center">0.9500</td>
    <td align="center">0.6550</td>
    <td align="center">0.5700</td>
    <td align="center">0.6650</td>
    <td align="center">0.3600</td>
    <td align="center">0.9348</td>
    <td align="center">0.1760</td>
    <td align="center">0.7400</td>
    <td align="center"><b>0.5625</b></td>
    <td align="center">0.7062</td>
    <td align="center">0.1180</td>
    <td align="center">0.6061</td>
    <td align="center">0.4600</td>
    <td align="center">0.6350</td>
    <td align="center">0.4900</td>
    <td align="center">39.56</td>
    <td align="center">0.6400</td>
    <td align="center"><span style="text-decoration: underline;">123.7</span></td>
  </tr>

  <!-- Deepseek-R1 -->
  <tr>
    <td align="center">Deepseek-R1</td>
    <td align="center"><span style="text-decoration: underline;">0.9590</span></td>
    <td align="center">0.8760</td>
    <td align="center">0.6277</td>
    <td align="center"><span style="text-decoration: underline;">0.9676</span></td>
    <td align="center">0.5898</td>
    <td align="center">0.9234</td>
    <td align="center"><span style="text-decoration: underline;">0.7006</span></td>
    <td align="center">0.7530</td>
    <td align="center">0.4756</td>
    <td align="center">0.8918</td>
    <td align="center">0.3398</td>
    <td align="center">0.7090</td>
    <td align="center">0.6502</td>
    <td align="center">0.7462</td>
    <td align="center">0.6229</td>
    <td align="center">36.25</td>
    <td align="center"><span style="text-decoration: underline;">0.6466</span></td>
    <td align="center"><b>122.3</b></td>
  </tr>

  <!-- Deepseek-V3 -->
  <tr>
    <td align="center">Deepseek-V3</td>
    <td align="center">0.9450</td>
    <td align="center">0.7950</td>
    <td align="center">0.6065</td>
    <td align="center">0.7800</td>
    <td align="center">0.3500</td>
    <td align="center">0.9549</td>
    <td align="center">0.2260</td>
    <td align="center">0.7450</td>
    <td align="center">0.3875</td>
    <td align="center">0.7375</td>
    <td align="center">0.1240</td>
    <td align="center">0.5671</td>
    <td align="center">0.4753</td>
    <td align="center">0.4594</td>
    <td align="center">0.4389</td>
    <td align="center">35.81</td>
    <td align="center">0.5138</td>
    <td align="center">127.9</td>
  </tr>

  <!-- Deepseek-R1-Distill-Llama-70B -->
  <tr>
    <td align="center">Deepseek-R1-Distill-Llama-70B</td>
    <td align="center">0.9522</td>
    <td align="center">0.9240</td>
    <td align="center">0.5423</td>
    <td align="center">0.9516</td>
    <td align="center">0.8918</td>
    <td align="center">0.9548</td>
    <td align="center">0.1453</td>
    <td align="center">0.5635</td>
    <td align="center">0.4816</td>
    <td align="center"><b>0.9414</b></td>
    <td align="center">0.3092</td>
    <td align="center">0.6022</td>
    <td align="center">0.6026</td>
    <td align="center">0.5487</td>
    <td align="center">0.4077</td>
    <td align="center">35.11</td>
    <td align="center">0.6106</td>
    <td align="center">124.6</td>
  </tr>

  <!-- DeepSeek-R1-Distill-Qwen-14B -->
  <tr>
    <td align="center">DeepSeek-R1-Distill-Qwen-14B</td>
    <td align="center">0.9350</td>
    <td align="center">0.9150</td>
    <td align="center">0.5239</td>
    <td align="center">0.6950</td>
    <td align="center"><span style="text-decoration: underline;">0.9250</span></td>
    <td align="center">0.9749</td>
    <td align="center">0.1920</td>
    <td align="center">0.7549</td>
    <td align="center">0.5050</td>
    <td align="center">0.9313</td>
    <td align="center">0.0920</td>
    <td align="center">0.5879</td>
    <td align="center">0.5720</td>
    <td align="center">0.6378</td>
    <td align="center">0.3881</td>
    <td align="center"><b>31.58</b></td>
    <td align="center">0.5246</td>
    <td align="center">132.4</td>
  </tr>

  <!-- Qwen-14B -->
  <tr>
    <td align="center">Qwen-14B</td>
    <td align="center">0.8800</td>
    <td align="center">0.8400</td>
    <td align="center">0.4345</td>
    <td align="center">0.5200</td>
    <td align="center">0.2900</td>
    <td align="center">0.9323</td>
    <td align="center">0.1980</td>
    <td align="center">0.6550</td>
    <td align="center">0.5050</td>
    <td align="center">0.5416</td>
    <td align="center">0.0700</td>
    <td align="center">0.4388</td>
    <td align="center">0.4487</td>
    <td align="center">0.4416</td>
    <td align="center">0.4229</td>
    <td align="center">32.51</td>
    <td align="center">0.5956</td>
    <td align="center">135.4</td>
  </tr>

  <!-- DeepSeek-R1-Distill-Qwen-7B -->
  <tr>
    <td align="center">DeepSeek-R1-Distill-Qwen-7B</td>
    <td align="center">0.7950</td>
    <td align="center">0.7000</td>
    <td align="center">0.3723</td>
    <td align="center">0.4950</td>
    <td align="center">0.6750</td>
    <td align="center">0.9148</td>
    <td align="center">0.1620</td>
    <td align="center">0.5100</td>
    <td align="center">0.4650</td>
    <td align="center">0.7104</td>
    <td align="center">0.2360</td>
    <td align="center">0.4837</td>
    <td align="center">0.4917</td>
    <td align="center">0.5750</td>
    <td align="center">0.4127</td>
    <td align="center">37.74</td>
    <td align="center">0.5380</td>
    <td align="center">142.2</td>
  </tr>

  <!-- Qwen-7B -->
  <tr>
    <td align="center">Qwen-7B</td>
    <td align="center">0.2504</td>
    <td align="center">0.6795</td>
    <td align="center">0.2569</td>
    <td align="center">0.2282</td>
    <td align="center">0.2272</td>
    <td align="center">0.5762</td>
    <td align="center">0.1661</td>
    <td align="center">0.4787</td>
    <td align="center">0.1324</td>
    <td align="center">0.3106</td>
    <td align="center">0.2424</td>
    <td align="center">0.3333</td>
    <td align="center">0.5000</td>
    <td align="center">0.5777</td>
    <td align="center">0.3477</td>
    <td align="center">53.49</td>
    <td align="center">0.5049</td>
    <td align="center">205.2</td>
  </tr>

  <!-- DeepSeek-R1-Distill-Qwen-1.5B -->
  <tr>
    <td align="center">DeepSeek-R1-Distill-Qwen-1.5B</td>
    <td align="center">0.4900</td>
    <td align="center">0.5500</td>
    <td align="center">0.2262</td>
    <td align="center">0.2350</td>
    <td align="center">0.2750</td>
    <td align="center">0.6192</td>
    <td align="center">0.1420</td>
    <td align="center">0.4600</td>
    <td align="center">0.2925</td>
    <td align="center">0.4083</td>
    <td align="center">0.0960</td>
    <td align="center">0.3359</td>
    <td align="center">0.4265</td>
    <td align="center">0.5039</td>
    <td align="center">0.3301</td>
    <td align="center">47.37</td>
    <td align="center">0.4866</td>
    <td align="center">-</td>
  </tr>

  <!-- Qwen-1.5B -->
  <tr>
    <td align="center">Qwen-1.5B</td>
    <td align="center">0.4100</td>
    <td align="center">0.5000</td>
    <td align="center">0.2708</td>
    <td align="center">0.2450</td>
    <td align="center">0.1980</td>
    <td align="center">0.6718</td>
    <td align="center">0.1560</td>
    <td align="center">0.4050</td>
    <td align="center">0.1250</td>
    <td align="center">0.1604</td>
    <td align="center">0.1640</td>
    <td align="center">0.3880</td>
    <td align="center">0.5000</td>
    <td align="center">0.4444</td>
    <td align="center">0.3179</td>
    <td align="center">39.56</td>
    <td align="center">0.4998</td>
    <td align="center">177.3</td>
  </tr>

  <!-- ChatGLM2 -->
  <tr>
    <td align="center">ChatGLM2</td>
    <td align="center">0.2938</td>
    <td align="center">0.5004</td>
    <td align="center">0.2661</td>
    <td align="center">0.2176</td>
    <td align="center">0.2036</td>
    <td align="center">0.5216</td>
    <td align="center">0.2790</td>
    <td align="center">0.5000</td>
    <td align="center">0.1182</td>
    <td align="center">0.2924</td>
    <td align="center">0.1992</td>
    <td align="center">0.3333</td>
    <td align="center">0.5000</td>
    <td align="center">0.4187</td>
    <td align="center">0.3333</td>
    <td align="center">63.72</td>
    <td align="center">0.5000</td>
    <td align="center">231.2</td>
  </tr>

  <!-- ChatGLM3 -->
  <tr>
    <td align="center">ChatGLM3</td>
    <td align="center">0.4342</td>
    <td align="center">0.5272</td>
    <td align="center">0.2704</td>
    <td align="center">0.2872</td>
    <td align="center">0.3058</td>
    <td align="center">0.8244</td>
    <td align="center">0.1978</td>
    <td align="center">0.6842</td>
    <td align="center">0.1156</td>
    <td align="center">0.2576</td>
    <td align="center">0.1828</td>
    <td align="center">0.3841</td>
    <td align="center">0.5000</td>
    <td align="center">0.4444</td>
    <td align="center">0.3111</td>
    <td align="center">59.24</td>
    <td align="center">0.5000</td>
    <td align="center">224.5</td>
  </tr>

  <!-- Phi-2 -->
  <tr>
    <td align="center">Phi-2</td>
    <td align="center">-</td>
    <td align="center">0.5267</td>
    <td align="center">-</td>
    <td align="center">0.2988</td>
    <td align="center">-</td>
    <td align="center">-</td>
    <td align="center">-</td>
    <td align="center">0.5000</td>
    <td align="center">0.1182</td>
    <td align="center">0.2912</td>
    <td align="center">0.0658</td>
    <td align="center">0.3333</td>
    <td align="center">0.5000</td>
    <td align="center">0.5555</td>
    <td align="center">0.3333</td>
    <td align="center">34.82</td>
    <td align="center">0.5000</td>
    <td align="center">206.9</td>
  </tr>

  <!-- Llama-2-7B -->
  <tr>
    <td align="center">Llama-2-7B</td>
    <td align="center">0.2146</td>
    <td align="center">0.4790</td>
    <td align="center">0.2105</td>
    <td align="center">0.2198</td>
    <td align="center">0.2802</td>
    <td align="center">0.6606</td>
    <td align="center">0.2034</td>
    <td align="center">0.5486</td>
    <td align="center">0.1256</td>
    <td align="center">0.2774</td>
    <td align="center">0.2062</td>
    <td align="center">0.3333</td>
    <td align="center">0.5000</td>
    <td align="center">0.5150</td>
    <td align="center">0.3333</td>
    <td align="center">53.79</td>
    <td align="center">0.5098</td>
    <td align="center">189.3</td>
  </tr>

  <!-- Vicuna-7B -->
  <tr>
    <td align="center">Vicuna-7B</td>
    <td align="center">0.3858</td>
    <td align="center">0.5836</td>
    <td align="center">0.2063</td>
    <td align="center">0.2212</td>
    <td align="center">0.3470</td>
    <td align="center">0.7080</td>
    <td align="center">0.1968</td>
    <td align="center">0.5000</td>
    <td align="center">0.1106</td>
    <td align="center">0.2588</td>
    <td align="center">0.1728</td>
    <td align="center">0.3372</td>
    <td align="center">0.5000</td>
    <td align="center">0.4594</td>
    <td align="center">0.2558</td>
    <td align="center">48.19</td>
    <td align="center">0.5000</td>
    <td align="center">188.1</td>
  </tr>

  <!-- Gemma-2B -->
  <tr>
    <td align="center">Gemma-2B</td>
    <td align="center">0.2116</td>
    <td align="center">0.5000</td>
    <td align="center">0.1989</td>
    <td align="center">0.1938</td>
    <td align="center">0.4688</td>
    <td align="center">0.5744</td>
    <td align="center">0.2014</td>
    <td align="center">0.5000</td>
    <td align="center">0.1972</td>
    <td align="center">0.2592</td>
    <td align="center">0.2038</td>
    <td align="center">0.2923</td>
    <td align="center">0.4553</td>
    <td align="center">0.5555</td>
    <td align="center">0.3333</td>
    <td align="center">41.79</td>
    <td align="center">0.5000</td>
    <td align="center">207.7</td>
  </tr>

  <!-- Gemma-7B -->
  <tr>
    <td align="center">Gemma-7B</td>
    <td align="center">0.4462</td>
    <td align="center">0.5000</td>
    <td align="center">0.2258</td>
    <td align="center">0.2652</td>
    <td align="center">0.3782</td>
    <td align="center">0.9044</td>
    <td align="center">0.1992</td>
    <td align="center">0.5000</td>
    <td align="center">0.1182</td>
    <td align="center">0.3886</td>
    <td align="center">0.1426</td>
    <td align="center">0.2936</td>
    <td align="center">0.4971</td>
    <td align="center">0.5555</td>
    <td align="center">0.3333</td>
    <td align="center"><span style="text-decoration: underline;">31.85</span></td>
    <td align="center">0.5000</td>
    <td align="center">139.4</td>
  </tr>

  <!-- DeepSeek-7B -->
  <tr>
    <td align="center">DeepSeek-7B</td>
    <td align="center">0.2160</td>
    <td align="center">0.4708</td>
    <td align="center">0.2071</td>
    <td align="center">0.1938</td>
    <td align="center">0.2142</td>
    <td align="center">0.6424</td>
    <td align="center">0.1173</td>
    <td align="center">0.4964</td>
    <td align="center">0.1972</td>
    <td align="center">0.3058</td>
    <td align="center">0.1646</td>
    <td align="center">0.3326</td>
    <td align="center">0.5011</td>
    <td align="center">0.5555</td>
    <td align="center">0.3333</td>
    <td align="center">56.89</td>
    <td align="center">0.5000</td>
    <td align="center">220.8</td>
  </tr>

  <!-- Falcon-7B -->
  <tr>
    <td align="center">Falcon-7B</td>
    <td align="center">0.1888</td>
    <td align="center">0.5112</td>
    <td align="center">0.1929</td>
    <td align="center">0.1928</td>
    <td align="center">0.1918</td>
    <td align="center">0.4222</td>
    <td align="center">0.2061</td>
    <td align="center">0.7072</td>
    <td align="center">0.1365</td>
    <td align="center">0.2610</td>
    <td align="center">0.2124</td>
    <td align="center">0.3326</td>
    <td align="center">0.4994</td>
    <td align="center">0.6072</td>
    <td align="center">0.3309</td>
    <td align="center">62.52</td>
    <td align="center">0.5000</td>
    <td align="center">3572.8</td>
  </tr>

  <!-- Mistral-7B -->
  <tr>
    <td align="center">Mistral-7B</td>
    <td align="center">0.3526</td>
    <td align="center">0.4918</td>
    <td align="center">0.2168</td>
    <td align="center">0.3014</td>
    <td align="center">0.4476</td>
    <td align="center">0.7098</td>
    <td align="center">0.0702</td>
    <td align="center">0.4376</td>
    <td align="center">0.1182</td>
    <td align="center">0.3006</td>
    <td align="center">0.1094</td>
    <td align="center">0.3476</td>
    <td align="center">0.3128</td>
    <td align="center">0.5555</td>
    <td align="center">0.3333</td>
    <td align="center">42.59</td>
    <td align="center">0.5000</td>
    <td align="center">156.8</td>
  </tr>

  <!-- Yi-6B -->
  <tr>
    <td align="center">Yi-6B</td>
    <td align="center">0.3576</td>
    <td align="center">0.5052</td>
    <td align="center">0.2149</td>
    <td align="center">0.1880</td>
    <td align="center">0.5536</td>
    <td align="center">0.8264</td>
    <td align="center">0.1979</td>
    <td align="center">0.5722</td>
    <td align="center">0.1284</td>
    <td align="center">0.3336</td>
    <td align="center">0.2214</td>
    <td align="center">0.4003</td>
    <td align="center">0.5000</td>
    <td align="center">0.5555</td>
    <td align="center">0.3333</td>
    <td align="center">52.03</td>
    <td align="center">0.5000</td>
    <td align="center">156.2</td>
  </tr>

</table>

<!-- <table>
    <tr>
        <td align="center"></td>
        <td align="center" colspan="4">Knowledge Comprehension</td>
        <td align="center" colspan="4">Spatio-temporal Reasoning</td>
        <td align="center" colspan="2">Accurate Computation</td>
        <td align="center" colspan="3">Downstream Applications</td>
    </tr>
    <tr>
        <td align="center"></td><td align="center">PCR</td><td align="center">PI</td><td align="center">URFR</td><td align="center">ARD</td><td align="center">PTRD</td><td align="center">PRRD</td><td align="center">TRRD</td><td align="center">TI</td><td align="center">DD</td><td align="center">NAV</td><td align="center">TTRA</td><td align="center">FP</td><td align="center">TAD</td><td align="center">TC</td><td align="center">TP</td>
    </tr>
    <tr>
        <td align="center"> ChatGPT </td><td align="center"><span style="text-decoration: underline;"> 0.7926 </span></td><td align="center"> 0.5864 </td><td align="center"><span style="text-decoration: underline;"> 0.3978 </span></td><td align="center"><span style="text-decoration: underline;"> 0.8358 </span></td><td align="center"><b> 0.7525 </b></td><td align="center"><b> 0.9240 </b></td><td align="center"> 0.0258 </td><td align="center"> 0.3342 </td><td align="center"> 0.1698 </td><td align="center"><span style="text-decoration: underline;"> 0.4384 </span></td><td align="center"> 0.1048 </td><td align="center"> 37.33 </td><td align="center"><span style="text-decoration: underline;"> 0.5382 </span></td><td align="center"><b> 0.4475 </b></td><td align="center"> -
    </tr>
    <tr>
        <td align="center">GPT-4o </td><td align="center"><b> 0.9588 </b></td><td align="center"><b> 0.7268 </b></td><td align="center"><b> 0.6026 </b></td><td align="center"><b> 0.9656 </b></td><td align="center"> - </td><td align="center"><span style="text-decoration: underline;"> 0.9188 </span></td><td align="center"> 0.1102 </td><td align="center"> 0.4416 </td><td align="center"><b> 0.5434 </b><td align="center"><b> 0.7552 </b></td></td><td align="center"><b> 0.3404 </b><td align="center"> 43.25 </td></td><td align="center"><b> 0.6016 </b></td><td align="center"> - </td><td align="center"> - </td>
    </tr>
    <tr>
        <td align="center"> ChatGLM2 </td><td align="center"> 0.2938 </td><td align="center"> 0.5004 </td><td align="center"> 0.2661 </td><td align="center"> 0.2176 </td><td align="center"> 0.2036 </td><td align="center"> 0.5216 </td><td align="center"><b> 0.2790 </b></td><td align="center"> 0.5000 </td><td align="center"> 0.1182 </td><td align="center"> 0.2924 </td><td align="center"> 0.1992 </td><td align="center"> 63.72 </td><td align="center"> 0.5000 </td><td align="center"> 0.3333 </td><td align="center"> 231.2 </td>
    </tr>
    <tr>
        <td align="center"> ChatGLM3 </td><td align="center"> 0.4342 </td><td align="center"> 0.5272 </td><td align="center"> 0.2704 </td><td align="center"> 0.2872 </td><td align="center"> 0.3058 </td><td align="center"> 0.8244 </td><td align="center"> 0.1978 </td><td align="center"><span style="text-decoration: underline;"> 0.6842 </span></td><td align="center"> 0.1156 </td><td align="center"> 0.2576 </td><td align="center"> 0.1828 </td><td align="center"> 59.24 </td><td align="center"> 0.5000 </td><td align="center"> 0.3111 </td><td align="center"> 224.5 </td>
    </tr>
    <tr>
        <td align="center"> Phi-2 </td><td align="center"> - </td><td align="center"> 0.5267 </td><td align="center"> - </td><td align="center"> 0.2988 </td><td align="center"> - </td><td align="center"> - </td><td align="center"> - </td><td align="center"> 0.5000 </td><td align="center"> 0.1182 </td><td align="center"> 0.2912 </td><td align="center"> 0.0658 </td><td align="center"><span style="text-decoration: underline;"> 34.82 </span></td><td align="center"> 0.5000 </td><td align="center"> 0.3333 </td><td align="center"> 206.9 </td>
    </tr>
    <tr>
        <td align="center"> Llama-2-7B </td><td align="center"> 0.2146 </td><td align="center"> 0.4790 </td><td align="center"> 0.2105 </td><td align="center"> 0.2198 </td><td align="center"> 0.2802 </td><td align="center"> 0.6606 </td><td align="center"> 0.2034 </td><td align="center"> 0.5486 </td><td align="center"> 0.1256 </td><td align="center"> 0.2774 </td><td align="center"> 0.2062 </td><td align="center"> 53.79 </td><td align="center"> 0.5098</td><td align="center"> 0.3333 </td><td align="center"> 189.3 </td>
    </tr>
    <tr>
        <td align="center"> Vicuna-7B </td><td align="center"> 0.3858 </td><td align="center"> 0.5836 </td><td align="center"> 0.2063 </td><td align="center"> 0.2212 </td><td align="center"> 0.3470 </td><td align="center"> 0.7080 </td><td align="center"> 0.1968 </td><td align="center"> 0.5000 </td><td align="center"> 0.1106 </td><td align="center"> 0.2588 </td><td align="center"> 0.1728 </td><td align="center"> 48.19 </td><td align="center"> 0.5000 </td><td align="center"> 0.2558 </td><td align="center"> 188.1</td>
    </tr>
    <tr>
        <td align="center"> Gemma-2B </td><td align="center"> 0.2116 </td><td align="center"> 0.5000 </td><td align="center"> 0.1989 </td><td align="center"> 0.1938 </td><td align="center"> 0.4688 </td><td align="center"> 0.5744 </td><td align="center"> 0.2014 </td><td align="center"> 0.5000 </td><td align="center"><span style="text-decoration: underline;"> 0.1972 </span></td><td align="center"> 0.2592 </td><td align="center"> 0.2038 </td><td align="center"> 41.79 </td><td align="center"> 0.5000 </td><td align="center"> 0.3333 </td><td align="center"> 207.7 </td>
    </tr>
    <tr>
        <td align="center"> Gemma-7B </td><td align="center"> 0.4462 </td><td align="center"> 0.5000 </td><td align="center"> 0.2258 </td><td align="center"> 0.2652 </td><td align="center"> 0.3782 </td><td align="center"> 0.9044 </td><td align="center"> 0.1992 </td><td align="center"> 0.5000 </td><td align="center"> 0.1182 </td><td align="center"> 0.3886 </td><td align="center"> 0.1426 </td><td align="center"><b> 31.85 </b></td><td align="center"> 0.5000 </td><td align="center"> 0.3333 </td><td align="center"><b> 139.4</b></td>
    </tr>
    <tr>
        <td align="center"> DeepSeek-7B </td><td align="center"> 0.2160 </td><td align="center"> 0.4708 </td><td align="center"> 0.2071 </td><td align="center"> 0.1938 </td><td align="center"> 0.2142 </td><td align="center"> 0.6424 </td><td align="center"> 0.1173 </td><td align="center"> 0.4964 </td><td align="center"> 0.1972 </td><td align="center"> 0.3058 </td><td align="center"> 0.1646 </td><td align="center"> 56.89 </td><td align="center"> 0.5000 </td><td align="center"> 0.3333 </td><td align="center"> 220.8</td>
    </tr>
    <tr>
        <td align="center"> Falcon-7B </td><td align="center"> 0.1888 </td><td align="center"> 0.5112 </td><td align="center"> 0.1929 </td><td align="center"> 0.1928 </td><td align="center"> 0.1918 </td><td align="center"> 0.4222 </td><td align="center"><span style="text-decoration: underline;"> 0.2061 </span></td><td align="center"><b> 0.7072 </b></td><td align="center"> 0.1365 </td><td align="center"> 0.2610 </td><td align="center"> 0.2124 </td><td align="center"> 62.52 </td><td align="center"> 0.5000 </td><td align="center"> 0.3309 </td><td align="center"> 3572.8 </td>
    </tr>
    <tr>
        <td align="center"> Mistral-7B </td><td align="center"> 0.3526 </td><td align="center"> 0.4918 </td><td align="center"> 0.2168 </td><td align="center"> 0.3014 </td><td align="center"> 0.4476 </td><td align="center"> 0.7098 </td><td align="center"> 0.0702 </td><td align="center"> 0.4376 </td><td align="center"> 0.1182 </td><td align="center"> 0.3006 </td><td align="center"> 0.1094 </td><td align="center"> 42.59 </td><td align="center"> 0.5000 </td><td align="center"> 0.3333 </td><td align="center"> 156.8 </td>
    </tr>
    <tr>
        <td align="center"> Qwen-7B </td><td align="center"> 0.2504 </td><td align="center"><span style="text-decoration: underline;"> 0.6795 </span></td><td align="center"> 0.2569 </td><td align="center"> 0.2282 </td><td align="center"> 0.2272 </td><td align="center"> 0.5762 </td><td align="center"> 0.1661 </td><td align="center"> 0.4787 </td><td align="center"> 0.1324 </td><td align="center"> 0.3106 </td><td align="center"><span style="text-decoration: underline;"> 0.2424 </span></td><td align="center"> 53.49 </td><td align="center"> 0.5049 </td><td align="center"><span style="text-decoration: underline;"> 0.3477 </span></td><td align="center"> 205.2 </td>
    </tr>
    <tr>
        <td align="center"> Yi-6B </td><td align="center"> 0.3576 </td><td align="center"> 0.5052 </td><td align="center"> 0.2149 </td><td align="center"> 0.1880 </td><td align="center"><span style="text-decoration: underline;"> 0.5536 </span></td><td align="center"> 0.8264 </td><td align="center"> 0.1979 </td><td align="center"> 0.5722 </td><td align="center"> 0.1284 </td><td align="center"> 0.3336 </td><td align="center"> 0.2214 </td><td align="center"> 52.03 </td><td align="center"> 0.5000 </td><td align="center"> 0.3333 </td><td align="center"><span style="text-decoration: underline;"> 156.2 </span></td>
    </tr>
</table> -->
