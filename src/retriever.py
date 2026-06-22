import chromadb


def retrieve_context(query: str, db_path='./chroma_data', top_k=5) -> str:
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_collection('codebase')

    primary = collection.query(query_texts=[query], n_results=top_k)
    seen_names = set()
    blocks, related_calls = [], []

    for doc, meta in zip(primary['documents'][0], primary['metadatas'][0]):
        seen_names.add(meta['name'])
        blocks.append(f"# {meta['file_path']} :: {meta['name']}\n{doc}")
        related_calls.extend(meta.get('calls', '').split(','))

    for call_name in set(related_calls):
        if not call_name or call_name in seen_names:
            continue
        hop = collection.query(query_texts=[call_name], n_results=1)
        if hop['documents'][0]:
            meta = hop['metadatas'][0][0]
            blocks.append(
                f"# {meta['file_path']} :: {meta['name']} (related)\n{hop['documents'][0][0]}")

    return '\n\n'.join(blocks)
