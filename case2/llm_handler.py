from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class MistralHandler:
    def __init__(self):
        self.model_name = "mistralai/Mistral-7B-v0.1"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
    def generate_response(self, prompt: str, max_length: int = 256) -> str:
        """LLM'den yanıt üretir"""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        outputs = self.model.generate(
            inputs["input_ids"],
            max_length=max_length,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.replace(prompt, "").strip()
    
    def format_prompt(self, user_input: str, context: str = "") -> str:
        """Prompt formatlar"""
        base_prompt = f"""Sen bir banka chatbotusun. Araç finansmanı konusunda müşterilere yardımcı oluyorsun.
        
Bağlam: {context}

Kullanıcı: {user_input}

Chatbot: """
        return base_prompt

    def process_sss_response(self, user_query: str, matched_qa: str) -> str:
        """SSS yanıtlarını işler ve formatlar"""
        prompt = f"""Aşağıdaki soru-cevap çiftini kullanarak kullanıcının sorusunu yanıtla.
        Yanıtı nazik ve yardımcı bir şekilde formatla.
        
Kullanıcı Sorusu: {user_query}
İlgili SSS: {matched_qa}

Yanıt: """
        return self.generate_response(prompt) 