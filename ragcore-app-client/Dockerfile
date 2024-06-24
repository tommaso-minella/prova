# Use Node.js version 20 as the build stage base image
# This stage is called 'build-stage'
FROM node:20 as build-stage

# Set the working directory to /app in the build stage
WORKDIR /app

# Copy the package.json and package-lock.json files to the working directory
# This step is isolated to leverage Docker's caching mechanism,
# ensuring that subsequent Docker image builds are faster
COPY package*.json ./

# Install the dependencies specified in package-lock.json
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Build the React application
# The output will be stored in the 'build' directory
RUN npm run build

# Use Nginx alpine image as the production stage base image
FROM nginx:alpine

# Copy the build output from the build-stage to the default Nginx
# public directory where Nginx serves static files from
COPY --from=build-stage /app/build /usr/share/nginx/html

# Expose port 80 to allow traffic to the application
EXPOSE 80

# Start Nginx and keep it running in the foreground
CMD ["nginx", "-g", "daemon off;"]