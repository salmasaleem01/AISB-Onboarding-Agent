from dataclasses import dataclass

AI_KEYWORDS = {"python", "ml", "machine learning", "ai", "deep learning", "nlp", "llm", "data science"}


@dataclass
class ScreeningResult:
	eligible: bool
	reason: str


class ScreeningAgent:
	def __init__(self) -> None:
		pass

	def screen(self, age: int, degree: str, skills: str) -> ScreeningResult:
		if not (18 <= age <= 25):
			return ScreeningResult(False, "Age not in 18-25 range")
		if "bs" not in degree.lower():
			return ScreeningResult(False, "Degree is not BS")
		skills_lower = skills.lower()
		has_ai = any(keyword in skills_lower for keyword in AI_KEYWORDS)
		if not has_ai:
			return ScreeningResult(False, "AI-related skills not found")
		return ScreeningResult(True, "Meets eligibility criteria")
