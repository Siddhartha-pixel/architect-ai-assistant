# backend/app/ai_service.py
import os
import google.generativeai as genai
import replicate
from PIL import Image

# Configure APIs from environment variables
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def run_ai_pipeline(prompt: str, sketch_path: str):
    """
    Full AI pipeline to generate design concepts from a prompt and sketch.
    """
    try:
        # Step 1: Analyze prompt and sketch with Gemini Vision
        print("Step 1: Analyzing with Gemini Vision...")
        vision_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        sketch_image = Image.open(sketch_path)
        
        prompt_for_vision = f"""
        You are an expert architectural assistant. Analyze the following user brief and rough sketch.
        Synthesize them into a highly detailed and descriptive prompt for an AI image generation model like Stable Diffusion.
        The prompt should capture the style, materials, lighting, and environment.
        Focus on creating a photorealistic architectural rendering.
        User Brief: "{prompt}"
        """
        response = vision_model.generate_content([prompt_for_vision, sketch_image])
        sd_prompt = response.text
        print(f"Generated Stable Diffusion Prompt: {sd_prompt}")

        # Step 2: Generate image with Stable Diffusion (via Replicate)
        print("Step 2: Generating image with Replicate...")
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={"prompt": sd_prompt}
        )
        generated_image_url = output[0]
        print(f"Generated Image URL: {generated_image_url}")

        # Step 3: Generate narrative and compliance check with Gemini
        print("Step 3: Generating narrative with Gemini...")
        text_model = genai.GenerativeModel('gemini-pro')
        prompt_for_narrative = f"""
        You are an architectural critic. Based on the original design brief "{prompt}",
        create a short "Design Narrative" explaining the concept.
        Also, perform a mock "Building Code Compliance Check", identifying one potential consideration
        (e.g., related to safety, energy, or accessibility).
        Return the response as a JSON object with two keys: "narrative" and "compliance_check".
        """
        narrative_response = text_model.generate_content(prompt_for_narrative)
        # Simple parsing, in production use a more robust JSON parser
        narrative_text = narrative_response.text.replace("```json", "").replace("```", "").strip()
        print(f"Generated Narrative/Compliance: {narrative_text}")

        return {
            "generated_image_url": generated_image_url,
            "narrative_and_compliance": narrative_text
        }

    except Exception as e:
        print(f"An error occurred in the AI pipeline: {e}")
        return None