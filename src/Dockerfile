FROM jjanzic/docker-python3-opencv as builder


COPY . /src

RUN pip3 install --upgrade pip
RUN pip3 install --user -r /src/requirements.txt


#FROM python:3.8-slim as app
FROM jjanzic/docker-python3-opencv as app
COPY --from=builder /root/.local /root/.local
COPY --from=builder /src .

ENV PATH=/root/.local:$PATH
EXPOSE 80

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "-p 80"]