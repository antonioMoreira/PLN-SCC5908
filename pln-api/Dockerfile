# Other images:
#	1. nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04
#	2. nvidia/cuda:12.4.1-devel-ubuntu22.04

#FROM nvidia/cuda:12.2.2-base-ubuntu22.04
# FROM nvidia/cuda:12.1.0-devel-ubuntu22.04
FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

WORKDIR /usr/src/app
COPY . .

ENV IMAGEIO_FFMPEG_EXE=ffmpeg
# Pode ser melhor: ENV GOOGLE_APPLICATION_CREDENTIALS="$HOME/skylar-api-new/application_default_credentials.json"
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/mnt/filestore/venvs/skylar-api-ll-ub2204-py31109/lib/python3.11/site-packages/nvidia/cudnn/lib/
ENV LL_APP_HOME=/usr/src/app

ARG DEBIAN_FRONTEND=noninteractive

# sudo apt update && sudo apt install -y lsb-release build-essential ffmpeg wget gnupg software-properties-common git curl
RUN apt update && \
	apt upgrade -y && \
	apt install -y lsb-release build-essential ffmpeg gnupg software-properties-common curl git tmux nano nvtop && \
	add-apt-repository ppa:deadsnakes/ppa && \
	apt update && \
	apt install -y python3.11 python3.11-venv && \
	rm -rf /var/lib/apt/lists/*

# ------------ Google SDK --------------------------------------------
# Ref.: https://cloud.google.com/sdk/docs/install?hl=pt-br | "Dica do Docker. Se o comando 'apt-key' não for compatível"
#RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.asc] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | tee /usr/share/keyrings/cloud.google.asc && apt-get update -y && apt-get install google-cloud-sdk -y
# Para pegar o Application Default Credentials: $ gcloud auth application-default login
# --------------------------------------------------------------------

# Connection
ENV PORT=5678
EXPOSE 5678

# Can remove this ↓ if check whether or not filestore is mounted
# CMD ["/bin/sleep", "infinity"]