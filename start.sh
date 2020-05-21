chmod +x ./tools/crawlergo
chmod +x ./tools/xray/xray_linux_amd64 
nohup python3 server.py > logs/server.log 2>&1 &
nohup ./tools/xray/xray_linux_amd64 webscan --listen 127.0.0.1:7777 --webhook-output http://127.0.0.1:2333/webhook > logs/xray.log 2>&1 &
nohup python3 subdomain_monitor.py > logs/subdomain_monitor.log 2>&1 &