#include <bits/stdc++.h>
using namespace std;
typedef string::const_iterator State;
class ParseError {};

struct Parser {
    int number(State &begin) {
	    int ret = 0;
	    while(isdigit(*begin)) {
	    	ret *= 10;
	    	ret += *begin - '0';
	    	begin++;
	    }
	    return ret;
    }

    int factor(State &begin) {
	    if(*begin == '(') {
		    begin++;
		    int ret = expression(begin);
		    begin++;
            return ret;
	    } else {
		    return number(begin);
	    }
    }

    int term(State &begin) {
	    int ret = factor(begin);
	    while(1) {
	    	if(*begin == '*') {
	    		begin++;
	    		ret *= factor(begin);
	    	} else if(*begin == '/') {
                begin++;
	    		ret /= factor(begin);
	    	} else {
	    		break;
	    	}
    	}
    	return ret;
    }

    int expression(State &begin) {
	    int ret = term(begin);
	    while(1) {
	    	if(*begin == '+') {
		    	begin++;
		    	ret += term(begin);
	    	} else if(*begin == '-') {
	    		begin++;
		    	ret -= term(begin);
	    	} else {
	    		break;
	    	}
    	}
    	return ret;
    }
};

int main() {
    int N;
    cin >> N;
    for(int i = 0; i < N; i++) {
        Parser ps;
        string s;
        cin >> s;
        State begin = s.begin();
        int ans = ps.expression(begin);
        cout << ans << endl;
    }
    return 0;
}
