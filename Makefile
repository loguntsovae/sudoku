# Makefile for Sudoku App

.PHONY: install-backend install-frontend start-backend start-frontend

install-backend:
	cd backend && uv sync

install-frontend:
	cd frontend && npm install

start-backend:
	cd backend && uvicorn main:app --reload --port 8004

start-frontend:
	cd frontend && npm start

install:
	make install-backend install-frontend

start:
	make start-backend start-frontend