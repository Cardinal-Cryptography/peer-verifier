# Verifier
This script verifies signature provided by validators and also checks whether they are sending data to telemetry server. 

## Instalation
To use this script you first need to run selenium docker image, so that telemetry page can be explored. It can be run by:
```
docker run --rm -d --name selenium -p 4444:4444 --shm-size="2g" selenium/standalone-chrome:4.3.0-20220726
```
You also need to install the requirements from `requirements.txt`

## Runing
To verify validators you need a csv file which contains necessary data. Important columns are `peer_id,public_key,signed_message`. So for example:
```
full_name,peer_id,public_key,signed_message
John,Qm2j30wjd7qwvb345kdw8w032hcba7742hj4k6owwu10p3n4bbu2,Qm2j30wjd7qwvb345kdw8w032hcba7742hj4k6owwu10p3n4bbu3Qm2j30wjd7qwvb345kdw,Qm2j30wjd7qwvb345kdw8w032hcba7742hj4k6owwu10p3n4bbu3Qm2j30wjd7qwvb345kdw8w032hcba7742hj4k6owwu10p3n4bbu3p3n4bbu3p3n4bbu3p3n4bbu3
Paul,Qmhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhf,Qmhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhghghghghghghghghghr,QmhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfQmhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhghghghghghghghghghgffff
Second,Qmdsaerefdna32nQmdsaerefdna32nQmdsaerefdna32nQmdsaer,12h123ls8csh312h123ls8csh312h123ls8csh312h123ls8csh312h123ls8csh312h123l,Qmdsaerefdna32nQmdsaerefdna32nQmdsaerefdna32nQmdsaerQmdsaerefdna32nQmdsaerefdna32nQmdsaerefdna32nQmdsaerQmdsaerefdna32nQmdsaeref
```
After that you can run:
```
python3 ./selenium/verify.py --verifier <verifier> --validators-in <validators_in> --validators-out <validators_out>
```
Where 
- verifier is path to verifier program, that can be found in `peer-verifier/target/debug/verifier` if you compile `peer-verifier/src/verifier.rs`
- validators_in is a path to csv file containing the data
- validators_out is a path to where you want to save new csv file with results

After runing the script it should create a file with appended columns containing results for verification
```
full_name,peer_id,public_key,signed_message,result,result_name
Mateusz Pęczkowski,Qm2j30wjd7qwvb345kdw8w032hcba7742hj4k6owwu10p3n4bbu2,Qm2j30wjd7qwvb345kdw8w032hcba7742hj4k6owwu10p3n4bbu3Qm2j30wjd7qwvb345kdw,Qm2j30wjd7qwvb345kdw8w032hcba7742hj4k6owwu10p3n4bbu3Qm2j30wjd7qwvb345kdw8w032hcba7742hj4k6owwu10p3n4bbu3p3n4bbu3p3n4bbu3p3n4bbu3,1,wrong signature
Mateusz pupa,Qmhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhf,Qmhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhghghghghghghghghghr,QmhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfQmhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhfhghghghghghghghghghgffff,1,wrong signature
MyName,Qmdsaerefdna32nQmdsaerefdna32nQmdsaerefdna32nQmdsaer,12h123ls8csh312h123ls8csh312h123ls8csh312h123ls8csh312h123ls8csh312h123l,Qmdsaerefdna32nQmdsaerefdna32nQmdsaerefdna32nQmdsaerQmdsaerefdna32nQmdsaerefdna32nQmdsaerefdna32nQmdsaerQmdsaerefdna32nQmdsaeref,1,wrong signature
```
