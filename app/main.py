#!/usr/bin/env python3
"""
Daily IT News Automation Script
Fetches IT news/learning content from OpenAI GPT-4 and sends via email
"""

import os
import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DailyITNews:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.today = datetime.now().strftime('%Y-%m-%d')
        
    def create_prompt(self):
        """Create a prompt for OpenAI to get IT news/learning content"""
        prompts = [
            "Berätta om en aktuell tekniknyhet eller trend inom IT-branschen som en utvecklare bör känna till. Ge en pedagogisk genomgång med praktiska exempel.",
            "Välj ett viktigt koncept inom datavetenskap, nätverk, säkerhet eller mjukvaruutveckling och förklara det på ett sätt som hjälper en utvecklare att lära sig något nytt.",
            "Hitta en intressant teknisk artikel eller upptäckt från senaste tiden och sammanfatta huvudpunkterna på ett pedagogiskt sätt för utvecklare.",
            "Förklara ett avancerat programmeringskoncept eller arkitekturmönster som är relevant för moderna utvecklare, med praktiska exempel.",
            "Berätta om en ny teknologi, ramverk eller verktyg som utvecklare bör känna till, och varför det är viktigt."
        ]
        
        import random
        base_prompt = random.choice(prompts)
        
        return f"""Du är en erfaren IT-pedagog som hjälper utvecklare att lära sig nya saker.

{base_prompt}

Svara på svenska och strukturera ditt svar så här:

**Ämne:** [Kort beskrivning av vad du kommer att förklara]

**Huvudpunkter:**
- Punkt 1
- Punkt 2
- Punkt 3

**Detaljerad förklaring:**
[Pedagogisk förklaring med exempel]

**Praktiska tips:**
[Konkreta råd för utvecklare]

**Länkar för vidare läsning:**
[Relevanta länkar om tillgängliga]

Gör svaret informativt men lättläst, ungefär 300-500 ord."""

    def get_openai_response(self, prompt):
        """Get response from OpenAI GPT-4"""
        try:
            logger.info("Hämtar svar från OpenAI...")
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Du är en kunnig IT-pedagog som förklarar tekniska koncept på ett tydligt och pedagogiskt sätt."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            logger.info("Fick svar från OpenAI")
            return content
            
        except Exception as e:
            logger.error(f"Fel vid hämtning från OpenAI: {e}")
            return f"Tyvärr kunde jag inte hämta dagens IT-nyhet på grund av ett tekniskt fel: {str(e)}"

    def send_email(self, content):
        """Send email with the IT news content"""
        try:
            logger.info("Skickar e-post...")
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = os.getenv('EMAIL_FROM')
            msg['To'] = os.getenv('EMAIL_TO')
            msg['Subject'] = f"Dagens IT-nyhet - {self.today}"
            
            # Email body
            body = f"""Hej!

Här kommer dagens IT-nyhet/tekniska läropunkt:

{content}

---
Skickat automatiskt av Daily IT News Bot
Datum: {self.today}
"""
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Send email
            server = smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT')))
            server.starttls()
            server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASS'))
            server.send_message(msg)
            server.quit()
            
            logger.info("E-post skickad framgångsrikt")
            return True
            
        except Exception as e:
            logger.error(f"Fel vid sändning av e-post: {e}")
            return False

    def save_to_file(self, content):
        """Save content to daily log file"""
        try:
            log_dir = '/app/logs'
            os.makedirs(log_dir, exist_ok=True)
            
            filename = f"{log_dir}/{self.today}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Dagens IT-nyhet - {self.today}\n")
                f.write("=" * 50 + "\n\n")
                f.write(content)
                f.write(f"\n\nSkickad: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            logger.info(f"Loggad till {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Fel vid sparande av fil: {e}")
            return False

    def run(self):
        """Main execution method"""
        logger.info("Startar dagens IT-nyhetsutskick...")
        
        try:
            # Create prompt
            prompt = self.create_prompt()
            logger.info("Skapade prompt för OpenAI")
            
            # Get response from OpenAI
            content = self.get_openai_response(prompt)
            
            # Save to file
            self.save_to_file(content)
            
            # Send email
            email_sent = self.send_email(content)
            
            if email_sent:
                logger.info("Dagens IT-nyhetsutskick slutfört framgångsrikt!")
            else:
                logger.error("E-post kunde inte skickas, men innehållet sparades")
                
        except Exception as e:
            logger.error(f"Oväntat fel: {e}")

def main():
    """Main function"""
    news_bot = DailyITNews()
    news_bot.run()

if __name__ == "__main__":
    main() 