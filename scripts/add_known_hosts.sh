
#!/bin/bash

set -e


echo "Waiting for all the ssh keyscan to complete"
for manager in $(seq 0 $((MANAGER_COUNT-1)));
do	
	MGR=MANAGER_$((manager+1))
	ssh-keyscan -H ${!MGR} >> ~/.ssh/known_hosts

done

echo "ssh key scan complete"