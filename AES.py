#AES 표준 ECB

def change_to_hex(text):#인자값으로 받은 문자열을 16진수로 변환에서 리턴하는 함수.
	hex_result = ''		#16진수로 변환된 결과를 받을 빈 문자열
	for x in text:
		hex_element = hex(ord(x))[2:]#hex함수를 써서 16진수로 변환하면 '0x'값이 붇는데 이를 지워준다.
		
		if len(hex_element)%2 != 0:	 #평문의 각 문자가 바이트 단위로 떨어지도록 16진수 짝수 자리가 되도록 한다.
			hex_element = '0' + hex_element
			hex_result += hex_element
		else:
			hex_result += hex_element
			
	return hex_result
	
'''
def Padding(hex_plain):
	if int(len(hex_plain)/2)%16 != 0: #이과정을 통해서 평문이 16진수 이면서 32의배수인 문자열길이를 만족한다.
		padding_num = 16 - int(len(hex_plain)/2)%16 #패딩과정에서 X923패딩사용
		hex_plain += '00'*(padding_num - 1) + '0' + hex(padding_num)[2:]#padding_num의 범위는 0~15이므로 16진수로 바꾸면 무조건 한자리

	return hex_plain
'''
def Padding(hex_plain):
	if int(len(hex_plain)/2)%16 != 0: #이과정을 통해서 평문이 16진수 이면서 32의배수인 문자열길이를 만족한다.
		padding_num = 16 - int(len(hex_plain)/2)%16 #패딩과정에서 X923패딩사용
		hex_plain += '00'*(padding_num)

	return hex_plain

	
#행렬을 모듈을 쓰지 않고 리스트로 구현할 것이다.
def make_matrix(hex_text):#4x4행렬을 만들어주는 함수이다.
	matrix = []			  #결과를 받을 리스트
	for block_num in range(int(len(hex_text)/32)):#128bits블록을 나눠서 나눠진 블록 만큼 반복
		tmp1 = []
		for row in range(4): 	#4x4행렬 이기떄문에 4번을 반복 
			tmp2 = []			#임시로 만든 리스트
			for column in range(4):
				tmp2.append(hex_text[block_num*32+row*2+column*8:block_num*32+row*2+column*8+2])
			tmp1.append(tmp2)
		matrix.append(tmp1)
			
	return matrix

#위에서 만든 make_matrix함수를 이용해서 만들었는데 이러니까 키 행렬을 만들때도 의도치않은 블록이 생김


def make_key_matrix():#함수이름 그대로 키를 받아서 행렬로만든다음 리턴하는 함수.
	while True:		  #무한루프
		key = input("16바이트 키를 입력하시오 : ")
		hex_key = change_to_hex(key)
		if len(hex_key)//2 == 16:	 #키의크기가 16바이트 128비트를 만족하면 무한루프를 빠져나간다.
			break
			
	
	key_matrix  = []  #키행렬을 받아올 리스트 선언
	for row in range(4):
		tmp = []
		for column in range(4): #hex_key 16진수로 변환한 키
			tmp.append(hex_key[row*2 + column*8 : row*2 + column*8 + 2])
		key_matrix.append(tmp)
	
	return key_matrix	


def matrix_XOR(plain_matrix,key_matrix,block_num):#행렬끼리의 xor 연산을 담당하는 함수이다.
	matrix = []
	tmp1 = []
	for row in range(4):
		tmp2 = []
		for column in range(4):
			XOR_result = hex(int(plain_matrix[block_num][row][column],16) ^ int(key_matrix[row][column],16))
			XOR_result = XOR_result[2:]
			
			if len(XOR_result)%2 != 0:
				XOR_result = '0' + XOR_result
			tmp2.append(XOR_result)
		tmp1.append(tmp2)
	matrix.append(tmp1)
	
	return matrix
	
	
#키 행렬 생성을 블록없이 리스트안에 리스트 4개로 표현


