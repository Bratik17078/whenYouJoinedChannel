import os
import asyncio
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.errors import PeerIdInvalid, UserNotParticipant, UsernameInvalid
from pathlib import Path

load_dotenv()

# Configuration
CACHE_FOLDER = Path(".cache")
SESSIONS_FOLDER = CACHE_FOLDER / "sessions"
os.makedirs(CACHE_FOLDER, exist_ok=True)
os.makedirs(SESSIONS_FOLDER, exist_ok=True)

# found at https://my.telegram.org/
API_ID = YOUR_API_ID
API_HASH = "YOUR_API_HASH"

async def GetJoinDate(session_name):
    app = Client(
        name=session_name,
        api_id=API_ID,
        api_hash=API_HASH,
        workdir=str(SESSIONS_FOLDER)
    )

    async with app:
        print(f"Logged in as: {(await app.get_me()).first_name}")
        
        while True:
            print("\n" + "="*40)
            target = input("Enter Channel ID (e.g., -100123...) or Username (without @):\nType 'exit' to quit: ").strip()
            
            if target.lower() == 'exit':
                break

            try:
                chat_identifier = int(target)
            except ValueError:
                chat_identifier = target

            try:
                print(f"Checking join date for: {chat_identifier}...")
                
                member = await app.get_chat_member(chat_identifier, "me")
                
                if member.joined_date:
                    formatted_date = member.joined_date.strftime("%B %d, %Y at %H:%M:%S")
                    print(f"\nYou joined this channel on: {formatted_date}")
                else:
                    print("\nCould not find a join date. (You might be the owner/creator, or it's too old).")
                    
            except UserNotParticipant:
                print("Error: You are not a member of this channel.")
            except (PeerIdInvalid, UsernameInvalid):
                print("Error: Invalid Channel ID or Username.")
            except Exception as e:
                print(f"Unexpected Error: {e}")

def main():
    print("Please enter a session name:")
    input_name = input().strip()
    session_name = input_name if input_name else "hehe"

    try:
        asyncio.run(GetJoinDate(session_name))
    except KeyboardInterrupt:
        print("\nOperation cancelled.")

if __name__ == "__main__":
    main()