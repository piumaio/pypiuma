
clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf

test: clean
  @flake8 pypiuma
	@pytest --cov pypiuma -s --cov-report term-missing
