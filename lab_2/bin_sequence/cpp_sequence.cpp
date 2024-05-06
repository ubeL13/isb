#include <iostream>
#include <bitset>
#include <cstdlib>
#include <ctime>
using namespace std;

int main() {
    srand(static_cast<unsigned int>(time(0)));
    bitset<128> binary_sequence;
    for (int i = 0; i < 128; ++i) {
        bool random_bit = rand() % 2;
        binary_sequence[i] = random_bit;
    }
    cout << "Random Binary Sequence: " << binary_sequence << endl;
    return 0;
}
