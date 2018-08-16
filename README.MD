This is a test Selenium automation demo of SpinCar's 360 Manager platform. Test may be open and ran in an IDE like PyCharm as well.

The following Python modules are needed:

	pip
	virtualenv
	
	To install virtualenv, run: "python -m pip install virtualenv"
	
Create virtual environment and install dependencies:
	
	open a terminal and navigate to the root of the work folder
	run "python -m virtualenv venv"
	run "/venv/Scripts/activate"

	you should now be inside the virtual environment
	run "pip install -r requirements.txt"

Run automation test:

	navigate to "tests" folder
	run "pytest -v"

If an "import file mismatch" error occurs, run: "py.cleanup -p" and rerun test
	