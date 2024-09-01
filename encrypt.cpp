#include "encrypt.hpp"

//Add salting+hashing
//Have it spit out garbage/no data if secret is wrong. Have processing time be as equivalent as possible.

std::string viginere_encrypt(std::string secret, std::string password){

    //Version of the viginere cipher - doesn't loop back around to characters. Generalised for any ascii symbol.
    std::string key = "";
    std::string encryptedSecret = "";

    //make key length equal to secret length
    while(key.length() < secret.length()){
        key+=password;
    }
    key = key.substr(0,secret.length());

    //Add ascii value of key[i] to secret[i] for encryptedSecret[i]
    for(int i=0;i<key.length();i++){
        encryptedSecret+= secret[i] + key[i];
    }
    
    return encryptedSecret;
}

std::string viginere_decrypt(std::string secret, std::string password){

    std::string key = "";
    std::string decryptedSecret = "";

    //make key length equal to secret length
    while(key.length() < secret.length()){
        key+=password;
    }
    key = key.substr(0,secret.length());

    //Add ascii value of key[i] to secret[i] for encryptedSecret[i]
    for(int i=0;i<key.length();i++){
        decryptedSecret+= secret[i] - key[i];
    }
    
    return decryptedSecret;
}
