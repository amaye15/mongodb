# Use the official MongoDB image from Docker Hub
FROM mongo:latest

# The two following lines are requirements for the Dev Mode to be functional
RUN useradd -m -u 1000 user
WORKDIR /app

# Copy the MongoDB configuration file if you have specific configurations
# Uncomment the next line if you want to use a custom MongoDB configuration
# COPY --chown=user ./mongod.conf /etc/mongod.conf

# Expose the MongoDB port
EXPOSE 80

# Switch to the "user" user
USER user

# Set environment variables if needed, for example:
# ENV MONGO_INITDB_ROOT_USERNAME=admin
# ENV MONGO_INITDB_ROOT_PASSWORD=yourpassword

# Start MongoDB with a command to bind to all IP addresses
CMD ["mongod", "--bind_ip_all"]

# Use the official MongoDB image
FROM mongo:latest

# Create a non-root user
RUN useradd -m -u 1000 user
WORKDIR /app

# Create a new data directory with appropriate permissions
RUN mkdir -p /app/data/db && chown -R user:user /app/data/db

# Expose the default MongoDB port
EXPOSE 80

# Switch to the non-root user
USER user

# Environment variables for initializing the root user
ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD=yourpassword

# Start MongoDB with a custom data directory
CMD ["mongod", "--dbpath", "/app/data/db", "--bind_ip_all"]



