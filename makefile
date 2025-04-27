default:
	@echo "Available actions: \n\
	    * make install        - create python virtual env, install requirements and create shortcut for service management\n\
	    * make docker_install - does the same as above, but in docker container \n\
	    * make clean          - delete __pycache__ dir, purge pip package cache and delete existing virtual env\n\
	    * make tests          - perform service.py tests command\n\
    \n\
	To install and deploy service:\n\
	   - create config.yaml file and modify it if needed.\n\
	Can be done with \"cp docs/config.sample.yaml config.yaml\" and then using your file editor of choice. \n\
	\"curl \"<your url here>\" > file.name\" is also a possibility \n\
	\n\
	   - use \"make install\" when ready, to create python environment and bashscript shortcut for easy service management.\n\
	See makefile contents for optional vars.\n\
	example how to pass options:\n\
	make install REQS_FILE=requirements/latest"

PYTHON_EXEC = python3
VENV_PATH = env
VENV_PYTHON_EXEC = ./$(VENV_PATH)/bin/python
REQS_FILE = requirements/latest

install:
	@echo "Creating python virtual environment..."
	$(PYTHON_EXEC) -m venv $(VENV_PATH)
	$(VENV_PYTHON_EXEC) -m pip install -r $(REQS_FILE)
	@echo "\nGenerating ruffles..."
	$(VENV_PYTHON_EXEC) service.py ruffles
	@echo "\nAll done!"

docker_install:
	@echo "installing dependencies..."
	$(PYTHON_EXEC) -m pip install -r $(REQS_FILE)
	@echo "\nAll done!"

docker_ruffles:
	@echo "\nGenerating ruffles..."
	$(PYTHON_EXEC) service.py ruffles

clean:
	rm -rf __pycache__

	@if $(VENV_PYTHON_EXEC) -m pip cache purge; then \
	    echo "purged pip cache"; \
	else \
	    echo "pip version is too old, has no \"cache purge\" command"; \
	fi
	rm -rf $(VENV_PATH)

tests::
	$(VENV_PYTHON_EXEC) service.py tests
