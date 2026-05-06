# syntax=docker.io/docker/dockerfile:1.23

# see https://github.com/jfrog/jfrog-cli/releases
FROM releases-docker.jfrog.io/jfrog/jfrog-cli-v2-jf:2.103.0

RUN apk add --no-cache python3

CMD ["bash", "/init/init.sh"]
