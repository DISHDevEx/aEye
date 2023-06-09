FROM public.ecr.aws/lambda/python:3.10
#COPY --from=make-pthread-nameshim /pthread-nameshim/pthread_shim.so /opt/pthread_shim.so

COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt
RUN yum install -y mesa-libGLw

COPY dist/aEye-0.0.1-py3-none-any.whl .
RUN pip3 install aEye-0.0.1-py3-none-any.whl --target "${LAMBDA_TASK_ROOT}"
RUN static_ffmpeg_paths
ADD https://storage.googleapis.com/mediapipe-models/object_detector/efficientdet_lite0/int8/latest/efficientdet_lite0.tflite /var/task/efficientdet_lite0.tflite

RUN chmod a+rx /var/task/*.tflite

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]