def Sub_Bytes_matrix(hex_matrix,block_num):#Sub_Bytes과정도 block_num을 인자로 받아서 전체 반복문 걸렸을때 반복
	S_Box = [['63','7c','77','7b','f2','6b','6f','c5','30','01','67','2b','fe','d7','ab','76'],
			 ['ca','82','c9','7d','fa','59','47','f0','ad','d4','a2','af','9c','a4','72','c0'],
			 ['b7','fd','93','26','36','3f','f7','cc','34','a5','e5','f1','71','d8','31','15'],
			 ['04','c7','23','c3','18','96','05','9a','07','12','80','e2','eb','27','b2','75'],
			 ['09','83','2c','1a','1b','6e','5a','a0','52','3b','d6','b3','29','e3','2f','84'],
			 ['53','d1','00','ed','20','fc','b1','5b','6a','cb','be','39','4a','4c','58','cf'],
			 ['d0','ef','aa','fb','43','4d','33','85','45','f9','02','7f','50','3c','9f','a8'],
			 ['51','a3','40','8f','92','9d','38','f5','bc','b6','da','21','10','ff','f3','d2'],
			 ['cd','0c','13','ec','5f','97','44','17','c4','a7','7e','3d','64','5d','19','73'],
			 ['60','81','4f','dc','22','2a','90','88','46','ee','b8','14','de','5e','0b','db'],
			 ['e0','32','3a','0a','49','06','24','5c','c2','d3','ac','62','91','95','e4','79'],
			 ['e7','c8','37','6d','8d','d5','4e','a9','6c','56','f4','ea','65','7a','ae','08'],
			 ['ba','78','25','2e','1c','a6','b4','c6','e8','dd','74','1f','4b','bd','8b','8a'],
			 ['70','3e','b5','66','48','03','f6','0e','61','35','57','b9','86','c1','1d','9e'],
			 ['e1','f8','98','11','69','d9','8e','94','9b','1e','87','e9','ce','55','28','df'],
			 ['8c','a1','89','0d','bf','e6','42','68','41','99','2d','0f','b0','54','bb','16']]
		 
	for row in range(4):
		for column in range(4):
			S_Box_row = int(hex_matrix[block_num][row][column][0],16)		#S-Box에서 행의 번호를 나타낼부분
			S_Box_column = int(hex_matrix[block_num][row][column][1],16)	#S-box에서 열의 번호를 나타낼부분
			hex_matrix[block_num][row][column] = S_Box[S_Box_row][S_Box_column]#S-box에서 대응된 값을 hex_matrix변수에 넣어주는과정
				
	return hex_matrix
	
	
def left_shift(list,shift_num):
	for x in range(shift_num):
		val = list.pop(0)
		list.append(val)

	
def Shift_Rows(matrix,block_num):				#인자 값으로 4x4 행렬을 받는다. block_num을 받아야하지? def Shift_Rows(matrix,block_num)
	for row in range(4):
		left_shift(matrix[block_num][row],row) 	#left_shift(matrix[block_num][row],row)
	return matrix


import copy

