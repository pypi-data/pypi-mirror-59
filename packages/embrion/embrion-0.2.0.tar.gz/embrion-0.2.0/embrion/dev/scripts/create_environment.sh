#!/usr/bin/env zsh

env_name=$(cat environment.yml | grep -oP '^name:\s*\K(\S+)(?=\s*$)')

echo "-- New environment is being created --"

echo "-- Installing project environment --"
conda env create -f environment.yml -n $env_name
conda env update --name $env_name -f /embrion/dev/environment_extra.yml
cp environment.yml /tmp/environment.yml

echo "-- Done: Installing project environment --"

echo "-- Registering project environment --"
echo "conda activate $env_name" >> ~/.zshrc
echo "-- Done: Registering project environment --"

echo "-- Done: New environment is being created --"