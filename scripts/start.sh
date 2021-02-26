#!/usr/bin/env bash

nohup hy /app/algo_bot/run.hy > /app/prod.log 2>&1 &
echo $! > /app/bot.pid
