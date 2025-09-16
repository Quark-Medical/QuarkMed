# encoding: utf8
import json
import re
import sys
from collections import defaultdict


def extract_llm_res(filename):
    # prediction results
    pred_res = []
    for line in open(filename, 'r', encoding='utf8'):
        # prediction result should follow this format: {"uid": "", "level": "", "department": "", "pred_str": "", "answer": ""}
        j = json.loads(line)
        ori_pred_str = j['pred_str']
        pred_str = ori_pred_str.strip()
        # some models may explain first, and finally summarize with JSON.
        if '\n\n' in pred_str:
            sps = pred_str.split('\n\n')
            if 'json' in sps[-1]:
                pred_str = sps[-1]
            else:
                pred_str = sps[0]
        try:
            # try to parse the prediction in json format
            pred_j = json.loads(pred_str.replace('```json', '').replace('```', ''))
            if isinstance(pred_j, dict):
                prediction = pred_j['answer']
            elif isinstance(pred_j, list):
                prediction = ''.join([x['answer'] for x in pred_j])
            else:
                raise ValueError(f"invalid data: {pred_str}")
        except json.JSONDecodeError:
            # json.loads failed, try extracting the answer string by regex
            if match := re.search(r'"answer":."(.*)"', pred_str):
                prediction = match.group(1)
            elif match := re.search(r'"answer":."(.*)$', pred_str):
                prediction = match.group(1)
            else:
                print(f"invalid data: {ori_pred_str}")
                prediction = ''
        except KeyError:
            prediction = ''
        if isinstance(prediction, list):  # multiple answers
            if isinstance(prediction[0], dict):
                # answers in list should string not dict
                print(prediction)
                prediction = ''
            else:
                prediction = ''.join(prediction)
        if prediction:
            prediction = re.sub(r'[、",|\s]', '', prediction)
            prediction = ''.join(sorted(list(prediction)))  # Some answers are in the wrong alphabetical order, need sort.
        j['prediction'] = prediction
        j['is_correct'] = j['prediction'] == j['answer']
        pred_res.append(j)
    calculate_accuracies(pred_res)


def calculate_accuracies(data_list):
    type_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    category_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    type_category_stats = defaultdict(lambda: defaultdict(lambda: {"correct": 0, "total": 0}))
    option_category_stats = defaultdict(lambda: {"correct": 0, "total": 0})

    tol, invalid_num = len(data_list), 0
    for item in data_list:
        t = item["level"]
        c = item["department"]
        ans = item["answer"]
        pred = item["prediction"]

        if not pred:
            invalid_num += 1

        if '案例分析' in item['type']:
            opt_type = '案例分析题'
        elif '题干' in item['type']:
            opt_type = '共用题干题'
        else:
            if len(ans) <= 1:
                opt_type = '单选题'
            else:
                opt_type = '多选题'

        correct = (ans == pred)

        # 更新 option type 总数和正确数量
        option_category_stats[opt_type]["total"] += 1
        if correct:
            option_category_stats[opt_type]["correct"] += 1

        # 更新 type 总数和正确数
        type_stats[t]["total"] += 1
        if correct:
            type_stats[t]["correct"] += 1

        # 更新 category 总数和正确数
        category_stats[c]["total"] += 1
        if correct:
            category_stats[c]["correct"] += 1

        # 更新 type-category 组合的总数和正确数
        type_category_stats[t][c]["total"] += 1
        if correct:
            type_category_stats[t][c]["correct"] += 1

    # 打印每个 type 的准确率
    print("每个考试类型的准确率：")
    for t, stats in type_stats.items():
        acc = stats["correct"] / stats["total"] if stats["total"] > 0 else 0
        print(f"Type: {t}, Accuracy: {acc:.2%}")

    print("每类题型的准确率：")
    for opt, stats in option_category_stats.items():
        acc = stats["correct"] / stats["total"] if stats["total"] > 0 else 0
        print(f"Option Type: {opt}, Accuracy: {acc:.2%}")

    print("\n每个科室的准确率：")
    for c, stats in category_stats.items():
        acc = stats["correct"] / stats["total"] if stats["total"] > 0 else 0
        print(f"Category: {c}, Accuracy: {acc:.2%}")

    # print("\n各考试类型下各科室的准确率：")
    # for t, cat_stats in type_category_stats.items():
    #     print(f"\nType: {t}")
    #     for c, stats in cat_stats.items():
    #         acc = stats["correct"] / stats["total"] if stats["total"] > 0 else 0
    #         print(f"  Category: {c}, Accuracy: {acc:.2%}")
    print(f"总数：{tol}，无效答案数量：{invalid_num}")


if __name__ == '__main__':
    assert len(sys.argv) >=2, print('please provide a file')
    extract_llm_res(sys.argv[1])
