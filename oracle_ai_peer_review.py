import os
import sys
import oci

compartment_id = os.getenv("ORACLE_COMPARTMENT_ID")
CONFIG_PROFILE = "DEFAULT"
config = oci.config.from_file('~/.oci/config', CONFIG_PROFILE)

endpoint = "https://inference.generativeai.uk-london-1.oci.oraclecloud.com"



def review_code(content, filename):
    generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config=config, service_endpoint=endpoint, retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10,240))
    chat_detail = oci.generative_ai_inference.models.ChatDetails()

    chat_request = oci.generative_ai_inference.models.CohereChatRequest()
    chat_request.message = f"You are an expert developer that needs to peer review code in a file. Please provide feedback with a focus on performance, security and presentation. Include the new code for the complete file in your response and include comments were possible. Please review the file called {filename}: ```{content}```"
    chat_request.max_tokens = 4000
    chat_request.temperature = 1
    chat_request.frequency_penalty = 0
    chat_request.top_p = 0.75
    chat_request.top_k = 0


    chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id="ocid1.generativeaimodel.oc1.uk-london-1.amaaaaaask7dceyahpidcahiiyhcdmnvicfxo7suq3pxcimkyik75mbxziqq")
    chat_detail.chat_request = chat_request
    chat_detail.compartment_id = compartment_id
    chat_response = generative_ai_inference_client.chat(chat_detail)
    return chat_response.data.chat_response.text

def write_feedback(content, filename, output_dir):
    feedback = review_code(content, filename)
    output_path = f"{output_dir}/{filename.replace('/', '_')}.md"
    with open(output_path, 'w') as f:
        f.write(feedback)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: oracle_ai_peer_review.py <content> <filename> <output_dir>")
        sys.exit(1)
    content = sys.argv[1]
    filename = sys.argv[2]
    output_dir = sys.argv[3]
    print(f"Reviewing {filename} and storing in {output_dir}/{filename}.md")
    write_feedback(content, filename, output_dir)

