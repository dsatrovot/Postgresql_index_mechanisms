def extract_tokens(value,path=()):
    tokens = set()

    if isinstance(value, dict):
        for key, child in value.items():
            child_path = path + (key,)
            # print(f"{child_path} --> child_path")
            # print(tokens)
            tokens |= extract_tokens(child,child_path)

    elif isinstance(value, list):
        for child in value:
            tokens |= extract_tokens(child,path)
    else:
        tokens.add((path,value))
    return tokens

#tokens {
#     (("status",), "success"),
#     (("payment", "method"), "card"),
#     (("payment", "amount"), 1500),
#     (("tags",), "sale"),
#     (("tags",), "mobile")
# }

def search_all_tokens(index,tokens):
    if not tokens:
        return set()
    result = None
    for token in tokens:
        document_ids = index.get(token,set())

        if result is None:
            result = set(document_ids)
        else:
            result &= document_ids
        if not result:
            break
    return result or set()

def build_gin_index(documents):
    index = {}
    for document_id, document in documents.items():
        tokens = extract_tokens(document)
        for token in tokens:
            if token not in index:
                index[token] = set()
                # print(f"index insert new value -> {index}")
            index[token].add(document_id)
            # print(f"index -> {index}")
    return index

def search_token(index, token):
    return index.get(token,set())

# def jsonb_contains(document,query):
#     if isinstance(query,dict):
#         if not isinstance(document,dict):
#             return False
    
documents = {
    1: {"status": "success", "tags": ["sale", "mobile"]},
    2: {"status": "failed", "tags": ["mobile"]},
    3: {"status": "success", "tags": ["sale", "web"]},
    4: {"status": "pending", "tags": ["web"]},
}

gin = build_gin_index(documents)
print(gin)
print(search_token(gin,(('tags', ),'sale')))