#!/bin/sh

deploy_sandbox_web () {
  echo "Switching to sandbox web environment"
  eb use traansmission-sand-web
  echo "Deploying to sandbox web server"
  eb deploy
}

deploy_sandbox_worker () {
  echo "Switching to sandbox worker environment"
  eb use traansmission-sand-work
  echo "Deploying to sandbox worker"
  eb deploy
}

deploy_demo_web () {
  echo "Switching to demo web environment"
  eb use traansmission-demo-web
  echo "Deploying to demo web server"
  eb deploy
}

deploy_demo_worker () {
  echo "Switching to demo worker environment"
  eb use traansmission-demo-work
  echo "Deploying to demo worker"
  eb deploy
}

deploy_prod_web () {
  echo "Switching to prod web environment"
  eb use traansmission-prod-web
  echo "Deploying to prod web server"
  eb deploy
}

deploy_prod_worker () {
  echo "Switching to prod worker environment"
  eb use traansmission-prod-work
  echo "Deploying to prod worker"
  eb deploy
}

if [ $1 = "sandbox" ]; then
  if [ -z "$2" ]; then
    deploy_sandbox_web
    deploy_sandbox_worker
  elif [ $2 = "work" ]; then
    deploy_sandbox_worker
  elif [ $2 = "web" ]; then
    deploy_sandbox_web
  fi
fi
if [ $1 = "demo" ]; then
  if [ -z "$2" ]; then
    deploy_demo_web
    deploy_demo_worker
  elif [ $2 = "work" ]; then
    deploy_demo_worker
  elif [ $2 = "web" ]; then
    deploy_demo_web
  fi
fi
if [ $1 = "prod" ]; then
  echo "Are you sure you want to deploy to production? (type y for yes)"
  read answer
  if [ $answer = "y" ]; then
    if [ -z "$2" ]; then
      deploy_prod_web
      deploy_prod_worker
    elif [ $2 = "work" ]; then
      deploy_prod_worker
    elif [ $2 = "web" ]; then
      deploy_prod_web
    fi
  fi
fi


