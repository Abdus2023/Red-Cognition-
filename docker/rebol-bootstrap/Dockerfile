FROM --platform=linux/386 i386/debian:bookworm-slim@sha256:75efd55b326373cf69989912388c0d50c5390638af7378d2fedc3aeb9d100e46
WORKDIR /red
ENV HOME=/root PATH=/opt/rebol:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates git libc6 libgcc-s1 libstdc++6 make python3 xvfb file libgdk-pixbuf-2.0-0 libgtk-3-0 libcurl4 && rm -rf /var/lib/apt/lists/*
COPY rebol /opt/rebol/rebol
RUN chmod 0755 /opt/rebol/rebol && file /opt/rebol/rebol
ENTRYPOINT ["/opt/rebol/rebol"]