def Mix_Column(Matrix,block_num):
	Mix_Column_matrix = [[2,3,1,1],	#Mix Column과정에서 사용할 행렬 선언 리스트 Mix_Column_matrix[x][y] 에서 x 는 행번호 y는 열번호를 나타낸다.
						 [1,2,3,1],
						 [1,1,2,3],
						 [3,1,1,2]]
						 
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
				
					if matrix_value[0] == '1':							#만약 인자값으로 준 행렬의 멤버를 8비트의 2진수로 변환했을때 가장 앞 비트가 1이라면
						shifted_matrix_value = int(matrix_value,2) << 1	#왼쪽으로 1번 쉬프트후 0x1b를 xor 해준다.
						shifted_matrix_value = shifted_matrix_value - 256
						Result = Result ^ shifted_matrix_value ^ 0x1b
						
					else:												#만약 인자값으로 준 행렬의 멤버를 8비트의 2진수로 변환했을때 가장 앞 비트가 1이 아니라면
						shifted_matrix_value = int(matrix_value,2) << 1	#왼쪽으로 1번 쉬프트만 해준다.
						Result = Result ^ shifted_matrix_value
						
				elif Mix_Column_value == 3:	#반복문을 돌면서 만약 Mix_Column_matrix의 값이 3이라면 -> 인자값으로준 행렬의 한멤버 * 3 이되는데 AES표준 암호화 방식에 의해 또 두가지 경우로 나뉜다.
				
					if matrix_value[0] == '1':							#만약 인자값으로 준 행렬의 멤버를 8비트의 2진수로 변환했을때 가장 앞 비트가 1이라면
						shifted_matrix_value = int(matrix_value,2) << 1	#왼쪽으로 1번 쉬프트후 0x1b를 xor 해주고 쉬프트전의 값을 xor해서 리턴한다.
						shifted_matrix_value = shifted_matrix_value - 256
						Result = Result ^ shifted_matrix_value ^ 0x1b ^ int(matrix_value,2)
						
					else:												#만약 인자값으로 준 행렬의 멤버를 8비트의 2진수로 변환했을때 가장 앞 비트가 0이라면
						shifted_matrix_value = int(matrix_value,2) << 1	#왼쪽으로 1번 쉬프트후 쉬프트전의 값을 xor해서 리턴한다.
						Result = Result ^ shifted_matrix_value ^ int(matrix_value,2)
						
						
			Result = Result ^ 0xFF
			Result = hex(Result)[2:]
			if len(Result) == 1:
				Result = '0' + Result
			Result_Matrix[block_num][special_row][column] = Result #matrix에 반복문을 돌면서 나온 결과를 하나씩 꼽아준다.
		
	return Result_Matrix


def Sub_Bytes(hex_element):#위에 선언한 Sub_Bytes_matrix와 달리 1바이트 16진수를 받아서 Sub Bytes 과정을 거친 결과를 리턴한다.
	S_Box = [['63','7c','77','7b','f2','6b','6f','c5','30','01','67','2b','fe','d7','ab','76'],
			 ['ca','82','c9','7d','fa','59','47','f0','ad','d4','a2','af','9c','a4','72','c0'],
			 ['b7','fd','93','26','36','3f','f7','cc','34','a5','e5','f1','71','d8','31','15'],
			 ['04','c7','23','c3','18','96','05','9a','07','12','80','e2','eb','27','b2','75'],
			 ['09','83','2c','1a','1b','6e','5a','a0','52','3b','d6','b3','29','e3','2f','84'],
			 ['53','d1','00','ed','20','fc','b1','5b','6a','cb','be','39','4a','4c','58','cf'],
			 ['d0','ef','aa','fb','43','4d','33','85','45','f9','02','7f','50','3c','9f','a8'],
			 ['51','a3','40','8f','92','9d','38','f5','bc','b6','da','21','10','ff','f3','d2'],
			 ['cd','0c','13','ec','5f','97','44','17','c4','a7','7e','3d','64','5d','19','73'],
			 ['60','81','4f','dc','22','2a','90','88','46','ee','b8','14','de','5e','0b','db'],
			 ['e0','32','3a','0a','49','06','24','5c','c2','d3','ac','62','91','95','e4','79'],
			 ['e7','c8','37','6d','8d','d5','4e','a9','6c','56','f4','ea','65','7a','ae','08'],
			 ['ba','78','25','2e','1c','a6','b4','c6','e8','dd','74','1f','4b','bd','8b','8a'],
			 ['70','3e','b5','66','48','03','f6','0e','61','35','57','b9','86','c1','1d','9e'],
			 ['e1','f8','98','11','69','d9','8e','94','9b','1e','87','e9','ce','55','28','df'],
			 ['8c','a1','89','0d','bf','e6','42','68','41','99','2d','0f','b0','54','bb','16']]

	if len(hex_element) != 2:				#S_box표에 대응될수 있도록 값을 변조 하는 부분
		hex_element = '0' + hex_element
	S_Box_row = int(hex_element[0],16)		#S-Box에서 행의 번호를 나타낼부분
	S_Box_column = int(hex_element[1],16)	#S-box에서 열의 번호를 나타낼부분
	Result = S_Box[S_Box_row][S_Box_column]	#S-box에서 대응된 값을 hex_matrix변수에 넣어주는과정
				
	return Result


