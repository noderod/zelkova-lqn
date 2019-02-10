FROM golang:1.11-alpine


COPY Makefile /cnode/Makefile
COPY cnode.go /cnode/cnode.go
COPY matrix_algebra /cnode/matrix_algebra.go



# Installs the necessary go libraries
RUN apk add --no-cache bash git curl make && go get github.com/gorilla/mux &&\
    go get github.com/influxdata/influxdb1-client/v2 && go get github.com/mongodb/mongo-go-driver/mongo &&\
    go get gonum.org/v1/gonum/mat





WORKDIR /cnode

