default:
	./.venv/bin/python3 ./src/main.py

run:
	./.venv/bin/python3 ./src/main.py


par:
	rm ./output/out*.txt
	time seq $N | parallel ./parallel/run_script.sh
	python3 ./parallel/find-best.py