from modelscope import AutoTokenizer, Model
import torch
import pdb

class falcon7b(object):

    def __init__(self, model_path='~/.cache/modelscope/hub/AI-ModelScope/falcon-7b', torch_dtype=torch.float32, device='cuda', max_new_tokens=5):
        print("Loading model from", model_path)
        self.model = Model.from_pretrained(model_path, torch_dtype=torch_dtype, device_map=device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model_path = model_path
        self.max_new_tokens = max_new_tokens
    
    def generate(self, input_text, max_new_tokens=None):
        if max_new_tokens is None:
            max_new_tokens = self.max_new_tokens
        inputs = self.tokenizer(input_text, return_tensors="pt").input_ids.to(self.model.device)
        outputs = self.model.generate(inputs, max_length=len(inputs[0])+max_new_tokens)
        return self.tokenizer.batch_decode(outputs)[0][len(input_text):]

if __name__=='__main__':
    model = falcon7b()
    print(model.generate("Yesterday was Thursday, today is Friday, so tomorrow is ", 10))
    print(model.generate("Yesterday was 2022-01-01, today is 2022-01-02, so tomorrow is ", 10))