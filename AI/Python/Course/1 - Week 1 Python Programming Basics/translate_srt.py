import os
import re
import shutil
import time
from deep_translator import GoogleTranslator

def translate_srt_files():
    # Target files 2.srt to 8.srt
    target_files = [f for f in os.listdir('.') if f.endswith('.srt') and f[0] in '2345678']
    
    translator = GoogleTranslator(source='en', target='vi')
    
    for filename in sorted(target_files):
        print(f"\n[{time.strftime('%H:%M:%S')}] Processing {filename}...")
        
        # Backup the original file
        backup_name = filename + '.bak'
        if not os.path.exists(backup_name):
            shutil.copy2(filename, backup_name)
            
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse SRT blocks
        blocks = content.strip().split('\n\n')
        new_blocks = []
        parsed_blocks = []
        
        for block in blocks:
            lines = block.split('\n')
            if len(lines) < 3:
                parsed_blocks.append({"original": block, "clean_text": None})
                continue
                
            text_lines = '\n'.join(lines[2:])
            # Remove HTML/subtitle tags like <font color="..."> and </font>
            clean_text = re.sub(r'<[^>]+>', '', text_lines).strip()
            
            # If no actual letters, no translation needed (e.g. symbols, empty)
            if not clean_text or not re.search(r'[a-zA-Z]', clean_text):
                parsed_blocks.append({"original": block, "clean_text": None})
            else:
                # Replace newlines with spaces for a single translation block context
                clean_text_single_line = clean_text.replace('\n', ' ')
                parsed_blocks.append({
                    "original": block,
                    "clean_text": clean_text_single_line
                })
        
        texts_to_translate = [b["clean_text"] for b in parsed_blocks if b["clean_text"]]
        translated_texts = []
        batch_size = 40
        
        print(f"Translating {len(texts_to_translate)} chunks...")
        
        # Translate in batches
        for i in range(0, len(texts_to_translate), batch_size):
            batch = texts_to_translate[i:i+batch_size]
            try:
                translated_batch = translator.translate_batch(batch)
                translated_texts.extend(translated_batch)
            except Exception as e:
                print(f"Batch {i} failed: {e}. Translating one by one...")
                for txt in batch:
                    try:
                        translated_texts.append(translator.translate(txt))
                    except Exception as e2:
                        print(f"Single translation failed for '{txt}': {e2}")
                        translated_texts.append("")
                        
            time.sleep(1.5) # Delay to respect rate limits
            
        # Reconstruct SRT content
        t_idx = 0
        for b in parsed_blocks:
            if b["clean_text"]:
                trans = translated_texts[t_idx] if t_idx < len(translated_texts) else ""
                t_idx += 1
                if trans:
                    # Append the translation in yellow font color
                    new_block = b["original"] + f'\n<font color="#ffff00">{trans}</font>'
                else:
                    new_block = b["original"]
                new_blocks.append(new_block)
            else:
                new_blocks.append(b["original"])
                
        # Write back to file
        new_content = '\n\n'.join(new_blocks) + '\n'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"[{time.strftime('%H:%M:%S')}] Successfully saved {filename}.")

if __name__ == "__main__":
    translate_srt_files()
