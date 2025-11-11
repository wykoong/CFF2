from flask import Blueprint, request, jsonify, render_template, current_app
from datetime import datetime, UTC
from ..dao import get_db, close_db
from ..models import Feedback, FeedbackStatus
import re
import logging
from pathlib import Path

bp = Blueprint('feedback', __name__)
logger = logging.getLogger(__name__)

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

def validate_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.match(email))

@bp.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get('email', '').strip()
    if not email or not validate_email(email):
        return jsonify({"error": "Valid email is required"}), 400

    message = data.get('message', '').strip()
    if not message:
        return jsonify({"error": "Message is required"}), 400
    if len(message) > 5000:
        return jsonify({"error": "Message too long (max 5000 chars)"}), 400

    feedback = Feedback(
        email=email,
        message=message,
        phone=data.get('phone'),
        metadata={
            'user_agent': request.headers.get('User-Agent'),
            'source_ip': request.remote_addr
        },
        created_at=datetime.now(UTC).isoformat(),
        status=FeedbackStatus.PENDING.value
    )

    conn = get_db()
    try:
        cur = conn.execute(
            """INSERT INTO feedback (email, phone, message, status, metadata, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (feedback.email, feedback.phone, feedback.message, feedback.status,
             str(feedback.metadata), feedback.created_at)
        )
        conn.commit()
        feedback.id = cur.lastrowid
        logging.debug(f"Inserted feedback with ID: {feedback.id}")
        return jsonify(feedback.to_dict()), 201
    except Exception as e:
        conn.rollback()
        logging.error(f"Error saving feedback: {e}")
        return jsonify({"error": "Server error saving feedback"}), 500
    finally:
        close_db(conn)

@bp.route('/feedback', methods=['GET'])
def show_form():
    try:
        logger.debug("Attempting to render feedback form template")
        return render_template('public/feedback.html')
    except Exception as e:
        logger.exception("Failed to render template")
        return (
            f"<html><body><h1>Feedback form unavailable</h1>"
            f"<p>Server error details: {str(e)}</p></body></html>",
            500
        )