import torch
from transformers import GPT2LMHeadModel
import requests
import time


def init():
    model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')

 
def process(url,secret):
    while True: 
        r = requests.get(url + "/testapi/list")
        json_data = r.json()
        if length > 0:
            length = len(json_data)
            last_data = json_data[length -1 ]
            get_id = last_data["id"]
            get_text = last_data["texts"]
            gpt2_predicted = do_predict(get_text) 
            update = requests.get(url + "/testapi/update/{}?secret={}&data={}".format(get_id,secret, gpt2_predicted ))
        else:
            print("No data, waiting 5 sec")
            time.sleep(5)
        
        pass

def do_predict(text):
    input_ids = tokenizer.encode(text)
    gen_ids = model.generate(torch.tensor([input_ids]),
        max_length=128,
        repetition_penalty=2.0,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
        bos_token_id=tokenizer.bos_token_id,
        use_cache=True
    )
    generated = tokenizer.decode(gen_ids[0,:].tolist())
    return generated
    
    
init()
process(os.getenv("ENDPOINT_URL"), os.getenv("SECRET"))
