import os
import json

class VectorDB:
    def __init__(self, collection_name="knowledge_base"):
        self.collection_name = collection_name
        self.db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
        self.documents = []
        self.metadatas = []
        self.ids = []
        
        self._load_from_disk()
    
    def _load_from_disk(self):
        try:
            db_file = os.path.join(self.db_path, f"{self.collection_name}.json")
            if os.path.exists(db_file):
                with open(db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.documents = data.get('documents', [])
                    self.metadatas = data.get('metadatas', [])
                    self.ids = data.get('ids', [])
        except Exception as e:
            print(f"加载数据库失败: {e}")
    
    def _save_to_disk(self):
        try:
            os.makedirs(self.db_path, exist_ok=True)
            db_file = os.path.join(self.db_path, f"{self.collection_name}.json")
            with open(db_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'documents': self.documents,
                    'metadatas': self.metadatas,
                    'ids': self.ids
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据库失败: {e}")
    
    def _calculate_similarity(self, text1, text2):
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        intersection = words1 & words2
        union = words1 | words2
        return len(intersection) / len(union)
    
    def add_documents(self, documents, metadatas=None, ids=None):
        if ids is None:
            ids = [f"doc_{len(self.documents) + i}" for i in range(len(documents))]
        
        if metadatas is None:
            metadatas = [{} for _ in range(len(documents))]
        
        self.documents.extend(documents)
        self.metadatas.extend(metadatas)
        self.ids.extend(ids)
        
        self._save_to_disk()
    
    def query(self, query_text, n_results=5):
        similarities = []
        for i, doc in enumerate(self.documents):
            similarity = self._calculate_similarity(query_text, doc)
            similarities.append((i, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_results = similarities[:n_results]
        
        result_documents = []
        result_metadatas = []
        result_distances = []
        
        for i, similarity in top_results:
            result_documents.append(self.documents[i])
            result_metadatas.append(self.metadatas[i])
            result_distances.append(1 - similarity)
        
        return {
            'documents': result_documents,
            'metadatas': result_metadatas,
            'distances': result_distances
        }
    
    def get_all_documents(self):
        return {
            'documents': self.documents,
            'metadatas': self.metadatas,
            'ids': self.ids
        }
    
    def delete_documents(self, ids):
        new_docs = []
        new_metas = []
        new_ids = []
        
        for doc, meta, id_ in zip(self.documents, self.metadatas, self.ids):
            if id_ not in ids:
                new_docs.append(doc)
                new_metas.append(meta)
                new_ids.append(id_)
        
        self.documents = new_docs
        self.metadatas = new_metas
        self.ids = new_ids
        
        self._save_to_disk()
    
    def clear_collection(self):
        self.documents = []
        self.metadatas = []
        self.ids = []
        self._save_to_disk()