# Astra Loop runtime image — drop-in for mattermost-team-edition with Postgres.
# Build with: ./astra-loop/build.sh
#
# Uses Ubuntu (not distroless) so document-processing shared libraries resolve
# reliably across Noble package layouts.

FROM ubuntu:noble-20251013@sha256:c35e29c9450151419d9448b0fd75374fec4fff364a27f176fb458d472dfc9e54
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG PUID=2000
ARG PGID=2000
ARG MM_PACKAGE=mattermost-team-linux-amd64.tar.gz

ENV PATH="/mattermost/bin:${PATH}"
ENV MM_SERVICESETTINGS_ENABLELOCALMODE="true"
ENV MM_INSTALL_TYPE="docker"
ENV MM_TEAMSETTINGS_SITENAME="Astra Loop"
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
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

RUN mkdir -p /mattermost/data /mattermost/plugins /mattermost/client/plugins /mattermost/logs /mattermost/config \
  && (getent group ${PGID} >/dev/null || groupadd --gid ${PGID} mattermost) \
  && (id -u ${PUID} >/dev/null 2>&1 || useradd --uid ${PUID} --gid ${PGID} --comment "" --home-dir /mattermost mattermost) \
  && tar -xzf /tmp/mattermost-package.tar.gz -C / \
  && rm /tmp/mattermost-package.tar.gz \
  && chown -R ${PUID}:${PGID} /mattermost \
  && mkdir -p /mattermost/.postgresql \
  && chmod 700 /mattermost/.postgresql

USER ${PUID}:${PGID}
WORKDIR /mattermost

HEALTHCHECK --interval=30s --timeout=10s \
  CMD ["/mattermost/bin/mmctl", "system", "status", "--local"]

CMD ["/mattermost/bin/mattermost"]

EXPOSE 8065 8067 8074
VOLUME ["/mattermost/data", "/mattermost/logs", "/mattermost/config", "/mattermost/plugins", "/mattermost/client/plugins"]
