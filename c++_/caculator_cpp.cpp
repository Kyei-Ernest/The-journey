#include <iostream>

using namespace std;

int main(){
    string positions[7] = {"first","second","third","fourth","fifth","sixth","other"};
    int calc_numbers[100];
    int operator_choice;
    int sum,subtraction,division,multiplication;
    string number;

    cout << "What operation would you like to perform?"<<endl;
    cout << "1. Addition"<< endl;
    cout << "2. Subtraction"<<endl;
    cout << "3. Division"<< endl;
    cout << "4. Multiplication"<<endl;
    cin >> operator_choice;
    cout<< "Enter number and press enter"<<endl;
    cout<<" AFTER ENTERING YOUR PREFERED NUMBERS ENTER '=' IN THE NEXT REQUEST  AND PRESS ENTER"<<endl;
    cout<< "IF you want to exit at any point type 'c'and press enter"<<endl;
    int i = 0;
    int array_length;

    //Allow operator to accept n numbers until user enters = for final result or press c to cancel.
    while (true){
        cout << "Enter "<<positions[i]<< "number: "<<endl;
        cin >>number;
        if (number == "c"){
        break;
        }
        else if(number == "="){
                sum = 0;
                division = 0;
                multiplication = 1;

                    if (operator_choice == 1) {
                            for (int j = i - 1; j >= 0; j--) {
                    sum += calc_numbers[j];  // Accumulate sum

                     }cout << sum << endl;
                     break;
                    }

                    else if (operator_choice == 2) {
                                subtraction = calc_numbers[0];
                                for (int j = i-1; j > 0; j--) {
                                subtraction -= calc_numbers[j];
                            }cout << subtraction << endl;
                            break;
                    }
                    else if (operator_choice == 3) {
                                division = calc_numbers[0];
                                for (int j = i-1; j > 0; j--) {
                                division /= calc_numbers[j];
                            }cout << division << endl;
                                break;
                    }
                    else if (operator_choice == 4) {
                        for (int j = i - 1; j >= 0; j--) {
                                multiplication *= calc_numbers[j];
                                }cout << multiplication << endl;
                                break;
                    }}
            else{
                    calc_numbers[i] = stoi(number);
                    if (positions[i]!="other"){
                    i++;}
            }
    }

    return 0;
}

