ENV_NAME = "archive"
ENV_FILE = "env_archive.yaml"

help :
	cat Makefile

install-develop : # sudo make install-develop
	npm i -g gitmoji-cli
	npm install git-br -g

git-aliases : # `git br` shows branchs descriptions `git root` prints the project root
	git config --global alias.br !git-br # git branch --edit-description
	git config --global alias.br-describe 'branch --edit-description'
	git config --global alias.root 'rev-parse --show-toplevel'

conda_env :
	conda env create --file "$(ENV_FILE)"

conda_env_rm :
	conda remove --name "$(ENV_NAME)" --all

hooks :
	# pre-commit install
	gitmoji -i

hooks-dry :
	pre-commit run --all-files

hooks-update :
	pre-commit autoupdate

style :
	isort ./
	black ./

test :
	pytest -m "not slow" --maxfail=3 ./

test-debug : # Depends on pip install pytest-ipdb
	pytest -m "not slow" --ipdb ./

test-coverage :
	pytest -m "not slow" -x --cov=./ ./

test-slow :
	time pytest -m "slow" -x ./

linter : # Finds debugging prints
	find ./gym_cellular_automata/ -type f -name "*.py" | sed '/test/ d' | xargs egrep -n 'print\(|ic\(' | cat
	mypy --config-file mypy.ini ./

clean : # Depends on trash-cli  https://github.com/andreafrancia/trash-cli
	find ./ -type d -name '__pycache__' | xargs -I{} trash {}
	find ./ -type d -name '*.egg-info' | xargs -I{} trash {}
	find ./ -type f -name '*~' | xargs -I{} trash {}
	find ./ -type f -name 'monkeytype.sqlite3' | xargs -I{} trash {}
	find ./ -type d -name '.pytest_cache' | xargs -I{} trash {}
	find ./ -type d -name '.mypy_cache' | xargs -I{} trash {}
	find ./ -name 'TMP*' | xargs -I{} trash {}
	git clean -d -n # To remove them change -n to -f
	echo "\n\nTo remove git untracked files run:\ngit clean -d -f"
