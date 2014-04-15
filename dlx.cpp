#include<iostream>
#include<vector>
#include<limits>

using namespace std;

struct Node{
	uint num, col_size;
	Node *up, *down, *left, *right, *col_header;

	Node() {
		up = down = left = right = this;
	}
};

void initialize_col_headers(int C, Node* h){
	for(int c=0;c<C;c++){
		Node *curr = new Node();
		curr->right = h;
		curr->left = h->left;
		h->left->right = curr;
		h->left = curr;
		curr->col_size = 0;
		curr->num = c;
		curr->col_header = curr;
	}
}

Node *read_graph(){
	int R, C;
	cin >> R >> C;
	Node *h = new Node();
	initialize_col_headers(C, h);
	int curr;
	Node *col;
	Node *row = NULL;
	for(int r=0;r<R;r++){
		col = h->right;
		// printf("%02d : ", r);
		for(int c=0;c<C;c++){
			cin>>curr;
			if(curr){
				// cout << "1";
				Node* new_node = new Node();
				new_node->col_header = col;
				new_node->num = r;
				new_node->up = col->up;
				new_node->down = col;
				col->up->down = new_node;
				col->up = new_node;
				if(!row){
					row = new_node;
				}
				new_node->left = row->left;
				new_node->right = row;
				row->left->right = new_node;
				row->left = new_node;
				col->col_size++;
			} else {
				// cout << "0";
			}
			col = col->right;
		}
		// cout << endl;
		row = NULL;
	}
	return h;
}

void print_graph(Node *h){
	Node *col, *row;
	col = h->right;
	Node* temp;
	while(col!=h){
		cout << "col " << col->num << endl;
		row = col->down;
		while(row!=col){
			cout << row->num << ",";
			temp = row->down;
			delete row;
			row = temp;
		}
		cout << endl;
		temp = col->right;
		delete col;
		col = temp;
	}
}

void select(Node *col){ 
	// cout << "selecting col " << col->num << endl;
	col->right->left = col->left;
	col->left->right = col->right;

	for(Node* row = col->down; row != col; row = row->down) {
		for(Node *right = row->right; right!=row; right = right->right){
			right->col_header->col_size--;
			right->up->down = right->down;
			right->down->up = right->up;
		}
	}
}

void deselect(Node *col){
	for(Node* row = col->up ; row != col ; row = row->up ) {
	     	for( Node* left = row->left ; left != row ; left = left->left) { 
	     		left->up->down = left;
	     		left->down->up = left;
	     		left->col_header->col_size++;
	     	} 
	}
	col->right->left = col;
	col->left->right = col;
}

Node *chooseNextColumn(Node *h){
	uint min = numeric_limits<int>::max();
	Node* min_col = NULL;
	for(Node *col = h->right; col!=h; col=col->right){
		if (col->col_size < min) {
			min = col->col_size;
			min_col = col;
		}
	}
	return min_col;
}

void print_solution(vector<int> *sol) {
	for(vector<int>::const_iterator i = sol->begin(); i != sol->end(); ++i) {
	    cout << *i << ' ';
	}
	cout << endl;
}

void search(Node *h, vector<int> *sol, int depth) {
	if (h->right == h) {
		// cout << "printing solution" << endl;
		print_solution(sol);
		return;
	}
	Node* col = chooseNextColumn(h);
	// cout << "selecting col " << col->num << endl;
	select(col);

	for(Node* row = col->down; row != col; row = row->down){
		// cout << "removing row " << row->num << endl;
		sol->push_back(row->num);

		for(Node *right = row->right; right != row; right = right->right) {
			select(right->col_header);
		}

		search(h, sol, depth + 1);

		// cout << "putting back " << row->num << endl;

		for(Node *left = row->left; left != row; left=left->left){
			deselect(left->col_header);
		}
		sol->pop_back();
	}

	// cout << "deselecting col " << col->num << endl;
	deselect(col);
	return;
}

int count_cols(Node* h) {
	int num_cols = 0;
	for(Node* col = h->right; col!=h; col=col->right){
		num_cols++;
	}
	return num_cols;
}

int main() {
	Node *h = read_graph();
	vector<int> *sol = new vector<int>();
	search(h, sol, 0);
	// print_graph(h);
	return 0;
}