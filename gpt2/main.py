import torch
from transformers import GPT2LMHeadModel
import requests
import time
import os

model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')
from transformers import PreTrainedTokenizerFast
tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
    bos_token='</s>', eos_token='</s>', unk_token='<unk>',
    pad_token='<pad>', mask_token='<mask>'
)
 
def process(url,secret):
    while True: 
        r = requests.get("{}/textapi/list".format(url))
        json_data = r.json()
        length = len(json_data)
        if length > 0:
            last_data = json_data[length -1 ]
            get_id = last_data["id"]
            get_text = last_data["texts"]
            gpt2_predicted = do_predict(get_text) 
            update = requests.get("{}/textapi/update/{}?secret={}&data={}".format(url,get_id,secret, gpt2_predicted ))
        else:
            print("No data, waiting 5 sec")
            time.sleep(5)
        
        pass

def do_predict(text):
    print("data received : {}".format(text))
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
    print("data returned : {}".format(generated))
    return generated
    
     
process(os.getenv("ENDPOINT_URL"), os.getenv("SECRET"))
