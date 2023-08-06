#!/usr/bin/env zsh

if [ ! -f environment.yml ]; then
    echo "Please run embrion init or manually create an environment.yml"
else
    if cmp -s environment.yml /tmp/environment.yml ; then
        echo "Already up to date."
    else
        env_name=$(cat environment.yml | grep -oP '^name:\s*\K(\S+)(?=\s*$)')

        if [ -s /tmp/environment.yml ]; then
            old_env_name=$(cat /tmp/environment.yml | grep -oP '^name:\s*\K(\S+)(?=\s*$)')

            if [ "$env_name" = "$old_env_name" ]; then
                zsh /embrion/dev/scripts/update_environment.sh
            else
                zsh /embrion/dev/scripts/remove_environment.sh
                zsh /embrion/dev/scripts/create_environment.sh
            fi
        else
            zsh /embrion/dev/scripts/create_environment.sh
        fi
    fi
fi
