md5_path = "./md5.text"

collection_name = "rag"
persist_directory = "./chroma_db"

similarity_threshold = 2

# splitter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " ", ""]
max_split_char_number = 1000

embedding_model = "text-embedding-v4"
chat_model_name = "qwen-max"

session_config = {
        "configurable":{
            "session_id": "user_001"
        }

    }