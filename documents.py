class Documents:
    def __init__(self):
        self.docs = {}

    def add(self, doc_path, ingest_status=True):
        if not self._exists(doc_path):
            self.docs[doc_path] = {"ingest": ingest_status}
        else:
            print(f"Document '{doc_path}' already exists. Ignoring.")

    def _exists(self, doc_path):
        return doc_path in self.docs

    def clear(self):
        self.docs = {}

    def __len__(self):
        return len(self.docs)

    def __getitem__(self, item):
        return self.docs[item]

    def __iter__(self):
        return iter(self.docs.items())

    def __str__(self):
        return str(self.docs)

    def __repr__(self):
        return repr(self.docs)

    def update_ingest_status(self, doc_path, ingest_status):
        if doc_path in self.docs:
            self.docs[doc_path]["ingest"] = ingest_status

    def get_all_uningested_files(self):
        return [doc for doc, details in self.docs.items() if not details["ingest"]]
