import chromadb
from chunker import chunk_directory


def build_index(repo_path: str, db_path: str = './chroma_data'):
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection('codebase')

    chunks = chunk_directory(repo_path)
    collection.add(
        ids=[f'{c["file_path"]}::{c["name"]}' for c in chunks],
        documents=[c['code'] for c in chunks],
        metadatas=[{
            'file_path': c['file_path'],
            'name': c['name'],
            'calls': ','.join(c['calls']),
        } for c in chunks],
    )
    print(f'Indexed {len(chunks)} functions/classes from {repo_path}')
    return collection


if __name__ == '__main__':
    build_index('../target_repo')
