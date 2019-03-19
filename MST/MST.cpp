#include <iostream>
#include <vector>
#include <cmath>
#include <stack>
#include <fstream>

struct Point {
	long double x, y;
	long double distTo(const Point& other_point) {
		return std::sqrt((this->x - other_point.x)*(this->x - other_point.x)
			+ (this->y - other_point.y)*(this->y - other_point.y)
		);
	}
};


std::vector<std::pair<int, int> > find_mst(std::vector<Point> &graph) {
	std::vector<std::pair<int, int > > mst;
	std::vector<bool> used(graph.size(), false);
	std::vector<int> parent(graph.size(), -1);
	std::vector<long double> min_dist(graph.size(), INFINITY);

	min_dist[0] = 0;
	for (int i = 0; i < (int)graph.size(); i++) {
		int cur_min_dist = -1;
		for (int j = 0; j < (int)graph.size(); j++) {
			if (!used[j] && (cur_min_dist == -1 || (min_dist[j] < min_dist[cur_min_dist]))) {
				cur_min_dist = j;
			}
		}
		used[cur_min_dist] = true;

		if (parent[cur_min_dist] != -1) {
			mst.push_back({ parent[cur_min_dist], cur_min_dist });
		}

		for (int j = 0; j < (int)graph.size(); j++) {
			if (graph[cur_min_dist].distTo(graph[j]) < min_dist[j]) {
				min_dist[j] = graph[cur_min_dist].distTo(graph[j]);
				parent[j] = cur_min_dist;
			}
		}

	}
	return mst;
}

void find_Euler_cycle(std::vector <std::vector<int> > &graph, std::vector <int> &ans) {
	std::stack<int> s;
	s.push(0);
	ans.clear();
	while (!s.empty()) {
		int cur = s.top();
		if (!graph[cur].empty()) {
			s.push(graph[cur].back());
			graph[cur].pop_back();
		}
		if (s.top() == cur) {
			ans.push_back(cur);
			s.pop();
		}
	}
	return;
}


int main(int argc, char *argv[])
{
	std::ifstream in(argv[1]);
	std::ofstream out(argv[2]);

	std::vector <Point> graph;
	int points;
	in >> points;
	for (int i = 0; i < points; i++) {
		Point new_point;
		in >> new_point.x >> new_point.y;
		graph.push_back(new_point);
	}

	auto mst_edges = find_mst(graph);

	std::vector<std::vector<int> > mst(graph.size());
	for (auto i : mst_edges) {
		mst[i.first].push_back(i.second);
		mst[i.second].push_back(i.first);
	}

	std::vector <int> ans;
	find_Euler_cycle(mst, ans);

	std::vector<bool> used(graph.size(), false);
	for (auto i : ans) {
		if (!used[i]) {
			out << i + 1 << ' ';
			used[i] = true;
		}
	}
	out << std::endl;
}


