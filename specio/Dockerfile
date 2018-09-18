#
# Specio Service
#
# Specio is a VeriPy wrapper with extra tooling to allow it to monitor for jobs.
# As such, the container will be setup very much like VeriPy would normally
# be installed, and additional utilities will be installed into the environemnt
# to allow the management of jobs to process.
#

FROM python:3.6 AS base

# Install VeriPy dependencies first to cache them away
RUN mkdir /install && \
    cd /install && \
    git clone https://github.com/Codebiosys/veripy.git && \
    pip install -r ./veripy/requirements.txt

# Install PyDF
RUN cd /install && \
    git clone https://41125aab2214caa4fab5be0cb5dddb5fa96739a9:@github.com/Codebiosys/pydf.git && \
    pip install ./pydf

# Setup filesytem to what VeriPy expects
# All module directories will be at /app/veripy/*
WORKDIR /app
RUN mv /install/veripy/veripy .

#
# Development multi-stage target
#
FROM base AS development

# Install additional dependencies testing dependencies
RUN pip install -r /install/veripy/requirements-development.txt

# Copy source code last so it can be mounted in Compose
# For development, each individual tool's requirements files must be copied
# individually to install the dependencies first. Afterwards, we can install
# the actual Python module so that the dependencies are not re-installed on
# Python file changes (in case the developer decides to mount the modules
# for development).
COPY ./dom2fixture/requirements* /install/dom2fixture/
COPY ./veripy2specio/requirements* /install/veripy2specio/
COPY ./run/requirements* /install/run/
RUN pip install -r /install/dom2fixture/requirements-development.txt && \
    pip install -r /install/veripy2specio/requirements-development.txt && \
    pip install -r /install/run/requirements-development.txt

COPY . /install/
RUN pip install -e /install/dom2fixture && \
    pip install -e /install/veripy2specio && \
    pip install -e /install/run

COPY logging.yml .
COPY entrypoint .
CMD ["entrypoint"]


#
# Production multi-stage target
#
FROM base AS production

# Copy and install immediately, there won't be file changes in production
COPY . /install/
RUN pip install /install/dom2fixture && \
    pip install /install/veripy2specio && \
    pip install /install/run

COPY entrypoint .
CMD ["entrypoint"]
