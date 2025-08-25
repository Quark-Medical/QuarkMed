## Evaluation method for CPQExam

### Introduction

CPQExam is a dataset built from the Chinese Health Professional Qualification Examination, an exam that physicians in China are required to pass for professional licensure and career advancement. The exam contains a large number of questions focusing on case analysis and practical application.

the prompt we used to test all the model is as follows:
```text
请思考后回答以下选择题目，以json格式返回结果，除此以外不要返回其它任何信息。如:
{"answer": "A/B/C"}
问题:
{question}
回答:
{option}
```

for example, a complete prompt to request the model is as follows:
```text
请思考后回答以下选择题目，以json格式返回结果，除此以外不要返回其它任何信息。如:
{"answer": "A/B/C"}
问题:
鼻腔鼻窦上皮源性恶性肿瘤CT征象中，比较有特征性表现的是
回答:
A. 鼻腔、鼻窦内软组织影
B. 肿瘤呈膨胀性生长
C. 有明显的骨质破坏
D. 无明显的骨质破坏
E. 增强扫描肿瘤无强化
```

### Get Metrics

```bash
python3 evaluation.py result_file_name.jsonl
```