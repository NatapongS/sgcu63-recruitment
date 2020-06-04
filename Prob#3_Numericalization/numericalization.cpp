#include <iostream>
#include <vector>
#include <string>

using namespace std;
struct numberString{
	private:
		int height;
		int width;
		int numberRef;
		char ** printableNumber;
		const string digit[10] = {"1110111", "0010010", "1011101", "1011011", "0111010", "1101011", "1101111", "1010010", "1111111", "1111011"};
		/*  digit is represented as lines that are drawn.
		 	00000
			1   2
			1   2
			33333
			4   5
			4   5
			66666
			Ps. The top-left corner is both 0's and 1's area, same goes for other corners:
			top-left = 0 and 1
			top-right = 1 and 2
			center-left = 1(upper center area) and 3 and 4(lower center area)
			center-right = 2(upper center area ) and 3 and 5(lower center area)
			bottom-left = 4 and 6
			bottom-right = 5 and 6
		*/
		void drawLine(int position){
			char num = '0' + numberRef;
			int x_1, y_1, x_2, y_2; //we will draw from (x_1, y_1) to (x_2, y_2)
			if(position == 0 || position == 3 || position == 6){
				x_1 = 0;
				x_2 = 5 * width - 1;
			}
			else if(position == 1 || position == 4){
				x_1 = 0;
				x_2 = width - 1;
			}
			else{
				x_1 = 4 *width;
				x_2 = 5  * width - 1;
			}
			if(position == 0){
				y_1 = 0;
				y_2 = height - 1;
			}
			else if(position == 3){
				y_1 = 2 * height;
				y_2 = 3 * height - 1;
			}
			else if(position == 6){
				y_1 = 4 * height;
				y_2 = 5 * height - 1;
			}
			else if(position == 1 || position == 2){
				y_1 = 0;
				y_2 = (5 * height - 1) / 2;
			}
			else {
				y_1 = 5 * height / 2;
				y_2 = 5 * height - 1;
			}
			for(int i = y_1; i <= y_2; i++){
				for(int j = x_1; j <= x_2;j ++){
					printableNumber[i][j] = num;
				}
			}

		}
	public:
		numberString(int numberRef, int height, int width){
			this -> height = height;
			this -> width = width;
			this -> numberRef = numberRef;
			printableNumber = new char*[5 * height];
			for(int i = 0; i < 5 * height; i++){
				printableNumber[i] = new char[5 * width + 1];
				for(int j = 0; j < 5 * width; j++){
					printableNumber[i][j] = ' ';

				}
				printableNumber[i][5 * width] = '\0';
			}
			for(int i = 0; i < 7; i++){
				if(digit[numberRef][i] == '1'){
					drawLine(i);
				}
			}
		}
		void printLine(int line){
			cout << printableNumber[line];
		}


};
int main(){
	
	string numberToConvert;
	int height, width;
	cin >> numberToConvert >> height >> width;
	vector<numberString> allNumber;
	for(int i = 0; i < numberToConvert.length(); i++){
		int numberRef = numberToConvert[i] - '0';
		allNumber.push_back(*(new numberString(numberRef, height, width)));
	}
	string space = "";
	for(int i = 0; i < width; i++) 
		space += " ";
	for(int i = 0; i < 5 * height; i++){
		for(auto number: allNumber){
			number.printLine(i);
			cout << space;
		}
		cout << '\n';
	}

}