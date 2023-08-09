import openai
import global_var
import aspose.words as aw

def prep_editor(extension):
    submit_text = ""

    if extension == ".txt":
        with open("text_files/original.txt", "r", encoding='utf-8', errors="ignore") as f:
            original_text = f.read()
        paragraph_text = original_text.split("\n")
        for paragraph in paragraph_text:
            submit_text += paragraph
            submit_text += "\n"
    
    if extension == ".docx":
        original_text = aw.Document("text_files/original.docx")
        for paragraph in original_text.get_child_nodes(aw.NodeType.PARAGRAPH, True):    
            #paragraph = paragraph.as_paragraph()
            submit_text += paragraph.to_string(aw.SaveFormat.TEXT)
        submit_text = submit_text[81:-144] #eliminate Aspose Words propaganda :)    
    
    global_var.chunk_count = (len(submit_text) // 4000) + 1
    return submit_text
    
    
def run_editor(submit_text):
    #clear the edited.txt file
    edited_text = open("text_files/edited.txt", "w", encoding='utf-8', errors="ignore")
    edited_text.close()
    #reopen with "append"
    edited_text = open("text_files/edited.txt", "a", encoding='utf-8', errors="ignore")
    
    run_count = 0
    while submit_text:
        adj_count = 0 #adjustment counter
        submit_chunk = ""
        if len(submit_text) > 4000:
            while submit_text[3999 + adj_count] != " ": #makes sure to end on a space
                adj_count += 1
        submit_chunk += submit_text[:4000 + adj_count]
        submit_text = submit_text[4000 + adj_count:]
        
        #turn this on, and next line off, for for testing purposes.
        #edited_text.write(submit_chunk)
        edited_text.write(openai_api(submit_chunk))
        
        #prints progress to terminal. Need to get something working for client side.
        run_count += 1
        print("Finished {:.0%}".format(run_count / global_var.chunk_count))
        
        #edit_progress = "Finished {:.0%}".format(run_count / chunk_count)
        # progress(edit_progress)
        # time.sleep(1) - using this to test a progress bar feedback
    
    edited_text.close()


def openai_api(original_text):
    
    openai.api_key = global_var.key #filled in by upload()
        
    prompt = "A professional copy editor has taken the text below and fixed all copy editing mistakes. He used the Chicago Manual of Style for writing numbers, capitalization, headers, and other guidelines. He did not edit the voice or style of the prose. He formatted quotes as ASCII directional quotes.\n\n"
    prompt += original_text + "\n\nRewritten by the editor:\n"

    chatgpt_response = openai.Completion.create(
        model="text-davinci-003", 
        prompt=prompt, 
        temperature= 0.1, 
        max_tokens=2000, top_p=1, 
        frequency_penalty=0, 
        presence_penalty=0)['choices'][0]['text']
    return chatgpt_response