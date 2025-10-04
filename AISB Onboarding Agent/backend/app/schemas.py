from pydantic import BaseModel, EmailStr
from typing import List, Dict, Optional


class ApplicantCreate(BaseModel):
	name: str
	email: EmailStr
	age: int
	degree: str
	skills: str
	track_preference: str


class ApplicantOut(BaseModel):
	id: int
	name: str
	email: EmailStr
	age: int
	degree: str
	skills: str
	track_preference: str
	status: str

	class Config:
		from_attributes = True


class QuizQuestionOut(BaseModel):
	id: int
	question: str
	options: List[str]

	class Config:
		from_attributes = True


class QuizGenerateRequest(BaseModel):
	applicant_id: int
	num_questions: int = 5


class QuizSubmitRequest(BaseModel):
	applicant_id: int
	answers: Dict[int, str]  # question_id -> chosen_option


class QuizSubmitResponse(BaseModel):
	score: float
	correct_count: int
	total: int


class VideoUploadResponse(BaseModel):
	transcript: str
	clarity_score: float
	relevance_score: float
	fluency_score: float
	overall_score: float


class AttendanceMarkRequest(BaseModel):
	applicant_id: int
	date: str  # YYYY-MM-DD
	present: bool


class AssignmentUploadResponse(BaseModel):
	file_path: str
	description: Optional[str] = None
