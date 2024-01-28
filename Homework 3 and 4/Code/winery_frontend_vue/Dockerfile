# Use an official Node.js runtime as a parent image
FROM node:14

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install app dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Build the Vue.js app
RUN npm run build

# Expose the port that the app will run on
EXPOSE 8000

# Command to run the application
CMD ["npm", "start"]