def make_Round_key(key_matrix):#키스케줄 알고리즘을 통해 각 라운드에서 쓰이는 라운드 키를 만드는 함수.
	Rcon = [['01','02','04','08','10','20','40','80','1b','36'], #인자값으로 받은 키와 Xor 할 행렬 선언
			['00','00','00','00','00','00','00','00','00','00'],
			['00','00','00','00','00','00','00','00','00','00'],
			['00','00','00','00','00','00','00','00','00','00']]
	Round_key_matrix = []				#결과를 받을 리스트 선언
	Round_key_matrix.append(key_matrix)	#암호화 과정 제일 첫번째 과정에서 인자값으로 받은 키를 라운드0에 쓰는 키라고 생각하겠다.
										#왜냐하면 그 다음 라운드 키를 만드는 과정에서 그전의 키값 정보를 사용하기 때문이다.
	
	for Round in range(10):	#총 10라운드를 진행한다.
		tmp = []			#반복문 과정에서 임시로 결과를 저장할 리스트
		tmp1 = []			#3중리스트를 사용해서 Round_key_matrix[x][y][z]라하면 x는 라운드,y는 행,z는 열을 나타내준다.
		
		for x in range(4):	#각 라운드가 시작되고 구하려하는 라운드의 첫번째열은 다른열을 구하는 것과 달라서 구별해준다.
			Target = Round_key_matrix[Round][(1+x)%4][3]#한칸씩 밀어주는과정
			Target = Sub_Bytes(Target)					#타겟 즉,Xor연산을 거치려는 값을 S_box치환 해준다.
			Target = int(Target,16) 					#16진수를 10진수로 변환
			Result = int(Rcon[x][Round],16) ^ Target ^ int(Round_key_matrix[Round][x][0],16)
			Result = hex(Result)[2:]#hex함수 결과로 앞에 붙는 '0x'부분 날려준다.
			
			if len(Result) == 1:	#예를 들어 0x1 이라는 값을 일관성 있게 0x01 처럼 '0x'뒤의 자리수를 두자리로 맞춰준다.
				Result = '0' + Result
				
			tmp1.append(Result)		#tmp1에 그값을 추가한다.
			tmp.append(tmp1)		#tmp에 tmp1을 추가함으로써 tmp리스트는 리스트를 멤버로 가진다.
			tmp1 = []				#tmp1은 반복문을 돌때마다 새로운 값을 받아올 것 이므로 초기화를 해주는 과정.
			
		for column in range(3):	#현재 라운드에서의 첫번째 열은 위의 반복문에서 처리됬으므로 남은 3개의 열을 처리하는 과정.
			for row in range(4):#각 행의 번호를 바꿔가면서 값을 채운다.
				Result = int(tmp[row][column],16) ^ int(Round_key_matrix[Round][row][column+1],16)
				Result = hex(Result)[2:]
				tmp[row].append(Result)
	
		Round_key_matrix.append(tmp)
		
	return Round_key_matrix		
				
def Right_Shift(list,shift_num):		#암호화 과정의 왼쪽으로 쉬프트와 반대로 오른쪽으로 쉬프트 한다.
	for x in range(shift_num):
		last_value = list.pop()
		list.insert(0,last_value)
		
	

def Inv_Shift_Rows(matrix,block_num):				#인자 값으로 4x4 행렬을 받는다.
	for row in range(4):
		Right_Shift(matrix[block_num][row],row) 	#각행 마다 쉬프트 값이 다른것을 적용
	return matrix	


