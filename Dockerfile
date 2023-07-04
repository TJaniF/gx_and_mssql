FROM --platform=linux/amd64 quay.io/astronomer/astro-runtime:8.6.0

# Install dependencies required for the ODBC driver
USER root
RUN apt-get update && apt-get install -y curl gnupg2

# Install the ODBC driver and related packages
RUN apt-get install -y unixodbc unixodbc-dev

# Download and install the Microsoft ODBC driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Install SQL Server Native Client 11.0
RUN apt-get install -y libssl1.1 libssl-dev

# Clean up
RUN apt-get autoremove -y && apt-get clean

USER astro
