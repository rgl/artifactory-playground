# syntax=docker.io/docker/dockerfile:1.16

# see https://github.com/jfrog/jfrog-cli/releases
FROM releases-docker.jfrog.io/jfrog/jfrog-cli-v2-jf:2.76.1

RUN apk add --no-cache python3

CMD ["bash", "/init/init.sh"]
