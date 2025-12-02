import json
import random

# Vertex AI Vector Search requires:
# 1. JSONL format (one JSON object per line)
# 2. 'id' field (string)
# 3. 'embedding' field (array of floats)
# 4. Optional: 'restricts' (for filtering)

# textembedding-gecko@003 produces 768-dimensional embeddings
DIMENSIONS = 768

def generate_placeholder():
    # Create a single dummy record
    record = {
        "id": "placeholder_0",
        "embedding": [0.0] * DIMENSIONS # Dummy zero vector
    }
    
    output_file = "placeholder.json"
    
    with open(output_file, "w") as f:
        json.dump(record, f)
        # No newline needed for a single record, but good practice for JSONL
        f.write("\n")
        
    print(f"✅ Generated {output_file} with {DIMENSIONS}-dimensional embedding.")

if __name__ == "__main__":
    generate_placeholder()
