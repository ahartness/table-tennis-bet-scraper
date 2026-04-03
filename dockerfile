FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV TZ=EST5EDT
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN date

CMD ["python","-u","scripts/job.py"]
# Above was used for python docker deploy

#FROM node:18

#WORKDIR /app

#COPY package*.json ./

#RUN npm install

#COPY . .

#RUN npm run build

#EXPOSE 3000

#CMD ["node", ""]
