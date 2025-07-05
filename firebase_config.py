import os
import logging
from google.cloud import firestore

def initialize_firebase():
    """Initialize Firebase services"""
    try:
        # Firebase will be initialized automatically using the environment variables
        logging.info("Firebase initialized successfully")
    except Exception as e:
        logging.error(f"Error initializing Firebase: {e}")
        raise

def get_firestore_client():
    """Get Firestore client"""
    try:
        # For client-side Firebase apps, we'll use the mock client for server-side operations
        # The real data operations will happen through the Firebase Client SDK on the frontend
        logging.info("Using mock Firestore client for development")
        return MockFirestoreClient()
    except Exception as e:
        logging.error(f"Error creating Firestore client: {e}")
        # Return a mock client for development if Firebase is not available
        return MockFirestoreClient()

class MockFirestoreClient:
    """Mock Firestore client for development when Firebase is not available"""
    
    def __init__(self):
        self.data = {
            'threads': {},
            'replies': {},
            'votes': {}
        }
        self.doc_counter = 0
    
    def collection(self, collection_name):
        return MockCollection(collection_name, self)
    
    def field_increment(self, value):
        return MockFieldIncrement(value)

class MockCollection:
    def __init__(self, name, client):
        self.name = name
        self.client = client
    
    def document(self, doc_id=None):
        if doc_id is None:
            self.client.doc_counter += 1
            doc_id = f"doc_{self.client.doc_counter}"
        return MockDocument(doc_id, self.name, self.client)
    
    def where(self, field, op, value):
        return MockQuery(self.name, self.client, [(field, op, value)])
    
    def order_by(self, field, direction='ASCENDING'):
        return MockQuery(self.name, self.client, [], [(field, direction)])
    
    def limit(self, count):
        return MockQuery(self.name, self.client, [], [], count)
    
    def stream(self):
        collection_data = self.client.data.get(self.name, {})
        for doc_id, doc_data in collection_data.items():
            yield MockDocumentSnapshot(doc_id, doc_data)

class MockQuery:
    def __init__(self, collection_name, client, filters=None, order_by=None, limit=None):
        self.collection_name = collection_name
        self.client = client
        self.filters = filters or []
        self.order_by_fields = order_by or []
        self.limit_count = limit
    
    def where(self, field, op, value):
        new_filters = self.filters + [(field, op, value)]
        return MockQuery(self.collection_name, self.client, new_filters, self.order_by_fields, self.limit_count)
    
    def order_by(self, field, direction='ASCENDING'):
        new_order_by = self.order_by_fields + [(field, direction)]
        return MockQuery(self.collection_name, self.client, self.filters, new_order_by, self.limit_count)
    
    def limit(self, count):
        return MockQuery(self.collection_name, self.client, self.filters, self.order_by_fields, count)
    
    def stream(self):
        collection_data = self.client.data.get(self.collection_name, {})
        results = []
        
        for doc_id, doc_data in collection_data.items():
            # Apply filters
            matches = True
            for field, op, value in self.filters:
                if op == '==' and doc_data.get(field) != value:
                    matches = False
                    break
            
            if matches:
                results.append((doc_id, doc_data))
        
        # Apply ordering (simplified)
        if self.order_by_fields:
            field, direction = self.order_by_fields[0]
            reverse = direction == 'DESCENDING'
            results.sort(key=lambda x: x[1].get(field, ''), reverse=reverse)
        
        # Apply limit
        if self.limit_count:
            results = results[:self.limit_count]
        
        for doc_id, doc_data in results:
            yield MockDocumentSnapshot(doc_id, doc_data)

class MockDocument:
    def __init__(self, doc_id, collection_name, client):
        self.id = doc_id
        self.collection_name = collection_name
        self.client = client
    
    def set(self, data):
        if self.collection_name not in self.client.data:
            self.client.data[self.collection_name] = {}
        self.client.data[self.collection_name][self.id] = data.copy()
    
    def get(self):
        collection_data = self.client.data.get(self.collection_name, {})
        if self.id in collection_data:
            return MockDocumentSnapshot(self.id, collection_data[self.id], exists=True)
        return MockDocumentSnapshot(self.id, {}, exists=False)
    
    def update(self, data):
        if self.collection_name not in self.client.data:
            self.client.data[self.collection_name] = {}
        if self.id not in self.client.data[self.collection_name]:
            self.client.data[self.collection_name][self.id] = {}
        
        for key, value in data.items():
            if isinstance(value, MockFieldIncrement):
                current = self.client.data[self.collection_name][self.id].get(key, 0)
                self.client.data[self.collection_name][self.id][key] = current + value.value
            else:
                self.client.data[self.collection_name][self.id][key] = value
    
    def delete(self):
        if (self.collection_name in self.client.data and 
            self.id in self.client.data[self.collection_name]):
            del self.client.data[self.collection_name][self.id]

class MockDocumentSnapshot:
    def __init__(self, doc_id, data, exists=True):
        self.id = doc_id
        self._data = data
        self.exists = exists
        self.reference = MockDocument(doc_id, '', None)
    
    def to_dict(self):
        return self._data.copy()

class MockFieldIncrement:
    def __init__(self, value):
        self.value = value
