#
# Specio Service
#
# Specio is a VeriPy wrapper with extra tooling to allow it to monitor for jobs.
# As such, the container will be setup very much like VeriPy would normally
# be installed, and additional utilities will be installed into the environemnt
# to allow the management of jobs to process.
#

FROM python:3.6 AS base

# Install VeriPy
RUN pip install git+https://github.com/Codebiosys/veripy.git@v0.1.0#egg=veripy

# Install PyDF and a special version of weasyprint
RUN pip install git+https://41125aab2214caa4fab5be0cb5dddb5fa96739a9:@github.com/Codebiosys/pydf.git@master#egg=pydf && \
    pip install --ignore-installed git+https://github.com/Kozea/WeasyPrint@56904ba#egg=weasyprint

# Install veripy2specio
RUN pip install git+https://41125aab2214caa4fab5be0cb5dddb5fa96739a9:@github.com/Codebiosys/veripy2specio.git@master#egg=veripy2specio

# Install dom2fixture
RUN pip install git+https://41125aab2214caa4fab5be0cb5dddb5fa96739a9:@github.com/Codebiosys/dom2fixture.git@master#egg=dom2fixture

# Do not buffer Python output
ENV PYTHONUNBUFFERED=0

#
# Development multi-stage target
#
FROM base AS development

# Copy source code last so it can be mounted in Compose
# For development, each individual tool's requirements files must be copied
# individually to install the dependencies first. Afterwards, we can install
# the actual Python module so that the dependencies are not re-installed on
# Python file changes (in case the developer decides to mount the modules
# for development).
COPY ./forrest/requirements* /install/forrest/
RUN pip install -r /install/forrest/requirements-development.txt

COPY . /install/
RUN pip install -e /install/forrest

# Setup filesytem to what VeriPy expects
# All module directories will be at /app/veripy/*
WORKDIR /app

COPY logging.yml .
COPY entrypoint .
CMD ["./entrypoint"]


#
# Production multi-stage target
#
FROM base AS production

# Copy and install immediately, there won't be file changes in production
COPY . /install/
RUN pip install /install/forrest

# Setup filesytem to what VeriPy expects
# All module directories will be at /app/veripy/*
WORKDIR /app

COPY entrypoint .
CMD ["./entrypoint"]
