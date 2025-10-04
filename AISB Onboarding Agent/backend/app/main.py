from fastapi import FastAPI, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict
import json
import os

from .database import Base, engine, get_db
from . import models, schemas
from .agents.screening_agent import ScreeningAgent
from .agents.quiz_agent import QuizAgent
from .agents.video_agent import VideoAgent
from .agents.selection_agent import SelectionAgent

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bootcamp Onboarding Platform")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

screening_agent = ScreeningAgent()
quiz_agent = QuizAgent()
video_agent = VideoAgent()
selection_agent = SelectionAgent()


@app.post("/apply", response_model=schemas.ApplicantOut)
def apply(applicant: schemas.ApplicantCreate, db: Session = Depends(get_db)):
	existing = db.query(models.Applicant).filter(models.Applicant.email == applicant.email).first()
	if existing:
		return existing
	new_app = models.Applicant(
		name=applicant.name,
		email=applicant.email,
		age=applicant.age,
		degree=applicant.degree,
		skills=applicant.skills,
		track_preference=applicant.track_preference,
	)
	db.add(new_app)
	db.commit()
	db.refresh(new_app)
	return new_app


@app.get("/screen-applications")
def screen_applications(db: Session = Depends(get_db)):
	apps = db.query(models.Applicant).all()
	updated = []
	for a in apps:
		res = screening_agent.screen(a.age, a.degree, a.skills)
		a.status = "eligible" if res.eligible else "ineligible"
		db.add(a)
		updated.append({"id": a.id, "eligible": res.eligible, "reason": res.reason})
	db.commit()
	return {"results": updated}


@app.post("/quiz/generate")
def generate_quiz(req: schemas.QuizGenerateRequest, db: Session = Depends(get_db)):
	applicant = db.query(models.Applicant).get(req.applicant_id)
	if not applicant:
		return {"error": "Applicant not found"}
	questions = quiz_agent.generate(req.num_questions)
	created = []
	for q_text, options, answer in questions:
		qq = models.QuizQuestion(
			applicant_id=applicant.id,
			question=q_text,
			options=json.dumps(options),
			answer=answer,
		)
		db.add(qq)
		db.flush()
		created.append({"id": qq.id, "question": qq.question, "options": options})
	db.commit()
	return {"questions": created}


@app.post("/quiz/submit", response_model=schemas.QuizSubmitResponse)
def submit_quiz(req: schemas.QuizSubmitRequest, db: Session = Depends(get_db)):
	qs = db.query(models.QuizQuestion).filter(models.QuizQuestion.applicant_id == req.applicant_id).all()
	correct_map: Dict[int, str] = {q.id: q.answer for q in qs}
	correct_count, total = quiz_agent.grade(correct_map, req.answers)
	score = (correct_count / total) * 100 if total > 0 else 0.0
	sub = models.QuizSubmission(applicant_id=req.applicant_id, answers=json.dumps(req.answers), score=score)
	db.add(sub)

	applicant = db.query(models.Applicant).get(req.applicant_id)
	if applicant:
		if score >= 60:
			applicant.status = "quiz_passed"
		else:
			applicant.status = "eligible"
		db.add(applicant)

	db.commit()
	return schemas.QuizSubmitResponse(score=score, correct_count=correct_count, total=total)


@app.post("/video/upload", response_model=schemas.VideoUploadResponse)
async def upload_video(
	applicant_id: int = Form(...),
	topic: str = Form(...),
	file: UploadFile = File(...),
	db: Session = Depends(get_db),
):
	# Save file to disk (MVP)
	uploads_dir = "backend/uploads/videos"
	os.makedirs(uploads_dir, exist_ok=True)
	file_path = os.path.join(uploads_dir, file.filename)
	with open(file_path, "wb") as f:
		f.write(await file.read())

	analysis = video_agent.transcribe_and_score(file_path, topic)
	rec = models.VideoSubmission(
		applicant_id=applicant_id,
		topic=topic,
		video_path=file_path,
		transcript=analysis.transcript,
		clarity_score=analysis.clarity_score,
		relevance_score=analysis.relevance_score,
		fluency_score=analysis.fluency_score,
		overall_score=analysis.overall_score,
	)
	db.add(rec)

	applicant = db.query(models.Applicant).get(applicant_id)
	if applicant:
		if analysis.overall_score >= 0.75:
			applicant.status = "video_passed"
		else:
			applicant.status = "quiz_passed"
		db.add(applicant)

	db.commit()
	return schemas.VideoUploadResponse(
		transcript=analysis.transcript,
		clarity_score=analysis.clarity_score,
		relevance_score=analysis.relevance_score,
		fluency_score=analysis.fluency_score,
		overall_score=analysis.overall_score,
	)


@app.get("/final-selection")
def final_selection(db: Session = Depends(get_db)):
	# collect candidates with quiz/video scores
	apps = db.query(models.Applicant).filter(models.Applicant.status.in_(["quiz_passed", "video_passed", "selected"]))
	apps = apps.all()
	compiled = []
	for a in apps:
		quiz_score = 0.0
		video_score = 0.0
		last_quiz = (
			db.query(models.QuizSubmission)
			.filter(models.QuizSubmission.applicant_id == a.id)
			.order_by(models.QuizSubmission.created_at.desc())
			.first()
		)
		if last_quiz:
			quiz_score = last_quiz.score
		last_video = (
			db.query(models.VideoSubmission)
			.filter(models.VideoSubmission.applicant_id == a.id)
			.order_by(models.VideoSubmission.created_at.desc())
			.first()
		)
		if last_video:
			video_score = last_video.overall_score * 100
		compiled.append({
			"id": a.id,
			"name": a.name,
			"track_preference": a.track_preference,
			"quiz_score": quiz_score,
			"video_score": video_score,
		})

	result = selection_agent.select(compiled)

	# mark selected
	selected_ids = [x["id"] for grp in result.values() for x in grp]
	for a in db.query(models.Applicant).filter(models.Applicant.id.in_(selected_ids)).all():
		a.status = "selected"
		db.add(a)
	db.commit()
	return result


@app.post("/attendance")
def mark_attendance(req: schemas.AttendanceMarkRequest, db: Session = Depends(get_db)):
	rec = db.query(models.Attendance).filter(
		models.Attendance.applicant_id == req.applicant_id,
		models.Attendance.date == req.date,
	).first()
	if rec:
		rec.present = req.present
	else:
		rec = models.Attendance(applicant_id=req.applicant_id, date=req.date, present=req.present)
		db.add(rec)
	db.commit()
	return {"ok": True}


@app.post("/assignments/upload", response_model=schemas.AssignmentUploadResponse)
async def upload_assignment(
	applicant_id: int = Form(...),
	description: str = Form(""),
	file: UploadFile = File(...),
	db: Session = Depends(get_db),
):
	uploads_dir = "backend/uploads/assignments"
	os.makedirs(uploads_dir, exist_ok=True)
	file_path = os.path.join(uploads_dir, file.filename)
	with open(file_path, "wb") as f:
		f.write(await file.read())

	rec = models.Assignment(applicant_id=applicant_id, file_path=file_path, description=description)
	db.add(rec)
	db.commit()
	return schemas.AssignmentUploadResponse(file_path=file_path, description=description)
