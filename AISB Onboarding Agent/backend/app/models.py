from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Applicant(Base):
	__tablename__ = "applicants"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, nullable=False)
	email = Column(String, unique=True, index=True, nullable=False)
	age = Column(Integer, nullable=False)
	degree = Column(String, nullable=False)
	skills = Column(Text, default="")
	track_preference = Column(String, nullable=False)  # Generative or Agentic
	status = Column(String, default="applied")  # applied, eligible, ineligible, quiz_passed, video_passed, selected
	created_at = Column(DateTime, default=datetime.utcnow)

	quiz_submissions = relationship("QuizSubmission", back_populates="applicant")
	video_submissions = relationship("VideoSubmission", back_populates="applicant")
	attendance_records = relationship("Attendance", back_populates="applicant")
	assignments = relationship("Assignment", back_populates="applicant")


class QuizQuestion(Base):
	__tablename__ = "quiz_questions"

	id = Column(Integer, primary_key=True, index=True)
	applicant_id = Column(Integer, ForeignKey("applicants.id"), index=True)
	question = Column(Text, nullable=False)
	options = Column(Text, nullable=False)  # JSON string list
	answer = Column(String, nullable=False)  # correct option key like "A"
	created_at = Column(DateTime, default=datetime.utcnow)


class QuizSubmission(Base):
	__tablename__ = "quiz_submissions"

	id = Column(Integer, primary_key=True, index=True)
	applicant_id = Column(Integer, ForeignKey("applicants.id"), index=True)
	answers = Column(Text, nullable=False)  # JSON string map
	score = Column(Float, default=0.0)
	created_at = Column(DateTime, default=datetime.utcnow)

	applicant = relationship("Applicant", back_populates="quiz_submissions")


class VideoSubmission(Base):
	__tablename__ = "video_submissions"

	id = Column(Integer, primary_key=True, index=True)
	applicant_id = Column(Integer, ForeignKey("applicants.id"), index=True)
	topic = Column(String, nullable=False)
	video_path = Column(String, nullable=False)
	transcript = Column(Text, default="")
	clarity_score = Column(Float, default=0.0)
	relevance_score = Column(Float, default=0.0)
	fluency_score = Column(Float, default=0.0)
	overall_score = Column(Float, default=0.0)
	created_at = Column(DateTime, default=datetime.utcnow)

	applicant = relationship("Applicant", back_populates="video_submissions")


class Attendance(Base):
	__tablename__ = "attendance"

	id = Column(Integer, primary_key=True, index=True)
	applicant_id = Column(Integer, ForeignKey("applicants.id"), index=True)
	date = Column(String, nullable=False)  # ISO date string
	present = Column(Boolean, default=False)

	applicant = relationship("Applicant", back_populates="attendance_records")


class Assignment(Base):
	__tablename__ = "assignments"

	id = Column(Integer, primary_key=True, index=True)
	applicant_id = Column(Integer, ForeignKey("applicants.id"), index=True)
	file_path = Column(String, nullable=False)
	description = Column(Text, default="")
	created_at = Column(DateTime, default=datetime.utcnow)

	applicant = relationship("Applicant", back_populates="assignments")
