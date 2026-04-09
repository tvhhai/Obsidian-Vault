import os
import re
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from deep_translator import GoogleTranslator

def translate_block(idx, clean_text):
    if not clean_text:
        return idx, ""
    try:
        translator = GoogleTranslator(source='en', target='vi')
        return idx, translator.translate(clean_text)
    except Exception as e:
        print(f"Failed translation at idx {idx}: {e}")
        return idx, ""

def process_file(filename):
    print(f"\n[{time.strftime('%H:%M:%S')}] Processing {filename}...")
    
    # Restoring from backup if it exists to ensure idempotency
    backup_name = filename + '.bak'
    if os.path.exists(backup_name):
        shutil.copy2(backup_name, filename)
    else:
        shutil.copy2(filename, backup_name)
        
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    blocks = content.strip().split('\n\n')
    parsed_blocks = []
    
    for i, block in enumerate(blocks):
        lines = block.split('\n')
        if len(lines) < 3:
            parsed_blocks.append({"original": block, "clean_text": None, "idx": i})
            continue
            
        text_lines = '\n'.join(lines[2:])
        clean_text = re.sub(r'<[^>]+>', '', text_lines).strip()
        
        if not clean_text or not re.search(r'[a-zA-Z]', clean_text):
            parsed_blocks.append({"original": block, "clean_text": None, "idx": i})
        else:
            clean_text_single_line = clean_text.replace('\n', ' ')
            parsed_blocks.append({
                "original": block,
                "clean_text": clean_text_single_line,
                "idx": i
            })

    print(f"Starting {len(parsed_blocks)} blocks translation for {filename}...")
    translated_dict = {}
    
    # Use ThreadPool to speed up the translation heavily
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for b in parsed_blocks:
            if b["clean_text"]:
                futures.append(executor.submit(translate_block, b["idx"], b["clean_text"]))
                
        # Progress tracking
        finished = 0
        total = len(futures)
        for future in as_completed(futures):
            idx, translation = future.result()
            translated_dict[idx] = translation
            finished += 1
            if finished % 200 == 0:
                print(f"{filename}: {finished}/{total} translations done.")

    # Reconstruct blocks
    new_blocks = []
    for b in parsed_blocks:
        idx = b["idx"]
        trans = translated_dict.get(idx, "")
        if trans:
            new_block = b["original"] + f'\n<font color="#ffff00">{trans}</font>'
            new_blocks.append(new_block)
        else:
            new_blocks.append(b["original"])
            
    # Write back
    new_content = '\n\n'.join(new_blocks) + '\n'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"[{time.strftime('%H:%M:%S')}] Finished saving {filename}")

def main():
    target_files = [f for f in os.listdir('.') if f.endswith('.srt') and f[0] in '2345678']
    
    for filename in sorted(target_files):
        # We can skip file 2 if we know it's fully processed. But restoring from backup is safe.
        # Actually file 2 was fully processed, let's skip it to save time
        if filename.startswith('2 '): 
            print(f"Skipping {filename} as it's already translated.")
            continue
            
        process_file(filename)

if __name__ == "__main__":
    main()