def Inv_Sub_Bytes_matrix(hex_matrix,block_num):#Sub_Bytes의 역과정
	Inverse_S_Box =[['52','09','6a','d5','30','36','a5','38','bf','40','a3','9e','81','f3','d7','fb'],
					['7c','e3','39','82','9b','2f','ff','87','34','8e','43','44','c4','de','e9','cb'],
					['54','7b','94','32','a6','c2','23','3d','ee','4c','95','0b','42','fa','c3','4e'],
					['08','2e','a1','66','28','d9','24','b2','76','5b','a2','49','6d','8b','d1','25'],
					['72','f8','f6','64','86','68','98','16','d4','a4','5c','cc','5d','65','b6','92'],
					['6c','70','48','50','fd','ed','b9','da','5e','15','46','57','a7','8d','9d','84'],
					['90','d8','ab','00','8c','bc','d3','0a','f7','e4','58','05','b8','b3','45','06'],
					['d0','2c','1e','8f','ca','3f','0f','02','c1','af','bd','03','01','13','8a','6b'],
					['3a','91','11','41','4f','67','dc','ea','97','f2','cf','ce','f0','b4','e6','73'],
					['96','ac','74','22','e7','ad','35','85','e2','f9','37','e8','1c','75','df','6e'],
					['47','f1','1a','71','1d','29','c5','89','6f','b7','62','0e','aa','18','be','1b'],
					['fc','56','3e','4b','c6','d2','79','20','9a','db','c0','fe','78','cd','5a','f4'],
					['1f','dd','a8','33','88','07','c7','31','b1','12','10','59','27','80','ec','5f'],
					['60','51','7f','a9','19','b5','4a','0d','2d','e5','7a','9f','93','c9','9c','ef'],
					['a0','e0','3b','4d','ae','2a','f5','b0','c8','eb','bb','3c','83','53','99','61'],
					['17','2b','04','7e','ba','77','d6','26','e1','69','14','63','55','21','0c','7d']]
	
	for row in range(len(hex_matrix[0])):
		for column in range(len(hex_matrix[0][0])):
			Inverse_S_Box_row = int(hex_matrix[block_num][row][column][0],16)
			Inverse_S_Box_column = int(hex_matrix[block_num][row][column][1],16)
			hex_matrix[block_num][row][column] = Inverse_S_Box[Inverse_S_Box_row][Inverse_S_Box_column]
	
	return hex_matrix
	
	
#AES에서 *2과정을 담당하는 함수.
#'쉬프트 하기전의 바이트 = 쉬프트 결과 바이트'가 만족하게 쉬프트 해주는 함수.
def Safe_Shift(Bin): #인자값으로 길이가 8인 비트열을 받는다.(1바이트)
	if Bin[0] == '1':#가장 왼쪽의 비트가 1이라면
		Safe_Shift_value = int(Bin,2) << 1
		Safe_Shift_value -= 256
		Result = Safe_Shift_value ^ 0x1b
	else:			 #가장 오른쪽의 비트가 0이라면
		Result = int(Bin,2) << 1
	
	return Result




import copy

