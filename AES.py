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
	
	
def Padding(hex_plain):
	if int(len(hex_plain)/2)%16 != 0: #이과정을 통해서 평문이 16진수 이면서 32의배수인 문자열길이를 만족한다.
		padding_num = 16 - int(len(hex_plain)/2)%16 #패딩과정에서 X923패딩사용
		
		if padding_num >= 10:
			hex_plain += '00'*(padding_num - 1)+str(padding_num)
		else:
			hex_plain += '00'*(padding_num - 1)+'0'+str(padding_num)
			
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


def Sub_Bytes(hex_matrix,block_num):#Sub_Bytes과정도 block_num을 인자로 받아서 전체 반복문 걸렸을때 반복
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
		 ['e7','c8','37','6d','8d','5d','4e','a9','6c','56','f4','ea','65','7a','ae','08'],
		 ['ba','78','25','2e','1c','a6','b4','c6','e8','dd','74','1f','4b','bd','8b','8a'],
		 ['70','3e','b5','66','48','03','f6','0e','61','35','57','b9','86','c1','1d','9e'],
		 ['e1','f8','98','11','69','d9','8e','94','9b','1e','87','e9','ce','55','28','df'],
		 ['8c','a1','89','0d','bf','e6','42','68','41','99','2d','0f','b0','54','bb','16']]
		 
	for row in range(4):
		for column in range(4):
			S_Box_row = int(hex_matrix[block_num][row][column][0],16)	#S-Box에서 행의 번호를 나타낼부분
			S_Box_column = int(hex_matrix[block_num][row][column][1],16)#S-box에서 열의 번호를 나타낼부분
			hex_matrix[block_num][row][column] = S_Box[S_Box_row][S_Box_column]#S-box에서 대응된 값을 hex_matrix변수에 넣어주는과정
				
	return hex_matrix
	
	
def list_shift(list,shift_num):
	for x in range(shift_num):
		val = list.pop(0)
		list.append(val)

	
def Shift_Rows(matrix,block_num):#인자 값으로 4x4 행렬을 받는다. block_num을 받아야하지? def Shift_Rows(matrix,block_num)
	for row in range(4):
		list_shift(matrix[block_num][row],row) #list_shift(matrix[block_num][row],row)
	return matrix

	
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
						
						
			Result = Result ^ 0xFF
			Result = hex(Result)[2:]
			if len(Result) == 1:
				Result = '0' + Result
			Result_Matrix[block_num][special_row][column] = Result #matrix에 반복문을 돌면서 나온 결과를 하나씩 꼽아준다.
		
	return Result_Matrix
	
result = Mix_Column([[['d4','e0','b8','1e'],['bf','b4','41','27'],['5d','52','11','98'],['30','ae','f1','e5']]],0)
print(result)

	

#확인하는 과정
hex_plain = change_to_hex('zdsdadadadsd')#평문을 입력해준다.
hex_plain = Padding(hex_plain) #입력한 평문을 블록의 크기에맞게 패딩해준다.

plain_matrix = make_matrix(hex_plain)#16진수로 변환된 평문을 4x4행렬로 만들어준다.
print(plain_matrix)
block_num = len(plain_matrix)-1 #새로 생성


key_matrix = make_key_matrix() #키를 만들고 16진수로 구성된 4x4행렬을 리턴
print(key_matrix)


XOR_result = matrix_XOR(plain_matrix,key_matrix,block_num) #키행렬과 평문행렬을 XOR한 결과를 XOR_result에 저장
print(XOR_result)


Sub_Bytes_result = Sub_Bytes(XOR_result,block_num)		   #XOR연산이 끝난 행렬이 Sub_Bytes과정을 거친다.
print(Sub_Bytes_result)


Shift_Rows_result = Shift_Rows(Sub_Bytes_result,block_num) #Sub_Bytes 과정을 거친 행렬을 쉬프트해주는과정
print(Shift_Rows_result)


Mix_Column_result = Mix_Column(Shift_Rows_result,block_num)
print(Mix_Column_result)
