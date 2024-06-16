from modelscope import snapshot_download

snapshot_download('AI-ModelScope/gemma-7b', ignore_file_pattern = [r'\w+\.gguf'])
snapshot_download('AI-ModelScope/gemma-2b', ignore_file_pattern = [r'\w+\.gguf'])
snapshot_download('deepseek-ai/deepseek-llm-7b-base')
snapshot_download('AI-ModelScope/falcon-7b')
snapshot_download('AI-ModelScope/Mistral-7B-v0.1')
snapshot_download('qwen/Qwen-7B')
snapshot_download('01ai/Yi-6B')
snapshot_download('ZhipuAI/chatglm2-6b')
snapshot_download('ZhipuAI/chatglm3-6b')
snapshot_download('AI-ModelScope/phi-2')
snapshot_download('modelscope/Llama-2-7b-ms', ignore_file_pattern = [r'\w+\.bin'])
snapshot_download('AI-ModelScope/vicuna-7b-v1.5')