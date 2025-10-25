FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

# install dependencies
RUN npm install

# copy source code
COPY . .

# expose port
EXPOSE 5173

# start command
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]