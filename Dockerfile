FROM ubuntu:focal-20210827

COPY target/release/signer /usr/local/bin
RUN chmod +x /usr/local/bin/signer

COPY docker_entrypoint.sh /docker_entrypoint.sh
RUN chmod +x /docker_entrypoint.sh

ENTRYPOINT ["./docker_entrypoint.sh"]