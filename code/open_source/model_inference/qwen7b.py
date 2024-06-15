from modelscope import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch
import pdb

class qwen7b(object):

    def __init__(self, model_path='~/.cache/modelscope/hub/qwen/Qwen-7B', torch_dtype=torch.float32, device='cuda'):
        print("Loading model from", model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch_dtype, device_map=device, trust_remote_code=True)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model.generation_config = GenerationConfig.from_pretrained(model_path, trust_remote_code=True)
        self.model_path = model_path

    def generate(self, input_text, max_new_tokens=100):
        inputs = self.tokenizer(input_text, return_tensors="pt").input_ids.to(self.model.device)
        outputs = self.model.generate(inputs, max_length=len(inputs[0])+max_new_tokens, max_new_tokens=None)
        return self.tokenizer.batch_decode(outputs)[0][len(input_text):]

if __name__=='__main__':
    model = qwen7b()
    print(model.generate("Yesterday was Thursday, today is Friday, so tomorrow is ", 10))
    print(model.generate("Yesterday was 2022-01-01, today is 2022-01-02, so tomorrow is ", 10))