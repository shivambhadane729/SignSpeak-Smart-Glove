
import asyncio
import edge_tts

async def main():
    voices = await edge_tts.list_voices()
    with open("all_voices.txt", "w", encoding="utf-8") as f:
        for v in voices:
            f.write(f"{v['ShortName']} - {v['FriendlyName']}\n")
    print("Voices written to all_voices.txt")

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
