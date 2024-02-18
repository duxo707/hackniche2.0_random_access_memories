


import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
import json
from langchain_openai import OpenAIEmbeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from llama_index.core.query_engine import NLSQLTableQueryEngine
import os
import openai
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random
from llama_index.core.objects import SQLTableSchema
from llama_index.core.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema,
)
from llama_index.core import SQLDatabase, VectorStoreIndex
from llama_index.core.retrievers import SQLRetriever
from typing import List
from llama_index.core.query_pipeline import FnComponent
from llama_index.core.prompts.default_prompts import DEFAULT_TEXT_TO_SQL_PROMPT
from llama_index.core import PromptTemplate
from llama_index.core.query_pipeline import FnComponent
from llama_index.core.llms import ChatResponse
from llama_index.core import VectorStoreIndex, load_index_from_storage
from sqlalchemy import text
from llama_index.core.schema import TextNode
from llama_index.core import StorageContext
import os
from pathlib import Path
from typing import Dict
from pyvis.network import Network
from llama_index.core.retrievers import SQLRetriever
from typing import List
from llama_index.core.query_pipeline import FnComponent
from llama_index.core.query_pipeline import (
    QueryPipeline as QP,
    Link,
    InputComponent,
    CustomQueryComponent,
)
import sqlite3

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.environ["OPENAI_API_KEY"]

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class Post(Base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class Comment(Base):
    __tablename__ = 'comments'
    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    content = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class Tag(Base):
    __tablename__ = 'tags'
    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String(50), nullable=False)

class PostTag(Base):
    __tablename__ = 'post_tags'
    post_id = Column(Integer, ForeignKey('posts.post_id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.tag_id'), primary_key=True)

# Replace 'your_database_url' with your actual database connection URL
database_url = 'sqlite:///:memory:'
engine = create_engine(database_url, echo=True)

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a Pandas DataFrame using the given schema
data = {
    'users': [(f'user_{i}', f'user_{i}@example.com', 'hashed_password', datetime.utcnow()) for i in range(30)],
    'posts': [(f'Title_{i}', f'Content_{i}', random.randint(1, 30), datetime.utcnow()) for i in range(30)],
    'comments': [(random.randint(1, 30), random.randint(1, 30), f'Comment_{i}', datetime.utcnow()) for i in range(30)],
    'tags': [(f'Tag_{i}',) for i in range(30)],
    'post_tags': [(random.randint(1, 30), random.randint(1, 30)) for i in range(30)],
}

users_df = pd.DataFrame(data['users'], columns=['username', 'email', 'password_hash', 'created_at'])
posts_df = pd.DataFrame(data['posts'], columns=['title', 'content', 'user_id', 'created_at'])
comments_df = pd.DataFrame(data['comments'], columns=['post_id', 'user_id', 'content', 'created_at'])
tags_df = pd.DataFrame(data['tags'], columns=['tag_name'])
post_tags_df = pd.DataFrame(data['post_tags'], columns=['post_id', 'tag_id'])

# Insert data into the database using SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

# Users
session.bulk_insert_mappings(User, users_df.to_dict(orient='records'))

# Posts
session.bulk_insert_mappings(Post, posts_df.to_dict(orient='records'))

# Comments
session.bulk_insert_mappings(Comment, comments_df.to_dict(orient='records'))

# Tags
session.bulk_insert_mappings(Tag, tags_df.to_dict(orient='records'))

# PostTags
session.bulk_insert_mappings(PostTag, post_tags_df.to_dict(orient='records'))

# Commit the changes to the database
session.commit()

# Close the session
session.close()

# Create SQLTableSchema objects for all tables in the schema
my_table_schema_objs = [
    SQLTableSchema(table_name='users', context_str='User table summary'),
    SQLTableSchema(table_name='posts', context_str='Post table summary'),
    SQLTableSchema(table_name='comments', context_str='Comment table summary'),
    SQLTableSchema(table_name='tags', context_str='Tag table summary'),
    SQLTableSchema(table_name='post_tags', context_str='PostTag table summary'),
]

# # Display my_table_schema_objs
# for table_schema_obj in my_table_schema_objs:
#     print(table_schema_obj)



sql_database = SQLDatabase(engine)

