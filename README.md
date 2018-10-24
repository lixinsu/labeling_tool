# labeling_tool

## Motivation
This labeling tool is used to label a text pair in a pre-defined classes.  
For example, we label the question and passage in SQuAD 2.0 to the classes in which each indicates why the question is not answerbale.

## Usage
1. **python format_data.py** to transform the data in SQuAD 2.0 to 
```python
{'passage': text,
'query': text,
'query_id': text,
}
```
2. **python server.py** starts labeling.
