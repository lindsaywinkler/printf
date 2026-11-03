## Overview

printf = print farm. A sketch of a 3D print manufacturing execution system (MES) for a facility with a large number of resin printers.

This project includes database modelling for a number of relevant entities:

- printers
- resins
- parts
- jobs

## Components

Data models are developed in SQLModel, which acts both as an ORM
and does validation in Pydantic (a popular validation library in
Python).

Migrations are managed by Alembic.

The backend is FastAPI, with Strawberry for exposing a GraphQL
endpoint.

The application is containerised for simplicity. It is deployed
to a Kubernetes cluster in a very simple fashion - just exposing
relevant points, rather than properly configuring ingress.

## Development

This sketch is intentionally kept minimal. It is an exploration
of concepts and code, rather than forming the basis of
any production ready system..

It is built up by hand, rather than using any templated stack.  
It therefore lacks many expected features such as user management.

### Migrations

To generate: `uv run alembic revision --autogenerate -m ""`

## Running

Python dependencies are managed by `uv`.

Create a cluster locally with `kind create cluster`

Deploy Helm chart from `/deploy` directory with `helm install printf .`

To connect to the db with `psql` during development/debugging,
forward ports out with `kubectl port-forward svc/postgres 5432:5432`.

This port forwarding is necessary to run alembic:

Run alembic migrations with `uv run alembic upgrade head`
(Ideally there's a hook in the Helm chart to do this automatically)

Build backend docker imagen with `docker build -t printf-api:dev backend`

Docker image is just built locally so push it into the kind cluster
with `kind load docker-image printf-api:dev`

(Ideally the local dev setup uses watchers to do this automatically!)

And then we need to forward the ports: `kubectl port-forward svc/backend 8000:80`
(when actually running the application, we don't forward Postgres port!)
