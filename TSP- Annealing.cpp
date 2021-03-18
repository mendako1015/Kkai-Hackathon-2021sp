#include <bits/stdc++.h>
using namespace std;

int n;
vector<vector<int>> dist(1010, vector<int>(1010));

int score(vector<int> route) {
	int now = 0;
	int all_dist = 0;
	for(int v : route) {
		all_dist += dist[now][v];
		now = v;
	}
	all_dist += dist[now][0];
	return all_dist;
}

int main() {
	cin >> n;
	for(int i = 0; i < n; i++) {
		for(int j = 0; j < n; j++) cin >> dist[i][j];
	}

	int best_dist = 1e9;
	vector<int> r;
	for(int i = 1; i < n; i++) r.push_back(i);
	while(true) {
		int u = rand() % (n - 1);
		int v = rand() % (n - 1);
		swap(r[u], r[v]);
		int changed_dist = score(r);
		if(best_dist > changed_dist) {
			best_dist = changed_dist;
			cout << best_dist << endl;
			for(int x : r) cout << x << " ";
			cout << endl;
		}
		if(best_dist <= changed_dist && rand() % 20) swap(r[u], r[v]);
	}
	return 0;
}
