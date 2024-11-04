runS:
	uvicorn server.src.main:app --reload

runC:
	cd client && npm run dev
