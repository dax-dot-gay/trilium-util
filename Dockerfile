FROM unit:python3.11
COPY dist /etc/trilium
COPY build-config/nginx.json /docker-entrypoint.d/
RUN /bin/bash -c "python -m pip install -r /etc/trilium/server/requirements.txt"
WORKDIR /etc/trilium/server
VOLUME /exports
RUN /bin/bash -c "chmod -R 777 /exports"