table_node_mapping = SQLTableNodeMapping(sql_database)

obj_index = ObjectIndex.from_objects(
    my_table_schema_objs,
    table_node_mapping,
    VectorStoreIndex,
)
obj_retriever = obj_index.as_retriever(similarity_top_k=3)



sql_retriever = SQLRetriever(sql_database)


def get_table_context_str(table_schema_objs: List[SQLTableSchema]):
    """Get table context string."""
    context_strs = []
    for table_schema_obj in table_schema_objs:
        table_info = sql_database.get_single_table_info(
            table_schema_obj.table_name
        )
        if table_schema_obj.context_str:
            table_opt_context = " The table description is: "
            table_opt_context += table_schema_obj.context_str
            table_info += table_opt_context

        context_strs.append(table_info)
    return "\n\n".join(context_strs)


table_parser_component = FnComponent(fn=get_table_context_str)




def parse_response_to_sql(response: ChatResponse) -> str:
    """Parse response to SQL."""
    response = response.message.content
    sql_query_start = response.find("SQLQuery:")
    if sql_query_start != -1:
        response = response[sql_query_start:]
        # TODO: move to removeprefix after Python 3.9+
        if response.startswith("SQLQuery:"):
            response = response[len("SQLQuery:") :]
    sql_result_start = response.find("SQLResult:")
    if sql_result_start != -1:
        response = response[:sql_result_start]
    return response.strip().strip("```").strip()


sql_parser_component = FnComponent(fn=parse_response_to_sql)

text2sql_prompt = DEFAULT_TEXT_TO_SQL_PROMPT.partial_format(
    dialect=engine.dialect.name
)


response_synthesis_prompt_str = (
    "Given an input question, synthesize a response from the query results.\n"
    "Query: {query_str}\n"
    "SQL: {sql_query}\n"
    "SQL Response: {context_str}\n"
    "Response: "
)
response_synthesis_prompt = PromptTemplate(
    response_synthesis_prompt_str,
)



from llama_index.llms.openai import OpenAI

llm=OpenAI(model='gpt-3.5-turbo')

from llama_index.core.query_pipeline import (
    QueryPipeline as QP,
    Link,
    InputComponent,
    CustomQueryComponent,
)

qp = QP(
    modules={
        "input": InputComponent(),
        "table_retriever": obj_retriever,
        "table_output_parser": table_parser_component,
        "text2sql_prompt": text2sql_prompt,
        "text2sql_llm": llm,
        "sql_output_parser": sql_parser_component,
        "sql_retriever": sql_retriever,
        "response_synthesis_prompt": response_synthesis_prompt,
        "response_synthesis_llm": llm,
    },
    verbose=True,
)

qp.add_chain(["input", "table_retriever", "table_output_parser"])
qp.add_link("input", "text2sql_prompt", dest_key="query_str")
qp.add_link("table_output_parser", "text2sql_prompt", dest_key="schema")
qp.add_chain(
    ["text2sql_prompt", "text2sql_llm", "sql_output_parser", "sql_retriever"]
)
qp.add_link(
    "sql_output_parser", "response_synthesis_prompt", dest_key="sql_query"
)
qp.add_link(
    "sql_retriever", "response_synthesis_prompt", dest_key="context_str"
)
qp.add_link("input", "response_synthesis_prompt", dest_key="query_str")
qp.add_link("response_synthesis_prompt", "response_synthesis_llm")




# net = Network(notebook=True, cdn_resources="in_line", directed=True)
# net.from_nx(qp.dag)
# net.show("text2sql_dag.html")


def index_all_tables(
    sql_database: SQLDatabase, table_index_dir: str = "table_index_dir"
) -> Dict[str, VectorStoreIndex]:
    """Index all tables."""
    if not Path(table_index_dir).exists():
        os.makedirs(table_index_dir)

    vector_index_dict = {}
    engine = sql_database.engine
    for table_name in sql_database.get_usable_table_names():
        print(f"Indexing rows in table: {table_name}")
        if not os.path.exists(f"{table_index_dir}/{table_name}"):
            # get all rows from table
            with engine.connect() as conn:
                cursor = conn.execute(text(f'SELECT * FROM "{table_name}"'))
                result = cursor.fetchall()
                row_tups = []
                for row in result:
                    row_tups.append(tuple(row))

            # index each row, put into vector store index
            nodes = [TextNode(text=str(t)) for t in row_tups]

            # put into vector store index (use OpenAIEmbeddings by default)
            index = VectorStoreIndex(nodes)

            # save index
            index.set_index_id("vector_index")
            index.storage_context.persist(f"{table_index_dir}/{table_name}")
        else:
            # rebuild storage context
            storage_context = StorageContext.from_defaults(
                persist_dir=f"{table_index_dir}/{table_name}"
            )
            # load index
            index = load_index_from_storage(
                storage_context, index_id="vector_index"
            )
        vector_index_dict[table_name] = index

    return vector_index_dict


