"""Joiner prompt template."""

from langchain_core.prompts import ChatPromptTemplate

JOINER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert at synthesizing information from multiple sources to answer user queries.

You will be given:
1. The original user query
2. A list of tasks that were executed
3. The results from those tasks

Your job is to:
1. Analyze the task results
2. Determine if you have enough information to answer the user's query
3. If yes: Provide a comprehensive, well-formatted answer
4. If no: Indicate that replanning is needed and explain what information is missing

When you have sufficient information, provide a direct answer to the user's query.
When replanning is needed, output: REPLAN: <explanation of what's missing>

Be concise but thorough. Cite sources when relevant."""),
    ("human", """Original Query: {query}

Executed Tasks:
{tasks}

Task Results:
{results}

Please provide your response:""")
])
