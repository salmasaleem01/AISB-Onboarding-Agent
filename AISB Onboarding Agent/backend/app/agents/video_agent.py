from dataclasses import dataclass

@dataclass
class VideoAnalysis:
	transcript: str
	clarity_score: float
	relevance_score: float
	fluency_score: float
	overall_score: float


class VideoAgent:
	def transcribe_and_score(self, video_path: str, topic: str) -> VideoAnalysis:
		# MVP: Fake a transcript and simple heuristic scores
		transcript = f"Transcript of {video_path} about {topic}."
		clarity = 0.8
		relevance = 0.85
		fluency = 0.82
		overall = round((clarity + relevance + fluency) / 3, 2)
		return VideoAnalysis(transcript, clarity, relevance, fluency, overall)