def Inv_Mix_Column(Matrix,block_num):
	Inv_Mix_Column_matrix = [[14,11,13,9], #Mix Column과정에서 사용할 행렬 선언 리스트 Inv_Mix_Column_matrix[x][y] 에서 x 는 행번호 y는 열번호를 나타낸다.
							 [9,14,11,13],
							 [13,9,14,11],
							 [11,13,9,14]]
						 
	Result_Matrix = copy.deepcopy(Matrix)
	
	for column in range(4):				#인자값으로 받은 행렬의 열
		for special_row in range(4):	#특정한 행렬의 행 (Inv_Mix_Column_matrix의 행)
			Final_Result = 0xFF			#Result값의 초기값을 설정해준다. Xor연산의 성질을 이용하기 위해 초기값을 숫자로 설정해준다.

			
			for same_index in range(4):	#입력해준 행렬의 열의 몇번째 행의 값인지 알려주는 index = 특정한 행렬의 행에서 몇번 열인지 값인지 알려주는 index  
				Inv_Mix_Column_value = Inv_Mix_Column_matrix[special_row][same_index]	#Inv_Mix_Column_matrix의 각 행과 열에 대응하는 값을 의미한다.
				matrix_value = Matrix[block_num][same_index][column]					#인자값으로 받은 행렬의 블록의 번호와 행과 열에 대응하는 값을 의미한다.
				matrix_value = bin(int(matrix_value,16))[2:]							#16진수를 2진수로 바꿔주는 과정 밑에서 길이가 8인 비트열에 대해 경우가 나뉘기 때문.
				matrix_value = '0'*(8-len(matrix_value)) + matrix_value					#2진수 값으로 변환한 결과에서 앞의 '0b'를 제외한 값
				
				if Inv_Mix_Column_value == 9:#9*x = ((x*2)*2)*2+x
					Result = Safe_Shift(matrix_value)
					Result = Safe_Shift('0'*(8-len(bin(Result)[2:])) + bin(Result)[2:])
					Result = Safe_Shift('0'*(8-len(bin(Result)[2:])) + bin(Result)[2:])
					Final_Result = Final_Result ^ Result ^ int(matrix_value,2)

				elif Inv_Mix_Column_value == 11:#11*x = (((x*2)*2)+x)*2 +x
					Result = Safe_Shift(matrix_value)
					Result = Safe_Shift('0'*(8-len(bin(Result)[2:])) + bin(Result)[2:])
					Result = Result ^ int(matrix_value,2)
					Result = Safe_Shift('0'*(8-len(bin(Result)[2:])) + bin(Result)[2:])
					Final_Result = Final_Result ^ Result ^ int(matrix_value,2)
	
				elif Inv_Mix_Column_value == 13:#13*x = ((((x*2)+x)*2)*2)+x
					Result = Safe_Shift(matrix_value)
					Result = Result ^ int(matrix_value,2)
					Result = Safe_Shift('0'*(8-len(bin(Result)[2:])) + bin(Result)[2:])
					Result = Safe_Shift('0'*(8-len(bin(Result)[2:])) + bin(Result)[2:])
					Final_Result = Final_Result ^ Result ^ int(matrix_value,2)
					
				elif Inv_Mix_Column_value == 14:#14*x = (((x*2)+x)*2+x)*2
					Result = Safe_Shift(matrix_value)
					Result = Result ^ int(matrix_value,2)
					Result = Safe_Shift('0'*(8-len(bin(Result)[2:])) + bin(Result)[2:])
					Result = Result ^ int(matrix_value,2)
					Final_Result = Final_Result ^ Safe_Shift('0'*(8-len(bin(Result)[2:])) + bin(Result)[2:])
						
			Final_Result = Final_Result ^ 0xFF
			Final_Result = hex(Final_Result)[2:]
			if len(Final_Result) == 1:
				Final_Result = '0' + Final_Result
			Result_Matrix[block_num][special_row][column] = Final_Result #matrix에 반복문을 돌면서 나온 결과를 하나씩 꼽아준다.
		
	return Result_Matrix


