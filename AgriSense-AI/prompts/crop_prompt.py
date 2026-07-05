# crop_prompt.py

def get_crop_prompt(crop, problem):
    prompt = f"""
You are an expert in agriculture and farming advisory system.

Your task is to help farmers solve their crop-related problems.

Follow this format strictly:

1. Problem Summary
2. Possible Cause
3. Solution (step by step)
4. Prevention Tips

Crop: {crop}
Problem: {problem}

Give simple, practical and farmer-friendly advice in Tamil and English mix.
Avoid technical jargon.
"""
    return prompt