FROM alpine:latest

# Install required packages
RUN apk add --no-cache \
    docker-cli \
    docker-compose \
    bash \
    curl

# Create scheduler script
COPY scheduler.sh /scheduler.sh
RUN chmod +x /scheduler.sh

# Set timezone
ENV TZ=Europe/Stockholm

# Run scheduler
CMD ["/scheduler.sh"] 