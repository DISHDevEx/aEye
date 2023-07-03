FROM public.ecr.aws/lambda/python:3.10

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt
RUN yum -y install mesa-libGL

COPY dist/aEye-0.0.1-py3-none-any.whl .
RUN pip3 install aEye-0.0.1-py3-none-any.whl --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]
