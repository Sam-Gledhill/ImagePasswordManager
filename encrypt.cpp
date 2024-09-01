#include "encrypt.hpp"

//Add salting+hashing

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


int main(){

    std::string secret = "Hello world!";
    std::string password = "shush";
    std::string encrypted_secret = viginere_encrypt(secret,password);
    std::string decrypted_secret = viginere_decrypt(encrypted_secret,password);

    std::cout << secret << "\n" << encrypted_secret << "\n" << decrypted_secret << std::endl;

    return 0;
}