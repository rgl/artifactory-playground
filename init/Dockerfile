# syntax=docker.io/docker/dockerfile:1.18

# see https://github.com/jfrog/jfrog-cli/releases
FROM releases-docker.jfrog.io/jfrog/jfrog-cli-v2-jf:2.78.9

RUN apk add --no-cache python3

CMD ["bash", "/init/init.sh"]
