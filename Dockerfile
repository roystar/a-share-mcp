# read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# you will also find guides on how best to write your Dockerfile

FROM python:3.9

# The two following lines are requirements for the Dev Mode to be functional
# Learn more about the Dev Mode at https://huggingface.co/dev-mode-explorers
RUN useradd -m -u 1000 user
WORKDIR /app
RUN chown -R user:user .

COPY . .
RUN pip install --upgrade pip
RUN pip install uv
RUN uv venv
RUN source .venv/bin/activate
RUN uv sync

ENV PYTHONPATH=/app:/app/src

CMD ["python", "src/mcp_server_tushare.py"]