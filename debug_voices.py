
import asyncio
import edge_tts

async def main():
    voices = await edge_tts.list_voices()
    print(f"Found {len(voices)} voices.")
    
    print("\n--- Punjabi Voices ---")
    found = False
    for v in voices:
        if "pa-" in v["ShortName"] or "Punjabi" in v["FriendlyName"]:
            print(f"{v['ShortName']} - {v['Gender']}")
            found = True
    if not found:
        print("No Punjabi voices found.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
