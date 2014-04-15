#include<iostream>

using namespace std;

typedef struct Node{
	uint num, col_size;
	Node *up, *down, *left, *right;
} Node;

Node *create_node(){
	return (Node *)malloc(sizeof(Node));
}

Node *create_h(){
	Node *h = create_node();
	h->up = h;
	h->down = h;
	h->right = h;
	h->left = h;
	return h;
}

void initialize_col_headers(int C, Node* h){
	for(int c=0;c<C;c++){
		Node *curr = create_node();
		curr->right = h;
		curr->left = h->left;
		h->left->right = curr;
		h->left = curr;
		curr->up = curr;
		curr->down = curr;
		curr->col_size = 0;
		curr->num = c;
	}
}

int main() {
	int R, C;
	cin >> R >> C;
	Node *h = create_h();
	initialize_col_headers(C, h);
	int curr;
	Node *col;
	Node *row = NULL;
	for(int r=0;r<R;r++){
		col = h->right;
		printf("%02d : ", r);
		for(int c=0;c<C;c++){
			cin>>curr;
			if(curr){
				cout << "1";
				Node* new_node = create_node();
				new_node->num = r;
				new_node->up = col->up;
				new_node->down = col;
				col->up->down = new_node;
				col->up = new_node;
				if(!row){
					row = new_node;
					row->right = row;
					row->left = row;
				}
				new_node->left = row->left;
				new_node->right = row;
				row->left->right = new_node;
				row->left = new_node;
				col->col_size++;
			} else {
				cout << "0";
			}
			col = col->right;
		}
		cout << endl;
		row = NULL;
	}
	col = h->right;
	Node* temp;
	while(col!=h){
		cout << "col " << col->num << endl;
		row = col->down;
		while(row!=col){
			cout << row->num << ",";
			temp = row->down;
			// free(row);
			row = temp;
		}
		cout << endl;
		temp = col->right;
		// free(col);
		col = temp;
	}
	return 0;
}