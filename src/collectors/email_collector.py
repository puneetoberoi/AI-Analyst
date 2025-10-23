# src/collectors/email_collector.py
import imaplib
import email
from datetime import datetime
import json
import base64

class EmailCollector:
    def __init__(self, smtp_user, smtp_pass):
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
        self.mail.login(smtp_user, smtp_pass)
    
    def fetch_new_questions(self):
        """Fetch unread emails with questions"""
        self.mail.select('inbox')
        _, message_ids = self.mail.search(None, 'UNSEEN', f'FROM "{self.smtp_user}"')
        
        questions = []
        for msg_id in message_ids[0].split():
            _, msg_data = self.mail.fetch(msg_id, '(RFC822)')
            email_body = email.message_from_bytes(msg_data[0][1])
            
            question = {
                'id': datetime.now().isoformat(),
                'subject': email_body['Subject'],
                'content': self.extract_body(email_body),
                'timestamp': datetime.now().isoformat(),
                'status': 'pending'
            }
            questions.append(question)
            
            # Mark as read
            self.mail.store(msg_id, '+FLAGS', '\\Seen')
        
        return questions
    
    def save_to_github(self, questions):
        """Save questions as GitHub database"""
        with open('data/questions_queue.json', 'r+') as f:
            existing = json.load(f)
            existing.extend(questions)
            f.seek(0)
            json.dump(existing, f, indent=2)
