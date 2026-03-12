import asyncio
from src.api.screening import generate_screening
from src.models.screening import ScreeningRequest

async def main():
    try:
        req = ScreeningRequest(modification_description="Replace the existing analog main steam line radiation monitors with digital transmitters in Turkey Point Unit 3.")
        res = await generate_screening(req)
        print(res)
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(main())
