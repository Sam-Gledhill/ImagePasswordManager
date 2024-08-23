#include <iostream>
#include <fstream>
#include <string>

// Use opencv to do image handling

std::string read_file(std::string filename)
{
    std::string s = "";
    std::ifstream in(filename, std::ios::binary);
    char c;
    while (in)
    {
        in.get(c);
        if (in)
        {
            s += int(c);
        }
    }
    in.close();
    return s;
}

void write_file(std::string filename, std::string data)
{
    std::ofstream out(filename);
    out << data;
    out.close();
}

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        return 0;
    }

    std::string main_file = read_file(argv[1]);
    std::string secret_file = read_file(argv[2]);

    size_t secret_position = 10000;
    main_file.replace(secret_position, 3, "Hello World!");
    std::string embedded_filename = "output.png";
    write_file(embedded_filename, main_file);

    return 0;
}