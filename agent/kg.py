# -*- coding: utf-8 -*-
"""
@file    : kg.py
@date    : 2024-05-26
@author  : leafw
"""
from neo4j import GraphDatabase
import threading


class Neo4jGraph:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.driver = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Neo4jGraph, cls).__new__(cls)
                    cls._instance._init_driver('neo4j://localhost:7687', 'neo4j', 'password')
        return cls._instance

    def _init_driver(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.driver:
            self.driver.close()
            self.driver = None

    def create_topic(self, name):
        with self.driver.session() as session:
            session.write_transaction(self._create_topic, name)

    def create_document(self, name, content):
        with self.driver.session() as session:
            session.write_transaction(self._create_document, name, content)

    def create_paragraph(self, content):
        with self.driver.session() as session:
            session.write_transaction(self._create_paragraph, content)

    def create_keyword(self, word):
        with self.driver.session() as session:
            session.write_transaction(self._create_keyword, word)

    def create_contains_topic(self, parent_name, child_name):
        with self.driver.session() as session:
            session.write_transaction(self._create_contains_topic, parent_name, child_name)

    def create_contains_document(self, topic_name, document_name):
        with self.driver.session() as session:
            session.write_transaction(self._create_contains_document, topic_name, document_name)

    def create_contains_paragraph(self, document_name, paragraph_content):
        with self.driver.session() as session:
            session.write_transaction(self._create_contains_paragraph, document_name, paragraph_content)

    def create_contains_keyword(self, paragraph_content, keyword):
        with self.driver.session() as session:
            session.write_transaction(self._create_contains_keyword, paragraph_content, keyword)

    def create_links_paragraph(self, content1, content2):
        with self.driver.session() as session:
            session.write_transaction(self._create_links_paragraph, content1, content2)

    @staticmethod
    def _create_topic(tx, name):
        tx.run("CREATE (t:Topic {name: $name})", name=name)

    @staticmethod
    def _create_document(tx, name, content):
        tx.run("CREATE (d:Document {name: $name, content: $content})", name=name, content=content)

    @staticmethod
    def _create_paragraph(tx, content):
        tx.run("CREATE (p:Paragraph {content: $content})", content=content)

    @staticmethod
    def _create_keyword(tx, word):
        tx.run("CREATE (k:Keyword {word: $word})", word=word)

    @staticmethod
    def _create_contains_topic(tx, parent_name, child_name):
        tx.run("""
            MATCH (p:Topic {name: $parent_name}), (c:Topic {name: $child_name})
            CREATE (p)-[:CONTAINS]->(c)
        """, parent_name=parent_name, child_name=child_name)

    @staticmethod
    def _create_contains_document(tx, topic_name, document_name):
        tx.run("""
            MATCH (t:Topic {name: $topic_name}), (d:Document {name: $document_name})
            CREATE (t)-[:CONTAINS]->(d)
        """, topic_name=topic_name, document_name=document_name)

    @staticmethod
    def _create_contains_paragraph(tx, document_name, paragraph_content):
        tx.run("""
            MATCH (d:Document {name: $document_name}), (p:Paragraph {content: $paragraph_content})
            CREATE (d)-[:CONTAINS]->(p)
        """, document_name=document_name, paragraph_content=paragraph_content)

    @staticmethod
    def _create_contains_keyword(tx, paragraph_content, keyword):
        tx.run("""
            MATCH (p:Paragraph {content: $paragraph_content}), (k:Keyword {word: $keyword})
            CREATE (p)-[:CONTAINS]->(k)
        """, paragraph_content=paragraph_content, keyword=keyword)

    @staticmethod
    def _create_links_paragraph(tx, content1, content2):
        tx.run("""
            MATCH (p1:Paragraph {content: $content1}), (p2:Paragraph {content: $content2})
            CREATE (p1)-[:LINKS]->(p2)
        """, content1=content1, content2=content2)


# 示例使用
if __name__ == "__main__":
    neo4j_graph = Neo4jGraph()
    neo4j_graph.create_topic("Project A")
    neo4j_graph.create_topic("Subproject A1")
    neo4j_graph.create_document("Document 1", "This is the content of document 1.")
    neo4j_graph.create_paragraph("This is the first paragraph of document 1.")
    neo4j_graph.create_paragraph("This is the second paragraph of document 1.")
    neo4j_graph.create_keyword("Keyword1")
    neo4j_graph.create_contains_topic("Project A", "Subproject A1")
    neo4j_graph.create_contains_document("Project A", "Document 1")
    neo4j_graph.create_contains_paragraph("Document 1", "This is the first paragraph of document 1.")
    neo4j_graph.create_contains_keyword("This is the first paragraph of document 1.", "Keyword1")
    neo4j_graph.create_links_paragraph("This is the first paragraph of document 1.",
                                       "This is the second paragraph of document 1.")
    neo4j_graph.close()
