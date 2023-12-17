import os
import set_api_key
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.multi_modal_llms.generic_utils import ImageDocument




def call_gemini_vision(user_input: str):
    temp_dir_path = os.path.abspath("./temp")
    print(temp_dir_path)

    file_paths = [os.path.join(temp_dir_path, file) for file in os.listdir(temp_dir_path)]
    print(file_paths)

    image_documents = []
    for file_path in file_paths:
        # Create ImageDocument objects instead of appending raw image data
        image_documents.append(ImageDocument(image_path=file_path))

    gemini_pro_vision = GeminiMultiModal(model="models/gemini-pro-vision", api_key=set_api_key.GOOGLE_API_KEY)

    complete_response = gemini_pro_vision.complete(
        prompt=user_input,
        image_documents=image_documents,
    )

    return complete_response

if __name__ == "__main__":
    call_gemini_vision()

