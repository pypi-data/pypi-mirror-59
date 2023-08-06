#!/usr/bin/env zsh

env_name=$(cat environment.yml | grep -oP '^name:\s*\K(\S+)(?=\s*$)')

echo "-- Updating old project environment --"
# There is a bug in conda that prune does not delete the packages.
# Just adding extra environment in case it starts working.
conda env update --prune --name $env_name environment.yml
conda env update --name $env_name -f /embrion/dev/environment_extra.yml
cp environment.yml /tmp/environment.yml

echo "-- Updating old project environment --"
