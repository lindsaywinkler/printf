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

## Running

Python dependencies are managed by `uv`.
