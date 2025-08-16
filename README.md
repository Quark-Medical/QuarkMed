# Quark Med


This repository introduces [**QuarkMed**](./report/QuarkMed_Technical_Report.pdf), a 32-billion parameter Large Language Model (LLM) developed by Alibaba Group's Quark Medical Team. It is specifically designed to address the complex and high-stakes demands of the medical domain, aiming to provide a robust foundation for applications like AI-powered consultations, diagnostic assistance, and medical search. A standout achievement is its **70% accuracy on the Chinese Medical Licensing Examination**.

#### Core Contributions
*   **Comprehensive Data Pipeline:** The model was trained on a massive, curated medical dataset of approximately 1 trillion tokens, including textbooks, clinical guidelines, and research literature, ensuring deep domain knowledge.
*   **Advanced Instruction Tuning:** A multi-task instruction fine-tuning (IFT) process was used to align the model with a wide range of medical abilities, from basic comprehension to complex clinical reasoning.
*   **Dual-Stage Reinforcement Learning (RL):** QuarkMed underwent a two-stage RL process. The first stage focused on improving verifiable medical reasoning (e.g., diagnosis, test ordering). The second stage aligned the model with human preferences for safety, honesty, and helpfulness.
*   **Integrated Retrieval-Augmented Generation (RAG):** The model is trained with a RAG system to ground its answers in timely and authoritative medical sources, significantly reducing hallucinations and improving factual accuracy.

#### Training Methodology
The development of QuarkMed follows a systematic multi-stage training pipeline:
1.  **Instruction Fine-Tuning (IFT):** An initial phase to teach the base model to follow a diverse set of medical instructions.
2.  **Supervised Fine-Tuning (SFT):** The model is further trained on a high-quality dataset of medical queries and expert-verified answers to enhance its conversational and reasoning abilities.
3.  **Stage 1 RL (Medical Reasoning):** A specialized RL phase using verifiable rewards to improve performance on structured tasks like disease diagnosis and medication recommendation.
4.  **Stage 2 RL (General Alignment):** A final RL phase to align the model with human values, optimizing for helpfulness, honesty, and safety using preference data.

### Key Results
QuarkMed was evaluated on a wide range of public (external) and private (internal) benchmarks. It demonstrates state-of-the-art performance for a model of its size and shows competitive results even against larger, proprietary models.

#### External Benchmark Performance (vs. Close-Size Models)
QuarkMed shows superior performance compared to other leading open-source models in the ~30B parameter class across various medical question-answering and reasoning tasks.

| Benchmark Dataset | QuarkMed (32B) | Qwen3-32B | o3-mini |
| :--- | :---: | :---: | :---: |
| MedQA (US) | **86.02%** | 87.19% | 74.46% |
| CMExam | **88.60%** | 85.80% | 70.74% |
| DiagnosisArena | **61.90%** | 52.17% | 56.00% |
| MedBullets | **77.27%** | 74.14% | 83.66% |
| **Average Score** | **71.36%** | 69.02% | 70.07% |

#### Internal Benchmark Performance (CPQExam)
On the private **CPQExam** (Chinese Health Professional Qualification Examination), QuarkMed demonstrates exceptional performance, significantly outperforming even the most powerful proprietary models. The scores marked with indicate results achieved with knowledge augmentation (RAG).


| CPQExam Category | Gemini-2.5-pro | gpt-4o | DeepSeek-R1 | Qwen3-32B | **QuarkMed (without RAG)** | **QuarkMed (with RAG)** |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| Primary Level | 80.50% | 71.67% | 81.42% | 78.76% | 81.50% | **83.30%** |
| Intermediate Professional | 79.87% | 64.15% | 82.58% | 72.42% | 75.08% | **85.40%** |
| Assoc. Senior Professional | 65.29% | 43.92% | 72.33% | 56.16% | 66.67% | **75.30%** |
| Senior Professional | 33.60% | 12.40% | 38.70% | 30.34% | 51.70% | **67.70%** |
| Case Analysis | 43.05% | 23.74% | 48.75% | 37.69% | 49.85% | **58.50%** |


We're planning to release our internal benchmark that curated from CPQExam to boost the medical related AI research. Stay tuned. 

