import copy

def Mix_Column(Matrix,block_num):
	Mix_Column_matrix = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]] #Mix Column과정에서 사용할 행렬 선언 리스트 Mix_Column_matrix[x][y] 에서 x 는 행번호 y는 열번호를 나타낸다.
	Result_Matrix = copy.deepcopy(Matrix)
	
	for column in range(4):				#인자값으로 받은 행렬의 열
		for special_row in range(4):	#특정한 행렬의 행 (Mix_Column_matrix의 행)
			Result = 0xFF				#Result값의 초기값을 설정해준다. Xor연산의 성질을 이용하기 위해 초기값을 숫자로 설정해준다.

			
			for same_index in range(4):	#입력해준 행렬의 열의 몇번째 행의 값인지 알려주는 index = 특정한 행렬의 행에서 몇번 열인지 값인지 알려주는 index  
				Mix_Column_value = Mix_Column_matrix[special_row][same_index]	#Mix_Column_matrix의 각 행과 열에 대응하는 값을 의미한다.
				matrix_value = Matrix[block_num][same_index][column]			#인자값으로 받은 행렬의 블록의 번호와 행과 열에 대응하는 값을 의미한다.
				matrix_value = bin(int(matrix_value,16))[2:]					#16진수를 2진수로 바꿔주는 과정 밑에서 길이가 8인 비트열에 대해 경우가 나뉘기 때문.
				matrix_value = '0'*(8-len(matrix_value)) + matrix_value			#2진수 값으로 변환한 결과에서 앞의 '0b'를 제외한 값
				
				if Mix_Column_value == 1:	#반복문을 돌면서 만약 Mix_Column_matrix의 값이 1이라면 -> 인자값으로 준 행렬의 한멤버 * 1 이므로 결과를 곱하기전의 값으로 한다. 
					Result = Result ^ int(matrix_value,2)

				elif Mix_Column_value == 2:	#반복문을 돌면서 만약 Mix_Column_matrix의 값이 2라면 -> 인자값으로 준 행렬의 한멤버 * 2 이되는데 AES표준 암호화 방식에 의해 또 두가지 경우로 나뉜다.
				
					if matrix_value[0] == '1':				#만약 인자값으로 준 행렬의 멤버를 8비트의 2진수로 변환했을때 가장 앞 비트가 1이라면
						shifted_matrix_value = int(matrix_value,2) << 1#왼쪽으로 1번 쉬프트후 0x1b를 xor 해준다.
						shifted_matrix_value = shifted_matrix_value - 256
						Result = Result ^ shifted_matrix_value ^ 0x1b
						
					else:												#만약 인자값으로 준 행렬의 멤버를 8비트의 2진수로 변환했을때 가장 앞 비트가 1이 아니라면
						shifted_matrix_value = int(matrix_value,2) << 1#왼쪽으로 1번 쉬프트만 해준다.
						Result = Result ^ shifted_matrix_value
						
				elif Mix_Column_value == 3:	#반복문을 돌면서 만약 Mix_Column_matrix의 값이 3이라면 -> 인자값으로준 행렬의 한멤버 * 3 이되는데 AES표준 암호화 방식에 의해 또 두가지 경우로 나뉜다.
				
					if matrix_value[0] == '1':				#만약 인자값으로 준 행렬의 멤버를 8비트의 2진수로 변환했을때 가장 앞 비트가 1이라면
						shifted_matrix_value = int(matrix_value,2) << 1#왼쪽으로 1번 쉬프트후 0x1b를 xor 해주고 쉬프트전의 값을 xor해서 리턴한다.
						shifted_matrix_value = shifted_matrix_value - 256
						Result = Result ^ shifted_matrix_value ^ 0x1b ^ int(matrix_value,2)
						
					else:												#만약 인자값으로 준 행렬의 멤버를 8비트의 2진수로 변환했을때 가장 앞 비트가 0이라면
						shifted_matrix_value = int(matrix_value,2) << 1#왼쪽으로 1번 쉬프트후 쉬프트전의 값을 xor해서 리턴한다.
						Result = Result ^ shifted_matrix_value ^ int(matrix_value,2)
						
						
				#Result = Result ^ 0xFF
				#Result = hex(Result)[2:] #16진수로 변환하고 앞에 붙는 '0x'값을 날려준다.
				#print(Result)
			Result = Result ^ 0xFF
			Result = hex(Result)[2:]
			if len(Result) == 1:
				Result = '0' + Result
			Result_Matrix[block_num][special_row][column] = Result #matrix에 반복문을 돌면서 나온 결과를 하나씩 꼽아준다.
		
	return Result_Matrix
	
result = Mix_Column([[['d4','e0','b8','1e'],['bf','b4','41','27'],['5d','52','11','98'],['30','ae','f1','e5']]],0)
print(result)
