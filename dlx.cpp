#include<iostream>
#include<vector>
#include<limits>
#include<cassert>

using namespace std;

struct Node{
	uint num, col_size;
	Node *up, *down, *left, *right, *col_header;

	Node() {
		up = down = left = right = this;
		col_header = NULL;
		col_size = 0;
	}
};

void initialize_col_headers(int C, Node* h){
	for(int c=0;c<C;c++){
		Node *curr = new Node();
		curr->right = h;
		curr->left = h->left;
		h->left->right = curr;
		h->left = curr;
		curr->num = c;
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

void check_graph(Node *h) {
	for(Node *col = h->right; col != h; col = col->right){
		int count = 0;
		for(Node *row = col->down; row != col; row = row->down) {
			assert(row->col_header == col);
			assert(row->right->left == row);
			assert(row->left->right == row);
			assert(row->up->down == row);
			assert(row->down->up == row);
			count++;
		}
		assert(col->col_size == count);
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
		// row->right->left = row->right;
		// row->left->right = row->left;
	}
	// cout << "done selecting col " << col->num << endl;
}

void deselect(Node *col){
	for(Node* row = col->up ; row != col ; row = row->up ) {
			// row->right->left = row;
	  //    	row->left->right = row;
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
	// cout << "starting depth " << depth << endl;
	if (h->right == h) {
		// cout << "printing solution" << endl;
		print_solution(sol);
		return;
	}
	Node* col = chooseNextColumn(h);
	// cout << "removing col " << col->num << endl;
	select(col);
	// check_graph(h);

	for(Node* row = col->down; row != col; row = row->down){
		// cout << "removing row " << row->num << endl;
		sol->push_back(row->num);

		for(Node *right = row->right; right != row; right = right->right) {
			select(right->col_header);
			// check_graph(h);
		}

		search(h, sol, depth + 1);

		// cout << "putting back " << row->num << endl;

		for(Node *left = row->left; left != row; left=left->left){
			deselect(left->col_header);
			// check_graph(h);
		}
		sol->pop_back();
	}

	// cout << "deselecting col " << col->num << endl;
	deselect(col);
	// check_graph(h);
	return;
}

int count_cols(Node* h) {
	int num_cols = 0;
	for(Node* col = h->right; col!=h; col=col->right){
		num_cols++;
	}
	return num_cols;
}

void delete_grid(Node* h){
	Node *col, *row;
	col = h->right;
	Node* temp;
	while(col!=h){
		row = col->down;
		while(row!=col){
			temp = row->down;
			delete row;
			row = temp;
		}
		temp = col->right;
		delete col;
		col = temp;
	}
	delete h;
}

int main() {
	Node *h = read_graph();
	vector<int> *sol = new vector<int>();
	// check_graph(h);
	// print_graph(h);
	search(h, sol, 0);
	delete_grid(h);
	return 0;
}