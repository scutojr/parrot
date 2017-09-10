#!/usr/bin/env bash

HOME=`cd $(dirname $0)/..;pwd`

export  PYTHONPATH=$PYTHONPATH:$HOME

source $HOME/virtualenv/bin/activate
