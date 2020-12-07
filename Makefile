default:
	./.venv/bin/python3 ./src/main.py

run:
	./.venv/bin/python3 ./src/main.py

trace:
	./.venv/bin/python3 ./src/main.py --trace

graph:
	./.venv/bin/python3 ./src/main.py --graph

par:
	rm ./output/out*.txt || echo "output is empty"
	time seq $N | parallel ./parallel/run_script.sh
	python3 ./parallel/find-best.py