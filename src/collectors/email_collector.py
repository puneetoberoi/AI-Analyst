# src/collectors/email_collector.py
import imaplib
import email
from email.header import decode_header
import os
import json
from datetime import datetime

class EmailCollector:
    def __init__(self):
        self.smtp_user = os.environ.get('SMTP_USER')
        self.smtp_pass = os.environ.get('SMTP_PASS')
        
    def connect(self):
        """Connect to Gmail IMAP"""
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        self.mail.login(self.smtp_user, self.smtp_pass)
        self.mail.select("INBOX")
        
    def fetch_unread_questions(self):
        """Fetch unread emails from myself"""
        self.connect()
        
        # Search for unread emails from self
        search_criteria = f'(UNSEEN FROM "{self.smtp_user}")'
        status, messages = self.mail.search(None, search_criteria)
        
        if status != 'OK':
            return []
        
        questions = []
        email_ids = messages[0].split()
        
        for email_id in email_ids:
            # Fetch email
            status, msg_data = self.mail.fetch(email_id, "(RFC822)")
            
            if status != 'OK':
                continue
                
            # Parse email
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Extract subject
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            
            # Extract body
            body = self.extract_body(msg)
            
            # Create question object
            question = {
                'id': datetime.now().isoformat() + '_' + email_id.decode(),
                'subject': subject,
                'content': body,
                'timestamp': datetime.now().isoformat(),
                'status': 'pending',
                'email_id': email_id.decode()
            }
            
            questions.append(question)
            
            # Mark as read
            self.mail.store(email_id, '+FLAGS', '\\Seen')
        
        self.mail.logout()
        return questions
    
    def extract_body(self, msg):
        """Extract email body"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        
        return body.strip()
    
    def save_questions(self, questions):
        """Save questions to database"""
        file_path = 'data/questions_queue.json'
        
        # Load existing questions
        existing = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                if content:
                    existing = json.loads(content)
        
        # Add new questions
        existing.extend(questions)
        
        # Save back
        with open(file_path, 'w') as f:
            json.dump(existing, f, indent=2)
        
        return len(questions)

if __name__ == "__main__":
    collector = EmailCollector()
    questions = collector.fetch_unread_questions()
    
    if questions:
        count = collector.save_questions(questions)
        print(f"✅ Saved {count} new questions")
        for q in questions:
            print(f"  - {q['subject']}")
    else:
        print("📭 No new questions found")
