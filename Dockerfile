FROM jgiannuzzi/gitolite

RUN apk add --update \
    python \
    py-pip \
 && rm -rf /var/cache/apk/*

WORKDIR /usr/src
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN ssh-keygen -q -t rsa -N "" -f /tmp/admin
ENTRYPOINT ["sh", "-c", "SSH_KEY=$(cat /tmp/admin.pub) /docker-entrypoint.sh $0 $@"]
