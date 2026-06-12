import os
import json
import re
from collections import defaultdict
from pathlib import Path

SKILLS_DIR = r"C:\Users\harshal.bhoyar\.gemini\antigravity\skills"
MANIFEST_PATH = os.path.join(SKILLS_DIR, "manifest.json")

def parse_frontmatter(file_path):
    name, desc = "Unknown", "No description"
    tags = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'^---\s*(.*?)\s*---', content, re.DOTALL)
            if match:
                fm = match.group(1)
                name_m = re.search(r'^name:\s*(.+)$', fm, re.MULTILINE)
                desc_m = re.search(r'^description:\s*(.+?)(?:\n[a-z]+:|$)', fm, re.MULTILINE | re.DOTALL)
                tags_m = re.search(r'^tags:\s*\[(.*?)\]', fm, re.MULTILINE)
                if name_m: name = name_m.group(1).strip()
                if desc_m: desc = desc_m.group(1).strip().replace('\n', ' ')
                if tags_m: tags = [t.strip() for t in tags_m.group(1).split(',')]
    except Exception as e:
        pass
    return name, desc, tags

def generate_indexes():
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    categories = manifest['categories']
    
    # Store skills by category -> sub_category -> list of skills
    categorized_skills = {c: defaultdict(list) for c in categories}
    
    for item in os.listdir(SKILLS_DIR):
        item_path = os.path.join(SKILLS_DIR, item)
        if not os.path.isdir(item_path) or item.startswith('.') or item in categories:
            continue
        
        skill_md = os.path.join(item_path, "SKILL.md")
        if not os.path.exists(skill_md):
            continue
            
        name, desc, tags = parse_frontmatter(skill_md)
        text_to_search = f"{name} {desc} {' '.join(tags)}".lower()
        
        # Determine category
        best_cat = "utilities"
        best_score = 0
        for cat, cat_info in categories.items():
            score = sum(1 for kw in cat_info['keywords'] if kw.lower() in text_to_search)
            if score > best_score:
                best_score = score
                best_cat = cat
                
        # Determine sub_category
        sub_cat = tags[0].lower() if tags else "general"
        sub_cat = re.sub(r'[^a-z0-9]', '_', sub_cat)
        
        categorized_skills[best_cat][sub_cat].append({
            "id": item,
            "name": name,
            "description": desc,
            "path": skill_md
        })

    # Balance sub-categories to max 30 items
    for cat in categorized_skills:
        new_sub_cats = defaultdict(list)
        for sub_cat, skills in categorized_skills[cat].items():
            if len(skills) > 30:
                # Split
                chunks = [skills[i:i+30] for i in range(0, len(skills), 30)]
                for idx, chunk in enumerate(chunks):
                    new_sub_cats[f"{sub_cat}_{idx+1}"] = chunk
            else:
                new_sub_cats[sub_cat] = skills
        categorized_skills[cat] = new_sub_cats

    # Write indexes
    for cat, sub_cats in categorized_skills.items():
        cat_dir = os.path.join(SKILLS_DIR, cat)
        os.makedirs(cat_dir, exist_ok=True)
        
        cat_index = []
        for sub_cat, skills in sub_cats.items():
            sub_dir = os.path.join(cat_dir, sub_cat)
            os.makedirs(sub_dir, exist_ok=True)
            
            # Write skill-index.json
            skill_index_path = os.path.join(sub_dir, "skill-index.json")
            with open(skill_index_path, 'w', encoding='utf-8') as f:
                json.dump({"sub_category": sub_cat, "skills": skills}, f, indent=2)
                
            cat_index.append({
                "sub_category": sub_cat,
                "count": len(skills),
                "index_path": skill_index_path
            })
            
        # Write category-index.json
        cat_index_path = os.path.join(cat_dir, "category-index.json")
        with open(cat_index_path, 'w', encoding='utf-8') as f:
            json.dump({"category": cat, "sub_categories": cat_index}, f, indent=2)
            
    print("Successfully generated 3-tier indexes!")

if __name__ == "__main__":
    generate_indexes()
