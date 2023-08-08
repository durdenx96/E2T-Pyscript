import imaplib
import email
import re
from email.header import decode_header 
import telegram
import time
import asyncio

# Define the async function that sends the message
async def send_telegram_message(subject, extracted_urls):
    if extracted_urls:
        urls_message = "\n".join(extracted_urls)
        message = "Subject: {}\nURLs:\n{}".format(subject, urls_message)
        bot = telegram.Bot(token=telegram_token)
        await bot.send_message(chat_id=user_id, text=message)
        print("Sent message to telegram")

# email instance and authentiation
email_server = 'imap.gmail.com'
email_user = 'xxxx@gmail.com'
email_password = 'abcdefghijklmno'

# telegram bot token and chat ID
telegram_token = 'kjhaeiedpike-sjfjlkn-ljgavafafkaa-ba783'
user_id = '123456789'

# initialize bot
bot = telegram.Bot(token=telegram_token)
print("Bot initialized")

# connect to email server
mail = imaplib.IMAP4_SSL(email_server, timeout=30)
mail.login(email_user, email_password)
print("Logged in to email:", email_user)

mail.select("INBOX", readonly=True)
print("Inbox selected")

# search emails 
result, data = mail.search(None, "FROM xxxxx@gmail.com")
email_ids = data[0].split()


# url pattern object as search condition
url_pattern = r'(https://example\.com/(link1|link2))'

# loop through emails
print("Searching email inbox...")
for num in email_ids[:20]:
    _, msg_data = mail.fetch(num, "(RFC822)")
    msg = email.message_from_bytes(msg_data[0][1])

    print("Looping through emails...")

    # Decode the email subject and handle non-ASCII characters
    subject = msg["subject"]
    if subject:
        subject, encoding = decode_header(msg["subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
    else:
        subject = "No Subject"
        print("Subject decoded")

    # Extract and print URLs from the email body
    urls_found = False
    for part in msg.walk():
        content_type = part.get_content_type()
        if content_type == "text/plain":
            payload = part.get_payload(decode=True)
            if isinstance(payload, bytes):
                try:
                    body = payload.decode('utf-8', errors='replace')
                    extracted_urls= []
                    for match in re.finditer(url_pattern, body):
                        url = match.group()
                        print("URL:", url)
                        extracted_urls.append(url)
                        urls_found = True

                        # Send to Telegram bot
                        if urls_found:
                            asyncio.run(send_telegram_message(subject, extracted_urls))
                    else:
                        print("No URLs found...")    
                except UnicodeDecodeError:
                    print("Unable to decode the email body.")
            else:
                print("No payload found.")

    if urls_found:
        print("-" * 40)

    # troubleshooting: time delay 
    time.sleep(1)

mail.logout()
print("Logged out of email:", email_user)