FROM golang:1.11-alpine




# Installs the necessary go libraries
RUN apk add --no-cache bash git curl && go get github.com/gorilla/mux &&\
    go get github.com/influxdata/influxdb1-client/v2 && go get github.com/mongodb/mongo-go-driver/mongo





WORKDIR /cnode

