current_directory=`dirname "$0"`
python3 $current_directory/main.py $current_directory/email-sender.properties $*


#function send-cv(){
#        if [[ $# != 2 ]]
#        then  
#            echo "<email-to> <url to position>"  
#        fi
#        /home/projects/email-sender/email-sender.sh $1 $2                     
#}
