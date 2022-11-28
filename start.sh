
RED='\033[1;31m'
GREEN='\033[1;32m'
LRED='\033[1;31m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
NC='\033[0m'

echo "Activating Python 3.10 Environment"
source ./bin/activate

echo "Installing dependencies >> "
pip install -r requirements.txt
clear 

echo "\n${CYAN}Initiating cloud watcher service !${NC}\n"
python cloud_watcher.py &
sleep 3

echo "\n${BLUE}Stopping any service at 8888${NC} \n"
lsof -i tcp:8888 
sleep 3

echo "${GREEN}Starting API Service...  !${NC}"
python server.py &
sleep 5

trap 'killall Python && echo "\n${RED}Stopping processes !${NC}\n" && exit'  INT
while true
echo "\n${LRED}To stop the server use ctrl + C${NC}"
do
   read -p "" INPUT
   if [[ $INPUT == [Ss]top ]]
   then
      break
   fi
done




