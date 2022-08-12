ver='target/debug/verifier'
val_in='validators.csv'
val_out='validators_out.csv'

if [ ! $(docker ps --format '{{.Names}}' | grep -w selenium &> /dev/null) ] 
then
    docker run --rm -d --name selenium -p 4444:4444 --shm-size="2g" selenium/standalone-chrome:4.3.0-20220726
    sleep 5
fi

python3 ./selenium/verify.py --verifier $ver --validators-in $val_in --validators-out $val_out