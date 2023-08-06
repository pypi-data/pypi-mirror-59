#!/usr/bin/env zsh

old_env_name=$(cat /tmp/environment.yml | grep -oP '^name:\s*\K(\S+)(?=\s*$)')

echo "-- Removing old project environment --"
conda env remove --name $old_env_name
echo "-- Done: Removing project environment --"
sed -i -e "s/conda activate $old_env_name//g" ~/.zshrc
