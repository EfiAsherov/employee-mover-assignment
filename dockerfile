FROM python:latest
WORKDIR /At-Bay-Assignment
copy . .
RUN pip install -r requirements.txt
CMD ["python", "main.py", "test_input", "out.xlsx", "expected_results", "1", "0"]