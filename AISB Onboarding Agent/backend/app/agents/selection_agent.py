from typing import List, Dict

class SelectionAgent:
	def select(self, eligible_applicants: List[Dict]) -> Dict[str, List[Dict]]:
		# Expect eligible_applicants as list of dict with keys: id, track_preference, quiz_score, video_score
		generative = [a for a in eligible_applicants if a.get("track_preference", "").lower().startswith("generative")]
		agentic = [a for a in eligible_applicants if a.get("track_preference", "").lower().startswith("agentic")]

		def score_key(a):
			return (a.get("quiz_score", 0.0) + a.get("video_score", 0.0))

		generative = sorted(generative, key=score_key, reverse=True)[:50]
		agentic = sorted(agentic, key=score_key, reverse=True)[:50]

		return {"Generative": generative, "Agentic": agentic}
