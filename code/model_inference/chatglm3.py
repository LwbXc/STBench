from modelscope import AutoTokenizer, AutoModel
import torch
import pdb

class chatglm3(object):

    def __init__(self, model_path='~/.cache/modelscope/hub/ZhipuAI/chatglm3-6b', torch_dtype=torch.float32, device='cuda', max_new_tokens=5):
        print("Loading model from", model_path)
        self.model = AutoModel.from_pretrained(model_path, torch_dtype=torch_dtype, device_map=device, trust_remote_code=True)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model_path = model_path
        self.max_new_tokens = max_new_tokens
    
    def generate(self, input_text, max_new_tokens=None):
        if max_new_tokens is None:
            max_new_tokens = self.max_new_tokens
        inputs = self.tokenizer(input_text, return_tensors="pt").input_ids.to(self.model.device)
        outputs = self.model.generate(inputs, max_length=len(inputs[0])+max_new_tokens)
        return self.tokenizer.batch_decode(outputs)[0][len(input_text)+11:]

if __name__=='__main__':
    model = chatglm3()
    print(model.generate("Yesterday was Thursday, today is Friday, so tomorrow is ", 10))
    print(model.generate("Yesterday was 2022-01-01, today is 2022-01-02, so tomorrow is ", 10))