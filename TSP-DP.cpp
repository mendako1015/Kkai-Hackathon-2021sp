#include <bits/stdc++.h>
using namespace std;

int main() {
	int n;
	cin >> n;
	vector<vector<int>> dist(n, vector<int>(n));
	for(int i = 0; i < n; i++) {
		for(int j = 0; j < n; j++) cin >> dist[i][j];
	}
	vector<vector<int>> dp(1<<n, vector<int>(n, 1e9));
	dp[0][0] = 0;
	for(int S = 0; S < (1 << n); S++) {
		for(int prev = 0; prev < n; prev++) {
			for(int now = 0; now < n; now++) {
				if((S & (1 << now)) == 0) {
					dp[S | (1 << now)][now] = min(dp[S | (1 << now)][now], dp[S][prev] + dist[prev][now]);
				}
			}
		}
	}
	cout << dp[(1 << n) - 1][0] << endl;
	return 0;
}