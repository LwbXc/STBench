from modelscope import Model
from modelscope.models.nlp.llama2 import Llama2Tokenizer
import torch
import pdb

class llama2_7b(object):

    def __init__(self, model_path='~/.cache/modelscope/hub/modelscope/Llama-2-7b-ms', torch_dtype=torch.float32, device='cuda'):
        print("Loading model from", model_path)
        self.model = Model.from_pretrained(model_path, torch_dtype=torch_dtype, device_map=device)
        self.tokenizer = Llama2Tokenizer.from_pretrained(model_path)
        self.model_path = model_path

    def generate(self, input_text, max_new_tokens=100):
        inputs = self.tokenizer(input_text, return_tensors="pt").input_ids.to(self.model.device)
        outputs = self.model.generate(inputs, max_length=len(inputs[0])+max_new_tokens)
        return self.tokenizer.batch_decode(outputs)[0][len(input_text)+4:]

if __name__=='__main__':
    model = llama2_7b()
    print(model.generate("Yesterday was Thursday, today is Friday, so tomorrow is ", 10))
    print(model.generate("Yesterday was 2022-01-01, today is 2022-01-02, so tomorrow is ", 10))