vector_index_dict = index_all_tables(sql_database)

test_retriever = vector_index_dict["users"].as_retriever(
    similarity_top_k=1
)
nodes = test_retriever.retrieve("User37")



sql_retriever = SQLRetriever(sql_database)


def get_table_context_and_rows_str(
    query_str: str, table_schema_objs: List[SQLTableSchema]
):
    """Get table context string."""
    context_strs = []
    for table_schema_obj in table_schema_objs:
        # first append table info + additional context
        table_info = sql_database.get_single_table_info(
            table_schema_obj.table_name
        )
        if table_schema_obj.context_str:
            table_opt_context = " The table description is: "
            table_opt_context += table_schema_obj.context_str
            table_info += table_opt_context

        # also lookup vector index to return relevant table rows
        vector_retriever = vector_index_dict[
            table_schema_obj.table_name
        ].as_retriever(similarity_top_k=2)
        relevant_nodes = vector_retriever.retrieve(query_str)
        if len(relevant_nodes) > 0:
            table_row_context = "\nHere are some relevant example rows (values in the same order as columns above)\n"
            for node in relevant_nodes:
                table_row_context += str(node.get_content()) + "\n"
            table_info += table_row_context

        context_strs.append(table_info)
    return "\n\n".join(context_strs)


table_parser_component = FnComponent(fn=get_table_context_and_rows_str)



qp = QP(
    modules={
        "input": InputComponent(),
        "table_retriever": obj_retriever,
        "table_output_parser": table_parser_component,
        "text2sql_prompt": text2sql_prompt,
        "text2sql_llm": llm,
        "sql_output_parser": sql_parser_component,
        "sql_retriever": sql_retriever,
        "response_synthesis_prompt": response_synthesis_prompt,
        "response_synthesis_llm": llm,
    },
    verbose=True,
)

qp.add_link("input", "table_retriever")
qp.add_link("input", "table_output_parser", dest_key="query_str")
qp.add_link(
    "table_retriever", "table_output_parser", dest_key="table_schema_objs"
)
qp.add_link("input", "text2sql_prompt", dest_key="query_str")
qp.add_link("table_output_parser", "text2sql_prompt", dest_key="schema")
qp.add_chain(
    ["text2sql_prompt", "text2sql_llm", "sql_output_parser", "sql_retriever"]
)
qp.add_link(
    "sql_output_parser", "response_synthesis_prompt", dest_key="sql_query"
)
qp.add_link(
    "sql_retriever", "response_synthesis_prompt", dest_key="context_str"
)
qp.add_link("input", "response_synthesis_prompt", dest_key="query_str")
qp.add_link("response_synthesis_prompt", "response_synthesis_llm")


# net = Network(notebook=True, cdn_resources="in_line", directed=True)
# net.from_nx(qp.dag)
# net.show("text2sql_dag.html")
# response = qp.run(query="give me top 5 users with highest posts")



query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database, llm=llm
)

i=1
while (i==1):
    query_str = str(input("enter the text input:  "))
    response = query_engine.query(query_str)
    answer=qp.run(query=query_str)
    sql_query = response.metadata['sql_query']

    import run
    content=run.generate_from_gemini(f"this is a query {sql_query}. give a robust and user-friendly javascript whole code with database connection and every function1 to execute this query")


    with open('result.js','w') as f:
        for con in content:
            f.write(con.replace('```','').replace('javascript',''))

    
    with open('answer.txt','w') as f:
        f.write(str(answer))

    print("Done--------------------------------")
    print()
    print()
    i=int(input("enter value of i:  "))