def main():
	#암호화 과정 
	plaintext = input("평문을 입력해주세요 : ")		#평문을 입력받는다.
	hex_plain = change_to_hex(plaintext)	#평문을 16진수로 변환
	plaintext = Padding(hex_plain)			#평문을 블록크기에 맞게 패딩 해주는 과정
	plain_matrix = make_matrix(plaintext)	#4x4 평문 행렬 생성
	print('Plain_Matrix')
	for x in range(len(plain_matrix)):
		print('Block',x+1)
		for y in plain_matrix[x]:
			print(y)
	
	print('\n')
	
	key_matrix = make_key_matrix()					#4x4키 행렬 생성
	Round_key_matrix = make_Round_key(key_matrix)	#라운드 키 생성 
	
	ENC_Matrix = []#암호화 결과를 담을 빈 리스트 선언
	
	for block_num in range(len(plain_matrix)):
		XOR_result = matrix_XOR(plain_matrix,key_matrix,block_num)#1라운드에 들어가기전 키 행렬과 평문 행렬을 Xor한다. 이과정에서 수행할 블록의 행렬이 결정
		
		for Round in range(9):#Round 1 ~ 9
			block_num = 0	  #바로 위의 과정에서 수행할 블록의 행렬이 하나로 결정되었으므로 고정해준다.
			Sub_Bytes_result = Sub_Bytes_matrix(XOR_result,block_num)
			Shift_Rows_result = Shift_Rows(Sub_Bytes_result,block_num)
			Mix_Column_result = Mix_Column(Shift_Rows_result,block_num)
			XOR_result = matrix_XOR(Mix_Column_result,Round_key_matrix[Round+1],block_num)
		
		Round = 10
		
		#Round 10 Mix_Column과정을 생략하고 진행한다.
		Sub_Bytes_result = Sub_Bytes_matrix(XOR_result,block_num)
		Shift_Rows_result = Shift_Rows(Sub_Bytes_result,block_num)
		XOR_result = matrix_XOR(Shift_Rows_result,Round_key_matrix[Round],block_num)
		result = XOR_result
		ENC_Matrix.append(result[0])#3중 리스트로 표현하기 위한 조치
		
	print('\nENC_Matrix')
	#결과 행렬의 행과 열을 쉽게 볼 수 있도록 해준다.
	for row in range(len(ENC_Matrix)):
		print('Block',row+1)
		for column in ENC_Matrix[row]:
			print(column)

#================================================================================================================================================================				
	#복호화 과정
	DEC_Matrix = []#복호화된 행렬을 받을 리스트를 선언
	for block_num in range(len(ENC_Matrix)):#복호화 과정에서는 위의 암호화과정의 결과를 이용하여 평문을 만든다.
		XOR_result = matrix_XOR(ENC_Matrix,Round_key_matrix[10],block_num)#1라운드에 들어가기전(0라운드) 키 행렬과 평문 행렬을 Xor한다. 이과정에서 수행할 블록의 행렬이 결정
		Round_result = XOR_result	#각 라운드에서의 결과를 받는 변수
		
		for Round in range(9):#Inv.Round 1 ~ 9
			block_num = 0	  #바로 위의 과정에서 수행할 블록의 행렬이 하나로 결정되었으므로 고정해준다.
			
			
			Inv_Shift_Rows_result = Inv_Shift_Rows(Round_result,block_num)
			Inv_Sub_Bytes_result = Inv_Sub_Bytes_matrix(Inv_Shift_Rows_result,block_num)
			XOR_result = matrix_XOR(Inv_Sub_Bytes_result,Round_key_matrix[9-Round],block_num)
			Inv_Mix_Column_result = Inv_Mix_Column(XOR_result,block_num)
			Round_result = Inv_Mix_Column_result#1~9라운드까지 도는 과정에서 각 라운드의 결과를 다음 라운드에 이용하므로 변수에 저장해서 이용한다.
			
		#Final Round -> Round 10 Inv Mix Columns과정을 생략하고 진행	
		Inv_Shift_Rows_result = Inv_Shift_Rows(Round_result,block_num)
		Inv_Sub_Bytes_result = Inv_Sub_Bytes_matrix(Inv_Shift_Rows_result,block_num)
		XOR_result = matrix_XOR(Inv_Sub_Bytes_result,Round_key_matrix[0],block_num)
		
		Final_Round_result = XOR_result 		#1~10라운드 과정을 모두 거쳐서 나온 결과를 저장

		DEC_Matrix.append(Final_Round_result[0])#행렬을 리스트로 구현했으므로 1~10라운드를 거쳐서 나온 결과를 리스트에 추가해준다.
		
		print('\nDEC_Matrix')
		#결과 행렬의 행과 열을 쉽게 볼 수 있도록 해준다.
		for row in range(len(DEC_Matrix)):
			print('Block',row+1)
			for column in DEC_Matrix[row]:
				print(column)

	
if __name__ == "__main__":
	main()
	a = input('')