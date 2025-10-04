from typing import List, Dict, Tuple
import random

TOPICS = [
	{"q": "Which library is commonly used for deep learning in Python?", "options": ["NumPy", "Pandas", "PyTorch", "Flask"], "answer": "C"},
	{"q": "What does LLM stand for?", "options": ["Large Language Model", "Low Latency Module", "Logical Learning Matrix", "Long Layer Memory"], "answer": "A"},
	{"q": "Which is a supervised learning algorithm?", "options": ["K-Means", "Linear Regression", "PCA", "t-SNE"], "answer": "B"},
	{"q": "What is tokenization?", "options": ["Optimizing weights", "Splitting text", "Merging datasets", "Compressing models"], "answer": "B"},
	{"q": "What is the purpose of a validation set?", "options": ["Train model", "Tune hyperparameters", "Store backups", "Test hardware"], "answer": "B"},
]


class QuizAgent:
	def generate(self, num_questions: int) -> List[Tuple[str, List[str], str]]:
		questions = random.sample(TOPICS, k=min(num_questions, len(TOPICS)))
		return [(q["q"], q["options"], q["answer"]) for q in questions]

	def grade(self, correct_answers: Dict[int, str], submitted: Dict[int, str]) -> Tuple[int, int]:
		correct = 0
		total = len(correct_answers)
		for qid, ans in submitted.items():
			if qid in correct_answers and correct_answers[qid] == ans:
				correct += 1
		return correct, total
