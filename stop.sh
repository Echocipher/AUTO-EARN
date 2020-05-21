ps -ef |grep python3 |awk '{print $2}'|xargs kill -9
ps -ef |grep xray |awk '{print $2}'|xargs kill -9
mv ./results/result.sqlite3 ./results/$(date "+%Y%m%d%H%M%S")_result.sqlite3
rm -rf ./tools/OneForAll/results/*