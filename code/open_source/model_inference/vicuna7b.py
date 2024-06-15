from modelscope import AutoModelForCausalLM, AutoTokenizer
import torch
import pdb
from fastchat.model import load_model, add_model_args

class vicuna7b(object):

    def __init__(self, model_path='~/.cache/modelscope/hub/AI-ModelScope/vicuna-7b-v1___5', torch_dtype=torch.float32, device='cuda'):
        print("Loading model from", model_path)
        self.model, self.tokenizer = load_model(model_path, device=device, load_8bit=False, dtype=torch_dtype)
        self.model_path = model_path
    
    def generate(self, input_text, max_new_tokens=100):
        inputs = self.tokenizer(input_text, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs,  max_new_tokens=max_new_tokens)
        if self.model.config.is_encoder_decoder:
            outputs = outputs[0]
        else:
            outputs = outputs[0][len(inputs["input_ids"][0]) :]
        return self.tokenizer.decode(outputs, skip_special_tokens=True, spaces_between_special_tokens=False)

if __name__=='__main__':
    model = vicuna7b()
    print(model.generate("Yesterday was Thursday, today is Friday, so tomorrow is ", 10))
    print(model.generate("Yesterday was 2022-01-01, today is 2022-01-02, so tomorrow is ", 10))