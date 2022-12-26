# OpenShift deployment
```sh
oc new-app --list
oc new-app --search python
```

```sh
GIT_REPO=https://github.com/cherkavi/python-deployment
# app.py, requirements.txt - must be present
GIT_BRANCH=main
APP_NAME=python-test
oc new-app --code "${GIT_REPO}#${GIT_BRANCH}" --name $APP_NAME
# OCP_BASE_IMAGE=python:3.8-ubi8 
# oc new-app --code "${GIT_REPO}#${GIT_BRANCH}" --name $APP_NAME --docker-image $OCP_BASE_IMAGE

## todo
# source to image 
# https://github.com/openshift/source-to-image/releases/tag/v1.3.2
# s2i build . $DOCKER_IMAGE python-test-app --pull-policy never
```