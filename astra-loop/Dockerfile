# Astra Loop runtime image — drop-in for mattermost-team-edition with Postgres.
# Build with: ./astra-loop/build.sh
# Or: docker build -f astra-loop/Dockerfile --build-arg MM_PACKAGE=file:///mattermost-team-linux-amd64.tar.gz -t astra-loop:dev .

ARG BASE_BUILDER=ubuntu:noble-20251013@sha256:c35e29c9450151419d9448b0fd75374fec4fff364a27f176fb458d472dfc9e54

FROM ${BASE_BUILDER} AS builder
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG PUID=2000
ARG PGID=2000
# Local package produced by astra-loop/build.sh (copied into build context as mattermost-team-linux-amd64.tar.gz)
ARG MM_PACKAGE=mattermost-team-linux-amd64.tar.gz

RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
  ca-certificates \
  curl \
  media-types \
  mailcap \
  unrtf \
  wv \
  poppler-utils \
  tidy \
  tzdata \
  && rm -rf /var/lib/apt/lists/*

COPY ${MM_PACKAGE} /tmp/mattermost-package.tar.gz

RUN mkdir -p /mattermost/data /mattermost/plugins /mattermost/client/plugins \
  && groupadd --gid ${PGID} mattermost \
  && useradd --uid ${PUID} --gid ${PGID} --comment "" --home-dir /mattermost mattermost \
  && tar -xzf /tmp/mattermost-package.tar.gz -C / \
  && rm /tmp/mattermost-package.tar.gz \
  && chown -R mattermost:mattermost /mattermost /mattermost/data /mattermost/plugins /mattermost/client/plugins \
  && mkdir -p /mattermost/.postgresql \
  && chmod 700 /mattermost/.postgresql

FROM gcr.io/distroless/base-debian12

ENV PATH="/mattermost/bin:${PATH}"
ENV MM_SERVICESETTINGS_ENABLELOCALMODE="true"
ENV MM_INSTALL_TYPE="docker"
ENV MM_TEAMSETTINGS_SITENAME="Astra Loop"

COPY --from=builder /etc/mime.types /etc
COPY --from=builder --chown=2000:2000 /etc/ssl/certs /etc/ssl/certs
COPY --from=builder /usr/bin/pdftotext /usr/bin/pdftotext
COPY --from=builder /usr/bin/wvText /usr/bin/wvText
COPY --from=builder /usr/bin/wvWare /usr/bin/wvWare
COPY --from=builder /usr/bin/unrtf /usr/bin/unrtf
COPY --from=builder /usr/bin/tidy /usr/bin/tidy
COPY --from=builder /usr/share/wv /usr/share/wv
COPY --from=builder /usr/lib/libpoppler.so* /usr/lib/
COPY --from=builder /usr/lib/libfreetype.so* /usr/lib/
COPY --from=builder /usr/lib/libpng.so* /usr/lib/
COPY --from=builder /usr/lib/libwv.so* /usr/lib/
COPY --from=builder /usr/lib/libtidy.so* /usr/lib/
COPY --from=builder /usr/lib/libfontconfig.so* /usr/lib/
COPY --from=builder --chown=2000:2000 /mattermost /mattermost
COPY passwd /etc/passwd

USER mattermost

HEALTHCHECK --interval=30s --timeout=10s \
  CMD ["/mattermost/bin/mmctl", "system", "status", "--local"]

WORKDIR /mattermost
CMD ["/mattermost/bin/mattermost"]

EXPOSE 8065 8067 8074
VOLUME ["/mattermost/data", "/mattermost/logs", "/mattermost/config", "/mattermost/plugins", "/mattermost/client/plugins"]
