FROM rust:1.61 as builder
WORKDIR /usr/src/signer
COPY . .
RUN cargo install --path .

FROM ubuntu:focal-20210827
COPY --from=builder /usr/local/cargo/bin/signer /usr/local/bin/signer
COPY docker_entrypoint.sh /docker_entrypoint.sh
RUN chmod +x /docker_entrypoint.sh

ENTRYPOINT ["./docker_entrypoint.sh"]

