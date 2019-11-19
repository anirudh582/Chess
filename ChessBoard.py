class ChessBoard:
    def __init__(self):
        self.board = []
        self.board.append(['BR','BN','BB','BQ','BK','BB','BN','BR'])
        self.board.append(['BP','BP','BP','BP','BP','BP','BP','BP'])
        self.board.append(['--','--','--','--','--','--','--','--']) 
        self.board.append(['--','--','--','--','--','--','--','--']) 
        self.board.append(['--','--','--','--','--','--','--','--']) 
        self.board.append(['--','--','--','--','--','--','--','--']) 
        self.board.append(['WP','WP','WP','WP','WP','WP','WP','WP'])
        self.board.append(['WR','WN','WB','WQ','WK','WB','WN','WR'])
        
    def show_board(self):
        for i in range(8):
            for j in range(8):
                print(self.board[i][j], end="|")
            print()

